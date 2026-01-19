#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: atx_flow.py
@time: 8/23/2023 5:18 PM
@file_desc:
"""
import base64
import json
import logging
import os
import subprocess
import time
from pathlib import Path

import allure
import requests
import uiautomator2 as u2
import urllib3

from common.atx_client import AtxClient
from common.load_profile import LoadProfile
from common.u2_client import UiAutomator2Client
from data.template.smv2_relate import SMV2
from data.template.src.context import AppListRelate, ScanResultJson

from utils.file_helper import get_temp_path, create_folder, powershell_zip_file, delete_folder, get_static_path, \
    wait_until, compare_times

urllib3.disable_warnings()
NoneType = type(None)
log = logging.getLogger(__name__)


class AtxFlow:
    def __init__(self, udid, force=True):
        self.atx_client = AtxClient()
        self.udid = udid
        self.u2_driver = self.connect_usb(udid, force=force)
        self.u2_client = UiAutomator2Client(self.u2_driver)
        self.u2_client.ct_go_home()

    @allure.step('Get ATXServer user')
    def get_username(self) -> str:
        """AtxFlow.get_username

        Get current username

        Parameters
        ----------
        :return: str
        """
        _, ret = self.atx_client.request("/api/v1/user")
        log.info("User: %s", ret['username'])
        return ret['username']

    @allure.step('Get usable devices')
    def get_usable_devices(self) -> list:
        """AtxFlow.get_usable_devices

        Get usable devices list

        Parameters
        ----------
        :return: list
        """
        _, ret = self.atx_client.request("/api/v1/devices", params={"usable": "true"})
        if not ret['devices']:
            raise EnvironmentError("No devices")
        log.info("Devices: %s", ret['devices'])
        return ret['devices']

    @allure.step('Use device: {udid}')
    def use_device(self, udid, timeout=120) -> dict:
        """AtxFlow.use_device

        Use device

        Parameters
        ----------
        :param udid: str
        :param timeout: float
        :return: dict
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                _, ret = self.atx_client.request("/api/v1/user/devices",
                                                 method="post",
                                                 json={"udid": udid, "idleTimeout": 60000})
                log.info(ret)
                self.udid = udid
                break
            except Exception as error:
                log.warning(str(error))
                time.sleep(2)

        _, ret = self.atx_client.request("/api/v1/user/devices",
                                         method="post",
                                         json={"udid": udid})
        log.info(ret)
        self.udid = udid
        assert ret['success'], ret['description']
        return ret

    @allure.step('Release device from ATXServer')
    def release_device(self) -> dict:
        """AtxFlow.release_device

        Release device from ATXServer

        Parameters
        ----------
        :return: dict
        """
        _, ret = self.atx_client.request("/api/v1/user/devices/" + self.udid, method="delete")
        log.info(ret)
        assert ret['success'], ret['description']
        return ret

    @allure.step('Get device: {udid} info from ATXServer')
    def get_device_info_origin(self, udid) -> dict:
        """AtxFlow.get_device_info_origin

        Get original device info from ATXServer

        Parameters
        ----------
        :param udid: str
        :return: dict
        """
        _, ret = self.atx_client.request("/api/v1/user/devices/" + udid)
        log.info(ret)
        return ret

    def get_device_info(self, udid) -> dict:
        """AtxFlow.get_device_info

        Get device info from ATXServer

        Parameters
        ----------
        :param udid: str
        :return: dict
        """
        ret = self.get_device_info_origin(udid)
        log.info(ret['device'])
        return ret['device']

    def get_device_source(self, udid) -> dict:
        """AtxFlow.get_device_source

        Get device source info

        Parameters
        ----------
        :param udid: str
        :return: dict
        """
        device = self.get_device_info(udid)
        log.info(device['source'])
        return device['source']

    @allure.step('Install app: {apk_url} for device')
    def install_app(self, apk_url) -> dict:
        """AtxFlow.install_app

        Install app via url

        Parameters
        ----------
        :param apk_url: str
        :return: dict
        """
        source = self.get_device_source(self.udid)
        provider_url = source['url']
        log.info("install app")
        _, ret = self.atx_client.request(
            provider_url + "/app/install",
            method="post",
            params={"udid": self.udid},
            data={
                "url": apk_url,
                "launch": False
            })
        log.info(ret)
        assert ret['success'], ret['description']
        return ret

    @allure.step('Connect device: {udid} usb')
    def u2_connect_usb(self, udid, force=True) -> u2.Device:
        """AtxFlow.u2_connect_usb

        Uiautomtor2 connect device via usb

        Parameters
        ----------
        :param udid: str
        :param force: bool
        :return: Device
        """
        usable = False
        if not force:
            usable_devices = self.get_usable_devices()
            for device in usable_devices:
                if device.get("udid") == udid:
                    usable = True
                    break
        else:
            usable = True
        assert usable, f"No usable device: {udid}, the device maybe offline or in using."
        source = self.get_device_source(udid)
        adb_remote_addr = source['remoteConnectAddress']
        subprocess.run(['adb', 'connect', adb_remote_addr])
        time.sleep(1)
        driver = u2.connect_usb(adb_remote_addr)
        time.sleep(1)
        try:
            if not driver.uiautomator.running():
                driver.uiautomator.start()
                log.info(driver.uiautomator.running())
        except Exception as error:
            log.warning(str(error))
        log_folder = get_temp_path(udid)
        delete_folder(log_folder)
        # fuzzy_delete_file(str(Path(log_folder).parent), "zip")
        self.u2_driver = driver
        return driver

    @allure.step('Use and connect device: {udid}')
    def connect_usb(self, udid, force=True) -> u2.Device:
        """AtxFlow.connect_usb

        Use device and Connect device via usb

        Parameters
        ----------
        :param udid: str
        :param force: bool
        :return: Device
        """
        try:
            ret = self.use_device(udid)
            if ret['success']:
                return self.u2_connect_usb(udid, force=force)
        except Exception as error:
            log.warning(str(error))

    def __get_file_full_path_via_ls(self, ls_output):
        file_path_list = []
        folder_files_list = ls_output.split("\n\n")
        for folder_files in folder_files_list:
            parent_folder, files = folder_files.split(":")
            if files != "":
                sub_files = files.strip().split("\n")
                for sub_file in sub_files:
                    file_path_list.append(parent_folder + "/" + sub_file)
        return file_path_list

    def __remove_redundant_folder(self, file_path_list):
        n = len(file_path_list)
        need_delete_folder_list = []
        for i in range(n):
            for j in range(n):
                if file_path_list[i] in file_path_list[j] and file_path_list[i] != file_path_list[j]:
                    need_delete_folder_list.append(file_path_list[i])
        need_delete_folders = set(need_delete_folder_list)
        for delete_folder in need_delete_folders:
            file_path_list.remove(delete_folder)
        return file_path_list

    def pull_udc_files(self):
        """AtxFlow.pull_udc_files

        Get UDC logs from device

        Parameters
        ----------
        :return: str
        """
        local_log_folder = get_temp_path(self.udid)
        create_folder(local_log_folder)
        app_name = "udc.lenovo.com.udclient"
        if not len(self.u2_driver.app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
        base_folder = f"sdcard/Android/data/{app_name}"
        output, exit_code = self.u2_driver.shell(["ls", "-R", base_folder])
        file_path_list = self.__remove_redundant_folder(self.__get_file_full_path_via_ls(output))
        for file_path in file_path_list:
            output, exit_code = self.u2_driver.shell(["ls", "-R", file_path])
            if ":\n" not in output:
                target = file_path.replace(base_folder, local_log_folder).replace("/", "\\")
                parent, filename = os.path.split(target)
                if not os.path.exists(parent):
                    os.makedirs(parent)
                self.u2_driver.pull(file_path, os.path.join(local_log_folder, target))
        return local_log_folder

    @allure.step('Get UDC logs')
    def zip_and_link_udc_logs(self, project_name="udc") -> str:
        """AtxFlow.zip_and_link_udc_logs

        Get UDC logs from device

        Parameters
        ----------
        :return: str
        """
        local_log_folder = self.pull_udc_files()
        time_str = time.strftime("%Y-%m-%d_%H-%M-%S")
        zip_file_path = f"{local_log_folder}_{time_str}.zip"
        powershell_zip_file(local_log_folder, zip_file_path)
        zip_link = self.upload_udc_log_to_file_server(zip_file_path, folder_name=project_name.upper())
        log.info(zip_link)
        allure.dynamic.link(zip_link, name="UDC log")
        return zip_link

    @allure.step('Upload UDC logs to file server http://10.184.72.46:50998')
    def upload_udc_log_to_file_server(self, zip_file_path, folder_name="UDC"):
        """AtxFlow.upload_udc_log_to_file_server

        Upload UDC logs to file server http://10.184.72.46:50998
        Upload UDC logs to file server 10.184.72.29:50001

        Parameters
        ----------
        :param zip_file_path: str
        :param folder_name: str
        :return: str
        """
        s = requests.session()
        payload = {"folderName": folder_name}
        if str(Path(zip_file_path).parent) == ".":
            zip_file_name = zip_file_path
        else:
            zip_file_name = zip_file_path.split(str(Path(zip_file_path).parent))[1].replace("\\", "")
        files = [
            ('file', (zip_file_name, open(zip_file_path, 'rb'), 'application/zip'))
        ]

        # url = "http://10.184.72.43:21117/atm-api/fileService/uploadFile"
        url = "http://10.184.72.29:50001/atm-api/fileService/uploadFile"
        response = s.post(url, data=payload, files=files)
        if response.status_code == 200:
            return response.json().get("data")[0].get("fileLink")

    # @allure.step('Upload UDC logs to file server http://10.176.36.152:50001')
    # def upload_udc_log_to_file_server(self, zip_file_path):
    #     """AtxFlow.upload_udc_log_to_file_server
    #
    #     Upload UDC logs to file server http://10.176.36.152:50001
    #
    #     Parameters
    #     ----------
    #     :param zip_file_path: str
    #     :return: str
    #     """
    #     url = "http://10.176.36.152:50001/api/v1/login"
    #     payload = json.dumps({
    #         "accessKey": "minioadmin",
    #         "secretKey": "minioadmin"
    #     })
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    #         'Connection': 'keep-alive'
    #     }
    #
    #     s = requests.session()
    #     response = s.request("POST", url, headers=headers, data=payload)
    #     zip_file_name = zip_file_path.split(str(Path(zip_file_path).parent))[1].replace("\\", "")
    #     file_size = os.stat(zip_file_path).st_size
    #     files = [
    #         (str(file_size), (zip_file_name, open(zip_file_path, 'rb'), 'application/zip'))
    #     ]
    #
    #     url = "http://10.184.72.43:21117/atm-api/fileService/uploadFile"
    #     response = s.post(url, files=files)
    #     if response.status_code == 200:
    #         return f"http://10.176.36.152:50001/browser/udc/{zip_file_name}"

    def release(self, get_udc_log=True, project="UDC") -> dict:
        """AtxFlow.release

        Release device from ATXServer

        Parameters
        ----------
        :param get_udc_log: bool
        :param project: str
        :return: dict
        """
        try:
            if get_udc_log:
                self.zip_and_link_udc_logs(project_name=project)
        finally:
            try:
                if self.u2_driver.screenrecord._running:
                    self.u2_driver.screenrecord.stop()
            except Exception as error:
                pass
            self.set_security_settings_back()
            # Release the device
            return self.release_device()

    def set_security_settings_back(self):
        try:
            self.u2_client.ct_open_security_settings()
            self.u2_client.ct_press("back")
            self.u2_client.ct_press("back")
            self.u2_client.ct_press("back")
        except Exception as error:
            log.warning(str(error))

    @allure.step('Push udc provision file')
    def push_udc_provision_file(self) -> dict:
        """AtxFlow.push_udc_provision_file

        Push udc-provision.json to device

        Parameters
        ----------
        :return: dict
        """
        provision_path = get_temp_path('udc-provision.json')
        return self.u2_client.ct_push_file(provision_path, '/sdcard/Download/')

    @allure.step('Push signed message digest file')
    def push_message_digest_file(self, filename=SMV2.msg_digest) -> dict:
        """AtxFlow.push_message_digest_file

        Push signed message digest to device

        Parameters
        ----------
        :return: dict
        """
        digest_path = get_static_path(filename)
        return self.u2_client.ct_push_file(digest_path, '/sdcard/Download/')

    def push_udc_provision_file_under_sdcard(self) -> dict:
        """AtxFlow.push_udc_provision_file

        Push udc-provision.json to device

        Parameters
        ----------
        :return: dict
        """
        provision_path = get_temp_path('udc-provision.json')
        return self.u2_client.ct_push_file(provision_path, '/sdcard/')

    def push_udc_provision_file_under_platform_app(self) -> dict:
        """AtxFlow.push_udc_provision_file

        Push udc-provision.json to device

        Parameters
        ----------
        :return: dict
        """
        provision_path = get_temp_path('udc-provision.json')
        return self.u2_client.ct_push_file(provision_path, '/sdcard/Android/data/com.lenovo.udcsystem/files/udc-provision.json')

    def __wait_device_online(self, timeout=120):
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                self.u2_driver = self.connect_usb(self.udid)
                break
            except Exception as error:
                log.info(str(error))
                time.sleep(2)

    def wait_device_online(self):
        self.__wait_device_online()
        wait_online = True
        while wait_online:
            try:
                self.u2_client = UiAutomator2Client(self.u2_driver)
                self.u2_client.ct_go_home()
                wait_online = False
                break
            except Exception as error:
                log.info(str(error))
                self.__wait_device_online()

    @allure.step('Get udc running log')
    def get_udc_running_log(self, app_name="udc.lenovo.com.udclient") -> str:
        """AtxFlow.get_udc_running_log

        Get registered device UDC running log info

        Parameters
        ----------
        :return: str
        """
        log_file_name = "udc_running.log"
        self.wait_device_online()
        if not len(self.u2_driver.app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
        base_folder = f"sdcard/Android/data/{app_name}"
        udc_log_path = f"{base_folder}/files/UDCLog"
        output, exit_code = self.u2_client.ct_list_folder(udc_log_path)
        parent_folder = output.strip().split(":\n")[0]
        udc_running_log_folder = get_temp_path(self.udid)
        create_folder(udc_running_log_folder)
        self.u2_client.ct_pull_file(f"{parent_folder}/{log_file_name}",
                                    os.path.join(udc_running_log_folder, log_file_name))
        output, exit_code = self.u2_client.ct_cat_file(f"{parent_folder}/{log_file_name}")
        self.udc_running_log = output
        return output

    @allure.step('get scan-result.json')
    def get_udc_scan_result_json(self, app_name="udc.lenovo.com.udclient") -> str:
        """AtxFlow.get_udc_scan_result_json
        Get registered device UDC applist info
        Parameters
        ----------
        :return: str
        """
        log_file_name = ScanResultJson.SCAN_RESULT_JSON
        parent_folder = ''
        self.wait_device_online()
        if not len(self.u2_driver.app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
        base_folder = f"sdcard/Android/data/{app_name}"
        udc_log_path = f"{base_folder}/files/UDCLog/Diagnostics/Latest"
        output, exit_code = self.u2_client.ct_list_folder(udc_log_path)
        try:
            parent_folder = output.strip().split(":\n")[0]
        except ValueError as e:
            log.error('No scan-result.json in UDC folder')
        udc_running_log_folder = get_temp_path(self.udid)
        create_folder(udc_running_log_folder)
        self.u2_client.ct_pull_file(f"{parent_folder}/{log_file_name}",
                                    os.path.join(udc_running_log_folder, log_file_name))
        output, exit_code = self.u2_client.ct_cat_file(f"{parent_folder}/{log_file_name}")
        self.scan_result_json = output
        log.info(output)
        return output
    @allure.step('Get udc applist')
    def get_udc_applist(self, app_name="udc.lenovo.com.udclient") -> str:
        """AtxFlow.get_udc_applist

        Get registered device UDC applist info

        Parameters
        ----------
        :return: str
        """
        log_file_name = AppListRelate.APPLIST_FILE_NAME
        parent_folder = ''
        self.wait_device_online()
        if not len(self.u2_driver.app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
        base_folder = f"sdcard/Android/data/{app_name}"
        udc_log_path = f"{base_folder}/files"
        output, exit_code = self.u2_client.ct_list_folder(udc_log_path)
        try:
            parent_folder = output.strip().split(":\n")[0]
        except ValueError as e:
            log.error('No Applist in UDC folder')
        udc_running_log_folder = get_temp_path(self.udid)
        create_folder(udc_running_log_folder)
        self.u2_client.ct_pull_file(f"{parent_folder}/{log_file_name}",
                                    os.path.join(udc_running_log_folder, log_file_name))
        output, exit_code = self.u2_client.ct_cat_file(f"{parent_folder}/{log_file_name}")
        self.applist = output
        log.info(output)
        return output

    @allure.step('Get udc applist sync time')
    def get_udc_applist_synctime(self, app_name="udc.lenovo.com.udclient") -> str:
        """AtxFlow.get_udc_applist

        Get registered device UDC applist info

        Parameters
        ----------
        :return: str
        """
        log_file_name = AppListRelate.APP_SYNC_TIME_FILE_NAME
        parent_folder = ''
        self.wait_device_online()
        if not len(self.u2_driver.app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
        base_folder = f"sdcard/Android/data/{app_name}"
        udc_log_path = f"{base_folder}/files"
        output, exit_code = self.u2_client.ct_list_folder(udc_log_path)
        try:
            parent_folder = output.strip().split(":\n")[0]
        except ValueError as e:
            log.error('No Applist sync time in UDC folder')
        udc_running_log_folder = get_temp_path(self.udid)
        create_folder(udc_running_log_folder)
        self.u2_client.ct_pull_file(f"{parent_folder}/{log_file_name}",
                                    os.path.join(udc_running_log_folder, log_file_name))
        output, exit_code = self.u2_client.ct_cat_file(f"{parent_folder}/{log_file_name}")
        self.app_sync_time = output
        return output

    @allure.step('Get udc running in system app')
    def get_udc_running_log_in_system_app(self) -> str:
        """AtxFlow.get_udc_running_log

        Get registered device UDC running log info

        Parameters
        ----------
        :return: str
        """
        log_file_name = "udc_running.log"
        self.wait_device_online()
        base_folder = f"sdcard/UDCLog"
        udc_log_path = f"{base_folder}"
        output, exit_code = self.u2_client.ct_list_folder(udc_log_path)
        parent_folder = output.strip().split(":\n")[0]
        udc_running_log_folder = get_temp_path(self.udid)
        create_folder(udc_running_log_folder)
        self.u2_client.ct_pull_file(f"{base_folder}/{log_file_name}",
                                    os.path.join(udc_running_log_folder, log_file_name))
        output, exit_code = self.u2_client.ct_cat_file(f"{parent_folder}/{log_file_name}")
        self.udc_running_log = output
        return output

    @allure.step('Get udc core log in system app')
    def get_core_log_in_system_app(self) -> str:
        """AtxFlow.get_udc_running_log

        Get registered device UDC core log info

        Parameters
        ----------
        :return: str
        """
        log_file_name = "CoreLog"
        self.wait_device_online()
        app_name = "udc.lenovo.com.udclient"
        base_folder = f"sdcard/Android/data"
        udc_log_path = f'{base_folder}/{app_name}/files/udclog'
        output, exit_code = self.u2_client.ct_list_folder(udc_log_path)
        parent_folder = output.strip().split(":\n")[0]
        udc_core_log_folder = get_temp_path(self.udid)
        create_folder(udc_core_log_folder)
        self.u2_client.ct_pull_file(f"{parent_folder}/{log_file_name}",
                                    os.path.join(udc_core_log_folder, log_file_name))
        output, exit_code = self.u2_client.ct_cat_file(f"{parent_folder}/{log_file_name}")
        self.udc_core_log = output
        return output

    @allure.step('Get udc core log in platform app')
    def get_core_log_in_platform_app(self) -> str:
        """AtxFlow.get_core_log_in_generic_or_private_app

        Get registered device UDC core log info

        Parameters
        ----------
        :return: str
        """
        log_file_name = "Corelog"
        self.wait_device_online()
        app_name = "com.lenovo.udcsystem"
        if not len(self.u2_driver.app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
        base_folder = f"sdcard/Android/data/{app_name}"
        udc_log_path = f"{base_folder}/files/UDCLog"
        output, exit_code = self.u2_client.ct_list_folder(udc_log_path)
        parent_folder = output.strip().split(":\n")[0]
        udc_core_log_folder = get_temp_path(self.udid)
        create_folder(udc_core_log_folder)
        self.u2_client.ct_pull_file(f"{parent_folder}/{log_file_name}",
                                    os.path.join(udc_core_log_folder, log_file_name))
        output, exit_code = self.u2_client.ct_cat_file(f"{parent_folder}/{log_file_name}")
        self.udc_core_log = output
        return output

    @allure.step('Get udc core log in system app')
    def get_core_log_in_generic_or_private_app(self) -> str:
        """AtxFlow.get_core_log_in_generic_or_private_app

        Get registered device UDC core log info

        Parameters
        ----------
        :return: str
        """
        log_file_name = "Corelog"
        self.wait_device_online()
        app_name = "udc.lenovo.com.udclient"
        if not len(self.u2_driver.app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
        base_folder = f"sdcard/Android/data/{app_name}"
        udc_log_path = f"{base_folder}/files/UDCLog"
        output, exit_code = self.u2_client.ct_list_folder(udc_log_path)
        parent_folder = output.strip().split(":\n")[0]
        udc_core_log_folder = get_temp_path(self.udid)
        create_folder(udc_core_log_folder)
        self.u2_client.ct_pull_file(f"{parent_folder}/{log_file_name}",
                                    os.path.join(udc_core_log_folder, log_file_name))
        output, exit_code = self.u2_client.ct_cat_file(f"{parent_folder}/{log_file_name}")
        self.udc_core_log = output
        return output

    @allure.step("Read udc running log to lines")
    def read_running_log_to_lines(self) -> list:
        udc_running_log_folder = get_temp_path(self.udid)
        udc_running_log_path = os.path.join(udc_running_log_folder, "udc_running.log")
        self.get_udc_running_log()
        with open(udc_running_log_path, "r", encoding="utf-8") as file_handle:
            return file_handle.readlines()

    @allure.step('Get udc info')
    def get_udc_info(self, app_name="udc.lenovo.com.udclient") -> dict:
        """AtxFlow.get_udc_info
        It is suitable for generic app or private app
        Get registered device UDC info from json file

        Parameters
        ----------
        :return: dict
        """
        if not len(self.u2_driver.app_list(app_name)):
            app_name = "com.lenovo.udcplatform"
            if not len(self.u2_driver.app_list(app_name)):
                app_name = "com.lenovo.udcsystem"
        base_folder = f"sdcard/Android/data/{app_name}"
        udc_info_path = f"{base_folder}/files/UDCInfo"
        output, exit_code = self.u2_client.ct_list_folder(udc_info_path)
        parent_folder, json_file = output.strip().split(":\n")
        output, exit_code = self.u2_client.ct_cat_file(f"{parent_folder}/{json_file}")
        log.info(output)
        udc_info = json.loads(output)
        return udc_info

    @allure.step('Get generic app android id')
    def get_android_id(self) -> str:
        try:
            android_id = self.get_udc_info()["android_id"]
            return android_id
        except ValueError as e:
            log.error(e)
            log.error('Can not get the android id')

    @allure.step('Get udc info')
    def get_udc_info_for_system_app(self) -> dict:
        """AtxFlow.get_udc_info
        It is suitable for system app
        Get registered device UDC info from json file

        Parameters
        ----------
        :return: dict
        """

        base_folder = "sdcard/udcinfo"

        output, exit_code = self.u2_client.ct_list_folder(base_folder)
        json_file = output.strip().split(":\n")[1]
        output, exit_code = self.u2_client.ct_cat_file(f"{base_folder}/{json_file}")
        log.info(output)
        udc_core_log_folder = get_temp_path(self.udid)
        create_folder(udc_core_log_folder)
        self.u2_client.ct_pull_file(f"{base_folder}/{json_file}",
                                    os.path.join(udc_core_log_folder, json_file))
        udc_info = json.loads(output)
        return udc_info

    @allure.step('Get registered device sn')
    def get_solution_sn(self) -> str:
        """AtxFlow.get_solution_sn

        Get registered device sn via UDC info

        Parameters
        ----------
        :return: str
        """
        udc_info = self.get_udc_info()
        sn = udc_info.get("sn")
        if sn == "":
            sn = udc_info.get("android_id")
        return sn

    @allure.step('Get registered device id')
    def get_solution_device_id(self, app_name="udc.lenovo.com.udclient") -> str:
        """AtxFlow.get_solution_device_id

        Get registered device id via UDC info

        Parameters
        ----------
        :return: str
        """
        udc_info = self.get_udc_info(app_name)
        return udc_info.get("device_id")

    @allure.step('Get registered device id')
    def get_solution_device_id_for_system_app(self) -> str:
        """AtxFlow.get_solution_device_id

        Get registered device id via UDC info

        Parameters
        ----------
        :return: str
        """
        udc_info = self.get_udc_info_for_system_app()
        return udc_info.get("device_id")

    def reboot(self):
        self.u2_client.ct_reboot()
        self.wait_device_online()

    @property
    def model(self):
        return self.u2_client.ct_model()

    def clean_udc_log_for_system_app(self):
        """
            We need use adb shell rm to clean sdcard/udclog to make sure
            the log is clean
        """
        log.info('cleaning udc running log folder')
        self.u2_client.ct_shell(["pm", "clear", 'udc.lenovo.com.udclient'])
        output, exitcode = self.u2_client.ct_clean_folder(f'sdcard/UDCLog')
        log.info(f"clean status: {output}")

    def clean_udc_log_for_platform_app(self):
        """
            We need use adb shell rm to clean sdcard/udclog to make sure
            the log is clean
        """
        log.info('cleaning udc running log folder')
        self.u2_client.ct_shell(["pm", "clear", 'com.lenovo.udcsystem'])

    def set_oem_url_for_zdu(self, oem_url: str):
        log.info(f'Set oem url as {oem_url}')
        return self.u2_client.ct_shell(["setprop","persist.debug.udc.oem_default_config_url", oem_url])

    def check_sync_status_for_db(self,regex, timeout=120):
        from udc.flows.udc_flow import check_match_log_in_log
        log.info(f'check sync status for regex {regex}')
        sync_success_regex = ".*DEBUG-NrtEventSyncCallback : Event Data:"
        sync_point_regex = sync_success_regex + regex
        log.info(sync_point_regex)
        result = wait_until(lambda: check_match_log_in_log(sync_point_regex,self.get_udc_running_log(), False),period=3,timeout=timeout)
        assert result, 'Sync success log not found'

    def check_db_collection_collected_since(self, regex, since, timeout=60):
        from udc.flows.udc_flow import catch_match_log_in_logs
        result = wait_until(lambda: compare_times(catch_match_log_in_logs(regex,self.get_udc_running_log()).get('item_time'),since),period=3,timeout=timeout)
        return catch_match_log_in_logs(regex,self.get_udc_running_log())

CONF = LoadProfile()


class LdmFlow:
    def __init__(self, username, password, org_id):
        self.username = username
        self.password = password
        self.org_id = org_id
        url = f"{CONF.AUTH_SERVER}/auth/realms/{org_id}/protocol/openid-connect/token"
        form_data = {
            'username': self.username,
            'password': self.password,
            'client_id': self.org_id,
            'grant_type': "password",
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'KEYCLOAK_LOCALE=en'
        }
        response = requests.request("POST", url, headers=headers, data=form_data)
        self.access_token = response.json().get("access_token")

    def get_qr_code(self):
        url = f"{CONF.TEST_SERVER}/core/installer-service/v1/installers"
        payload = json.dumps({
            "expirationTimeInDays": 1,
            "maxUsageLimit": 1000,
            "platform": "android",
            "packageType": "JSON"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        installer_id = response.json().get("id")
        log.info(installer_id)

        url = f"{CONF.TEST_SERVER}/core/installer-service/v1/installers/{installer_id}/device-owner?size=500&format=PNG"
        payload = ""
        response = requests.request("GET", url, headers=headers, data=payload)
        qr_code = response.json().get("qrCode")
        qr_code_png = get_temp_path("qrCode.png")
        with open(qr_code_png, 'wb') as png_file:
            png_file.write(base64.b64decode(qr_code))
        return qr_code_png


class GeminiFlow:
    def __init__(self, token):
        self.access_token = token

    def get_qr_code(self):
        url = f"{CONF.TEST_SERVER}/core/installer-service/v1/installers"
        payload = json.dumps({
            "expirationTimeInDays": 1,
            "maxUsageLimit": 1000,
            "name": "Installer_1750385002541",
            "platform": "android",
            "packageType": "JSON"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{self.access_token}',
            'X-Subscription': 'aa653038-614c-4635-b419-6171811e7edf'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        log.info(f"payload ==> {payload}")
        log.info(f"response ==> {response.json()}")
        installer_id = response.json().get("id")
        log.info(installer_id)

        url = f"{CONF.TEST_SERVER}/core/installer-service/v1/installers/{installer_id}/device-owner?size=500&format=PNG"
        payload = ""
        response = requests.request("GET", url, headers=headers, data=payload)
        qr_code = response.json().get("qrCode")
        qr_code_png = get_temp_path("qrCode.png")
        with open(qr_code_png, 'wb') as png_file:
            png_file.write(base64.b64decode(qr_code))
        return qr_code_png
