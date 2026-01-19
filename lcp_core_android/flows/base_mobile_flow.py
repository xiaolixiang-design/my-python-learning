#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: base_mobile_flow.py
@time: 8/18/2023 10:56 AM
@file_desc:
"""
import logging
import os
import time
import uiautomator2 as u2
import re

from typing import Any
from urllib import parse

import allure
import requests
from bs4 import BeautifulSoup
from requests import Response

from lcp_core_android.library.android_date_time_settings_po import AndroidDateTimeSettingsPo
from lcp_core_android.library.android_device_info_settings_po import AndroidDeviceInfoSettingsPo
from lcp_core_android.library.android_install_po import AndroidInstallPo
from lcp_core_android.library.android_languages_settings_po import AndroidLanguagesSettingsPo
from lcp_core_android.library.android_security_po import AndroidSecurityPo
from lcp_core_android.library.android_settings_po import AndroidSettingsPo
from lcp_core_android.library.extension_sample_app_po import AndroidExtensionAppPo
from lcp_core_android.library.main_po import MainPo
from utils.file_helper import get_temp_path

NoneType = type(None)
log = logging.getLogger(__name__)

# UDC_ANDROID_URL = 'https://artifactory.tc.lenovo.com/artifactory/lenovo-release-generic/UDC-Android-Platform'
UDC_ANDROID_URL = 'https://artifactory.tc.lenovo.com/artifactory/lenovo-release-generic/UDC/UDCAndroid'
UDC_ANDROID_DEVELOP_URL = 'https://artifactory.tc.lenovo.com/artifactory/lenovo-auto-delete-generic-local/UDC/UDCAndroid'

class BaseAndroidFlow(object):
    def __init__(self, driver: u2.Device):
        self.driver = driver
        self.main_po = MainPo(driver)
        self.android_settings_po = AndroidSettingsPo(driver)
        self.android_security_po = AndroidSecurityPo(driver)
        self.android_languages_po = AndroidLanguagesSettingsPo(driver)
        self.android_datetime_settings_po = AndroidDateTimeSettingsPo(driver)
        self.android_device_info_settings_po = AndroidDeviceInfoSettingsPo(driver)
        self.android_install_po = AndroidInstallPo(driver)
        self.android_extension_app_po = AndroidExtensionAppPo(driver)
        self.udc_version = None

    def home(self) -> NoneType:
        """BaseAndroidFlow.home

        Unlock and Go to home screen

        Parameters
        ----------
        :return: NoneType
        """
        self.main_po.go_home()

    def press_back(self) -> NoneType:
        """BaseAndroidFlow.press_back

        Press back

        Parameters
        ----------
        :return: NoneType
        """
        self.main_po.press_back()

    def __get_response(self, url):
        max_retries = 5
        retries = 0
        response = None
        error = None
        while retries < max_retries:
            try:
                response = requests.get(url, timeout=30)
                break
            except Exception as e:
                log.error(f"Error: {e}. Retrying...")
                error = e
                retries += 1
                time.sleep(retries)
        assert response is not None, 'Download build from artifactory failed. last error: %s' % error
        return response

    def __get_udc_release_branch_info(self, main_release_number=None, build_type="release") -> Response:
        """BaseAndroidFlow.__get_udc_release_branch_info

        Get udc release branch info

        Parameters
        ----------
        :param main_release_number: str: None, 23.10.0.0
        :return: Response
        """
        global UDC_ANDROID_URL
        global UDC_ANDROID_DEVELOP_URL
        if build_type == "develop" and main_release_number and main_release_number not in ["latest", "last"]:
            version_parts = main_release_number.split('.')
            if len(version_parts) == 4:
                sub_version = version_parts[-1]
                main_release_number = f"{sub_version}-{main_release_number}-develop"

        suffix = build_type

        if main_release_number is None or main_release_number == "latest":
            release_number = self.__get_main_release_branches()[0]
            url = f"{UDC_ANDROID_URL}/jmm/{suffix}/{release_number}"
        elif main_release_number == "last":
            release_number = self.__get_main_release_branches()[1]
            url = f"{UDC_ANDROID_URL}/jmm/{suffix}/{release_number}"
        elif build_type=="release":
            url = f"{UDC_ANDROID_URL}/jmm/{suffix}/{main_release_number}"
        elif build_type=="develop":
            url = f"{UDC_ANDROID_DEVELOP_URL}/jmm/{suffix}/{main_release_number}"

        log.info(url)
        response = self.__get_response(url)
        return response



    def __get_main_release_branches(self):
        suffix = "release"
        url = f"{UDC_ANDROID_URL}/jmm/{suffix}"
        log.info(url)
        response_release = self.__get_response(url)
        bs = BeautifulSoup(response_release.content.decode(), "html.parser")
        build_version_list = bs.find_all("a")
        build_version_dict_list = []
        for build in build_version_list:
            build_version = build.get("href").split("/")[0]
            if not build_version.startswith("..") and not build_version.startswith("jmm"):
                release_no = build_version.split("/")[0]
                build_version_dict_list.append(release_no)
        sorted_list = sorted(build_version_dict_list, reverse=True)
        return sorted_list

    def __get_target_build_number_from_sub_builds(self, url, sorted_list, pkg_type, env_type="test"):
        build_folder = "debug" if env_type == "test" else "release"
        target_build_number = None
        for i in range(len(sorted_list)):
            target_build_number = sorted_list[i].get("item") + "-" + sorted_list[i].get("version")
            log.info(target_build_number)
            url = parse.urljoin(url, target_build_number)
            response = requests.get(url, timeout=30)
            bs = BeautifulSoup(response.content.decode(), "html.parser")
            folder_list = bs.find_all("a")
            has_release = False
            for folder in folder_list:
                folder_name = folder.get("href").split("/")[0]
                log.info(folder_name)
                if folder_name == build_folder:
                    has_release = True
                    target_build_pkg_url = f"{url}/{build_folder}/{pkg_type}"
                    log.info(target_build_pkg_url)
                    response = requests.get(target_build_pkg_url, timeout=30)
                    if response.status_code != 200:
                        log.error(f"File not found: {url}\n{response.text}")
                        return None
                    else:
                        bs = BeautifulSoup(response.content.decode(), "html.parser")
                        pkg_list = bs.find_all("a")
                        has_pkg = False
                        for pkg in pkg_list:
                            apk_name = pkg.get("href").split("/")[0]
                            if apk_name.endswith(".apk"):
                                has_pkg = True
                                break
                        if has_pkg:
                            break
            if has_release:
                break
            else:
                target_build_number = None
        return target_build_number


    def __get_udc_target_build_number(self, response, build_number=None, pkg_type='privapp', env_type="test",
                                      build_type="release") -> str:
        url = response.url
        bs = BeautifulSoup(response.content.decode(), "html.parser")
        build_version_list = bs.find_all("a")
        build_version_dict_list = []

        for build in build_version_list:
            build_version = build.get("href").split("/")[0]
            if not build_version.startswith(".."):
                if build_type == "develop":
                    # develop version format: 358-29.09.1.358-develop
                    try:
                        item, full_version = build_version.split("-", 1)
                        build_version_dict_list.append({"item": item, "version": full_version})
                    except ValueError:
                        log.warning(f"Cannot decode develop version: {build_version}")
                else:
                    try:
                        item, sub_version = build_version.split("-")
                        build_version_dict_list.append({"item": item, "version": sub_version})
                    except ValueError:
                        log.warning(f"CAN NOT DECODE VERSION: {build_version}")

        target_build_number = ""
        if build_number is None or build_number == "latest":
            sorted_list = sorted(build_version_dict_list, key=lambda x: int(x['item']), reverse=True)
            target_build_number = self.__get_target_build_number_from_sub_builds(url, sorted_list, pkg_type, env_type)
        elif build_number is not None:
            for build_version_dict in build_version_dict_list:
                item = build_version_dict.get("item")
                version = build_version_dict.get("version")

                if build_type == "develop":
                    # develop regex logic: 29.09.1.612 match 612-29.09.1.612-develop
                    if build_number in version:
                        target_build_number = f"{item}-{version}"
                        break
                else:
                    # release logic
                    if f"{version}" == build_number:
                        target_build_number = f"{item}-{build_number}"
                        break

        log.info(f"target_build_number: {target_build_number}")
        return target_build_number
    def __generate_main_release_number(self, build_number=None):
        if build_number is None or build_number == "latest":
            release_number = self.__get_main_release_branches()[0]
            return release_number
        elif build_number is not None:
            number_list = build_number.split(".")
            number_list[-1] = "0"
            release_number = ".".join(number_list)
            return release_number


    @allure.step('Get specified udc build url: {build_number}-{pkg_type}')
    def get_specified_udc_build_url(self, build_number=None, pkg_type='privapp', env_type="test",
                                    build_type="release") -> tuple:
        """BaseAndroidFlow.get_specified_udc_build_url

        Get specified udc build url link

        Parameters
        ----------
        :param build_number: str, e.g: 23.08.0.11
        :param pkg_type: str, e.g: privapp, genericapp
        :param env_type: str, e.g: test, prod
        :param build_type: str, e.g: release, develop
        :return: tuple
        """
        log.info(f'Get udc {build_type} build url: {build_number}-{pkg_type}')

        if build_type == "release":
            main_release_number = self.__generate_main_release_number(build_number)
        else:
            main_release_number = build_number

        response = self.__get_udc_release_branch_info(main_release_number, build_type)
        target_build_number = self.__get_udc_target_build_number(response, build_number, pkg_type, env_type)

        if target_build_number is not None:
            return self.__get_build_url(response.url, target_build_number, pkg_type, env_type)
        else:
            response = self.__get_udc_release_branch_info("last", build_type)
            target_build_number = self.__get_udc_target_build_number(response, build_number, pkg_type, env_type)
            return self.__get_build_url(response.url, target_build_number, pkg_type, env_type)




    def __get_build_url(self, url, build_number, pkg_type, env_type="test"):
        release_type = "debug" if env_type == "test" else "release"
        url = parse.urljoin(url, build_number)
        url = f"{url}/{release_type}/{pkg_type}/signed"
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            log.error(f"File not found: {url}\n{response.text}")
            return None, None, None
        else:
            bs = BeautifulSoup(response.content.decode(), "html.parser")
            pkg_list = bs.find_all("a")
            apk_name = ""
            for pkg in pkg_list:
                apk_name = pkg.get("href").split("/")[0]
                if apk_name.endswith(".apk"):
                    break
            if apk_name != "":
                download_url = f"{url}/{apk_name}"
                log.info(download_url)
                version = apk_name.split('_')[-2].split('V')[1]
                return download_url, apk_name, version
            else:
                return None, None, None

    @allure.step('Get specified udc build')
    def get_specified_udc_build(self, build_number=None, pkg_type='privapp', env_type="test",build_type="release") -> tuple:
        """BaseAndroidFlow.get_specified_udc_build
        Get specified udc build, stored in \data\temp\ by default

        Parameters
        ----------
        :param build_number: str, e.g: 23.08.0.11
        :param pkg_type: str, e.g: privapp, genericapp
        :param env_type: str, e.g: test, prod
        :return: str， str
        """
        log.info("Get udc build")
        download_url, apk_name, version = self.get_specified_udc_build_url(build_number, pkg_type, env_type,build_type)
        if download_url is not None:
            download_path = get_temp_path(apk_name)
            if not os.path.isfile(download_path):
                log.info(f"Start to download: {apk_name}")
                response = requests.get(download_url, timeout=360)
                with open(download_path, 'wb') as f:
                    f.write(response.content)
                log.info(f"Finished Downloading: {apk_name}")
            return apk_name, version
        return None, None

    def get_specified_signed_system_app_build_from_temp(self, build_number=None, pkg_type='systemapp',
                                                        env_type="test") -> tuple:
        """BaseAndroidFlow.get_specified_udc_build

                Due to system app is not in CICD so we need to place build in temp folder manually
                Parameters
                ----------
                :param build_number: str, e.g: 23.08.0.11
                :param pkg_type: str, e.g: privapp, genericapp
                :param env_type: str, e.g: test, prod
                :return: str， str
                """
        env_type = 'debug' if env_type == 'test' else 'release'
        log.info('get UDC bulid from data/temp folder')
        if pkg_type == 'systemapp':
            pattern = r"^udc_android_{0}_{1}_V{2}_\d{{8}}_PICO_LEGACY\.apk$".format(pkg_type, env_type, build_number)
        else:
            pattern = r"^udc_android_{0}_{1}_V{2}_\d{{8}}.apk$".format(pkg_type, env_type, build_number)
        for root, dirs, files in os.walk(get_temp_path()):
            for file in files:
                match = re.match(pattern, file)
                if match:
                    return file, build_number
        raise FileNotFoundError("No matching APK found in temp folder.")

    def get_specified_platform_tsv_app_build_from_temp(self, build_number=None,pkg_type='platformapp', env_type="test")\
            -> tuple:
        """BaseAndroidFlow.get_specified_platform_tsv_app_build_from_temp

        Due to platform tsv app is not in CICD so we need to place build in temp folder manually
        Sample name :  udc_android_platformapp_debug_V24.01.0.9_20240122_TSV.apk
        Parameters
        ----------
        :param pkg_type: str, e.g: privapp, genericapp
        :param build_number: str, e.g: 24.01.0.9
        :param env_type: str, e.g: test, prod
        :return: str， str
        """
        env_type = 'debug' if env_type == 'test' else 'release'
        log.info(f'get {build_number} platform tsv app build from data/temp folder')
        pattern = r"^udc_android_{0}_{1}_V{2}_\d{{8}}_TSV\.apk$".format(pkg_type, env_type, build_number)
        log.info(f'{pattern}')
        for root, dirs, files in os.walk(get_temp_path()):
            for file in files:
                match = re.match(pattern, file)
                if match:
                    return file, build_number
        raise FileNotFoundError("No matching APK found in temp folder.")

    @allure.step('Launch UDC')
    def launch_udc(self, app_name="udc.lenovo.com.udclient") -> NoneType:
        """BaseAndroidFlow.launch_udc

        Launch UDC app

        Parameters
        ----------
        :param app_name: str
        :return: NoneType
        """
        if not len(self.main_po.get_app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
            if not len(self.main_po.get_app_list(app_name)):
                app_name = "com.lenovo.udcsystem"
        return self.main_po.launch_app(app_name)

    def splash_launch_udc(self):
        """BaseAndroidFlow.splash_launch_udc

        First Launch UDC app, only for private app

        Parameters
        ----------
        :return: NoneType
        """
        self.main_po.splash_launch_app()

    @allure.step('Get UDC Version')
    def get_udc_version(self, app_name="udc.lenovo.com.udclient") -> NoneType:
        """BaseAndroidFlow.get_udc_version

        Get UDC app version

        Parameters
        ----------
        :param app_name: str
        :return: NoneType
        """
        if not len(self.main_po.get_app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
            if not len(self.main_po.get_app_list(app_name)):
                app_name = "com.lenovo.udcsystem"
        return self.main_po.get_app_info(app_name).get("versionName")

    @allure.step('Install UDC via App path')
    def install_udc_via_path(self, build_number=None, pkg_type='privapp', env_type="test",build_type="release") -> Any:
        """BaseAndroidFlow.install_udc_via_path

        Install UDC via local apk file path

        Parameters
        ----------
        :param build_number: str
        :param pkg_type: str
        :param env_type: str
        :return: Any
        """
        apk_name, version = self.get_specified_udc_build(build_number, pkg_type, env_type,build_type)
        # apk_name, version = self.get_specified_signed_system_app_build_from_temp(build_number, pkg_type, env_type)
        self.udc_version = version
        app_path = get_temp_path(apk_name)
        install_result = self.main_po.install_app_via_path(app_path)
        os.environ['udc_version'] = self.get_udc_version()
        return install_result, apk_name, version

    @allure.step('Uninstall UDC')
    def uninstall_udc(self, app_name="udc.lenovo.com.udclient") -> bool:
        """BaseAndroidFlow.uninstall_udc

        Uninstall UDC

        Parameters
        ----------
        :param app_name: str, package name
        :return: bool
        """
        if not len(self.main_po.get_app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
        return self.main_po.uninstall_app(app_name)

    def uninstall_app(self, package_name) -> bool:
        """BaseAndroidFlow.uninstall_app

        Uninstall UDC

        Parameters
        ----------
        :param package_name: str, package name
        :return: bool
        """
        return self.main_po.uninstall_app(package_name)

    def clear_udc(self, app_name="udc.lenovo.com.udclient") -> NoneType:
        """BaseAndroidFlow.clear_udc

        Clear UDC

        Parameters
        ----------
        :return: NoneType
        """
        if not len(self.main_po.get_app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
            if not len(self.main_po.get_app_list(app_name)):
                app_name = "com.lenovo.udcsystem"
        return self.main_po.clear_app(app_name)

    def attach_png(self, png_file_name) -> str:
        """BaseAndroidFlow.attach_png

        Attach png file

        Parameters
        ----------
        :param png_file_name: str
        :return: str
        """
        return self.main_po.attach_screenshot(png_file_name)

    def open_settings(self):
        self.main_po.open_settings_page()

    def open_security_settings(self):
        self.main_po.open_security_settings_page()

    def clear_android_settings(self):
        self.main_po.clear_settings()

    def open_languages_settings(self):
        self.main_po.open_languages_settings_page()

    def open_date_time_settings(self):
        self.main_po.open_date_time_settings_page()

    def open_device_info_settings(self):
        self.main_po.open_device_info_settings_page()

    def change_language_to_en(self):
        self.open_languages_settings()
        self.android_languages_po.set_language_en()

    def change_language_to_en_for_mqtt(self):
        self.open_languages_settings()
        self.android_languages_po.set_language_en_for_mqtt()

    def change_language_to_zh(self):
        self.open_languages_settings()
        self.android_languages_po.set_language_zh()

    def change_timezone(self, region="Albania"):
        self.open_date_time_settings()
        self.android_datetime_settings_po.set_time_zone(region=region)

    def change_datetime_timezone_to_auto(self):
        self.open_date_time_settings()
        self.android_datetime_settings_po.set_datetime_timezone_auto()

    def get_timezone_value(self):
        self.home()
        self.open_date_time_settings()
        return self.android_datetime_settings_po.get_time_zone_value()

    def scroll_to_top(self):
        return self.main_po.scroll_to_top()

    def scroll_to_bottom(self):
        return self.main_po.scroll_to_bottom()

    def disable_wifi(self):
        return self.main_po.disable_wifi()

    def enable_wifi(self):
        return self.main_po.enable_wifi()

    def get_camera_client(self):
        return self.main_po.get_camera_client()

    def push_udc_provisioning_file(self, provisioning_file_path):
        self.main_po.push_file(provisioning_file_path, '/sdcard/Download/udc-provision.json')

    def match_image(self, image_path):
        return self.main_po.match_image(image_path)

    @allure.step('Deactivate Device admin app - udc')
    def deactivate_udc(self):
        self.clear_android_settings()
        self.open_security_settings()
        self.scroll_to_bottom()
        self.android_security_po.deactivate_admin_udc()

    def get_storage_free_percentage(self):
        self.open_settings()
        self.scroll_to_top()
        self.android_settings_po.swipe_to_setting_storage()
        storage_usage = self.android_settings_po.get_storage_usage()
        self.press_back()
        self.press_back()
        usage_percentage = storage_usage.split("%")[0].strip()
        return round(100 - float(usage_percentage))

    def change_device_name(self, origin_name="motorola edge X30", change_name="motorola edge X30"):
        self.open_device_info_settings()
        self.scroll_to_top()
        self.android_device_info_settings_po.scroll_to_device_name()
        time.sleep(3)
        exist = self.android_device_info_settings_po.exist_device_name()
        loop_count = 60
        while loop_count > 0 and not exist:
            self.open_device_info_settings()
            self.android_device_info_settings_po.scroll_to_device_name()
            exist = self.android_device_info_settings_po.exist_device_name()
            if exist:
                break
            time.sleep(0.5)
        if self.android_device_info_settings_po.exist_device_name():
            self.android_device_info_settings_po.change_device_name(origin_device_name=origin_name,
                                                                    change_device_name=change_name)

    def stop_udc(self, app_name="udc.lenovo.com.udclient"):
        if not len(self.main_po.get_app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
        return self.main_po.stop_app(app_name=app_name)

    def reboot(self):
        self.main_po.reboot()

    def get_language(self):
        return self.main_po.get_locale_language()
