#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: register_flow.py
@time: 8/22/2023 3:04 PM
@file_desc:
"""
import json
import logging
import os
import time
from typing import Any

import allure
import uiautomator2

from data.template.src.context import MqttType
from lcp_core_android.flows.base_mobile_flow import BaseAndroidFlow
from lcp_core_android.flows.atx_flow import AtxFlow
from lcp_core_android.library.constant.package import PRIV_APP
from lcp_core_android.library.constant.register import Register
from lcp_core_android.library.register_po import RegisterPo
from utils.file_helper import get_temp_path, get_cur_path, get_static_path
from utils.logger import allure_step_log

NoneType = type(None)
log = logging.getLogger(__name__)


class RegisterFlow(BaseAndroidFlow):
    def __init__(self, driver):
        super(RegisterFlow, self).__init__(driver)
        self.register_po = RegisterPo(driver)
        # self.udc_version = None

    def install_and_launch_udc(self, build_number, pkg_type='privapp', env_type="test", build_type="release") -> Any:
        """RegisterFlow.install_and_launch_udc

        Install udc and launch it

        Parameters
        ----------
        :param build_number: str, e.g: 23.08.0.11
        :param pkg_type: str, e.g: privapp, genericapp
        :param env_type: str, e.g: test, prod
        :return: Any
        """
        is_uninstall = self.uninstall_udc()
        log.info(f"Uninstall UDC: {is_uninstall}")
        # Install app via local apk file path
        log.info(f"Install UDC")
        res, apk_name, version = self.install_udc_via_path(build_number, pkg_type=pkg_type, env_type=env_type,build_type=build_type)
        log.info(f"Launch UDC")
        self.clear_udc()
        udc_version = self.get_udc_version()
        log.info(udc_version)
        # assert version in udc_version
        self.splash_launch_udc()
        self.launch_udc()
        self.udc_version = udc_version
        return self.udc_version

    def install_system_app_udc(self, build_number, pkg_type: str = 'systemapp', env_type="test"):
        """RegisterFlow.install_system app udc

               Install udc system flavor

               Parameters
               ----------
               :param build_number: str, e.g: 23.08.0.11
               :param pkg_type: str, e.g: systemapp
               :param env_type: str, e.g: test, prod
               :return: Any
               """
        self.clear_udc()
        log.info('Install UDC system app')
        apk_name, version = self.get_specified_signed_system_app_build_from_temp(build_number, pkg_type=pkg_type,
                                                                                 env_type=env_type)
        app_path = get_temp_path(apk_name)
        self.main_po.install_app_via_path(app_path)
        udc_version = self.get_udc_version()
        assert version in udc_version
        self.udc_version = udc_version
        return self.udc_version

    def install_platform_tsv_app_udc(self, build_number, pkg_type: str = 'platformapp', env_type="test"):
        """RegisterFlow.install_system app udc

               Install udc system flavor

               Parameters
               ----------
               :param build_number: str, e.g: 23.08.0.11
               :param pkg_type: str, e.g: systemapp
               :param env_type: str, e.g: test, prod
               :return: Any
               """
        log.info('Install UDC platform tsv app')
        apk_name, version = self.get_specified_platform_tsv_app_build_from_temp(build_number, pkg_type=pkg_type,
                                                                                env_type=env_type)
        app_path = get_temp_path(apk_name)
        self.main_po.install_app_via_path(app_path)
        udc_version = self.get_udc_version("com.lenovo.udcsystem")
        assert version in udc_version
        self.udc_version = udc_version
        return self.udc_version

    def install_test_app(self, apk_name):
        """RegisterFlow.install
            Install test app
        """
        app_path = get_static_path(apk_name)
        self.main_po.install_app_via_path(app_path)

    def check_udc_action_bar_exist(self):
        return self.register_po.register_config_page.check_action_bar_root_exist()

    def check_udc_action_bar_gone(self):
        return self.register_po.register_config_page.wait_action_bar_root_gone()

    def get_instruction_text(self):
        return self.register_po.register_config_page.get_instruction_text()

    # ------ Step 1 Begin ------#
    def goto_step1_udc_setup(self):
        self.register_po.register_config_page.click_step1_agreements_layout()

    def check_agreements_btn_enabled(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.get_agreements_btn_enabled_attr() \
            == "true"

    def get_agreements_btn_text(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.get_agreements_btn_text()

    def click_agreements_btn(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.click_agreements_btn()

    def check_step1_udc_setup_second_header_gone(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.check_agreements_second_header_gone()

    def check_tc_header_exist(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.tc.check_agreements_header_exist()

    def check_tc_header_gone(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.tc.check_agreements_header_gone()

    def click_tc_close_btn(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.tc.click_agreements_close_btn()

    def click_tc_accept_btn(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.tc.click_agreements_accept_btn()

    def check_tc_accept_btn_enabled(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.tc.get_agreements_accept_btn_enabled() \
            == "true"

    def check_pp_header_exist(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.pp.check_agreements_header_exist()

    def check_pp_header_gone(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.pp.check_agreements_header_gone()

    def click_pp_close_btn(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.pp.click_agreements_close_btn()

    def click_pp_accept_btn(self):
        return self.register_po.register_config_page.accept_privacy_and_tc_modal.pp.click_agreements_accept_btn()

    # ------ Step 1 End ------#

    # ------ Step 2 Begin ------#
    def goto_step2_device_admin(self):
        self.register_po.register_config_page.click_step2_device_admin_layout()

    def check_device_admin_btn_enabled(self):
        return self.register_po.register_config_page.enable_admin_permission_modal.get_device_admin_btn_enabled_attr() \
            == "true"

    def get_device_admin_btn_text(self):
        return self.register_po.register_config_page.enable_admin_permission_modal.get_device_admin_btn_text()

    def click_device_admin_btn(self):
        return self.register_po.register_config_page.enable_admin_permission_modal.click_device_admin_btn()

    def check_activate_device_admin_exist(self):
        return self.register_po.register_config_page.enable_admin_permission_modal.activate_device_admin_page.check_admin_name_exist()

    def check_activate_device_admin_gone(self):
        return self.register_po.register_config_page.enable_admin_permission_modal.activate_device_admin_page.check_content_frame_gone()

    def click_activate_device_admin_cancel(self):
        return self.register_po.register_config_page.enable_admin_permission_modal.activate_device_admin_page.click_cancel_btn()

    def click_activate_device_admin_activate(self):
        return self.register_po.register_config_page.enable_admin_permission_modal.activate_device_admin_page.click_action_btn()

    def check_step2_device_admin_second_header_gone(self):
        return self.register_po.register_config_page.enable_admin_permission_modal.check_device_admin_text_gone()

    # ------ Step 2 End ------#

    # ------ Step 3 Begin ------#
    def goto_step3_application_settings(self):
        self.register_po.register_config_page.click_step3_application_settings_layout()

    def check_app_permission_btn_enabled(self):
        return self.register_po.register_config_page.accept_app_permission_modal.get_app_permission_btn_enabled_attr() \
            == "true"

    def get_app_permission_btn_text(self):
        return self.register_po.register_config_page.accept_app_permission_modal.get_app_permission_btn_text()

    def click_app_permission_btn(self):
        return self.register_po.register_config_page.accept_app_permission_modal.click_app_permission_btn()

    def click_install_unknown_app_back_btn(self):
        return self.register_po.register_config_page.accept_app_permission_modal.install_unknown_app_page.click_navigate_up_btn()

    def accept_install_unknown_app(self):
        return self.register_po.register_config_page.accept_app_permission_modal.accept_install_unknown_app()

    def allow_and_change_to_access_location(self):
        return self.register_po.register_config_page.accept_app_permission_modal.allow_and_change_to_access_location()

    def allow_udc_display_over_other_apps(self):
        return self.register_po.register_config_page.accept_app_permission_modal.allow_udc_display_over_other_apps()

    def allow_udc_send_notification(self):
        if self.register_po.register_config_page.accept_app_permission_modal.check_app_permission_btn_exist():
            self.register_po.register_config_page.accept_app_permission_modal.click_app_permission_btn()
        return self.register_po.register_config_page.accept_app_permission_modal.allow_udc_send_notification()

    def check_step3_app_settings_detail_gone(self):
        return self.register_po.register_config_page.accept_app_permission_modal.check_app_settings_details_gone()

    # ------ Step 3 End ------#

    # ------ Step 4 Begin ------#
    def goto_step4_get_provision_files(self):
        self.register_po.register_config_page.click_step4_get_provision_files()

    def check_download_config_link_exist(self):
        return self.register_po.register_config_page.get_provision_file_modal.check_download_config_link_exist()

    def click_download_config_link(self):
        return self.register_po.register_config_page.get_provision_file_modal.click_download_config_link()

    def click_qrcode_scan_btn(self):
        return self.register_po.register_config_page.get_provision_file_modal.click_qrcode_scan_btn()

    def check_qrcode_scan_btn_exist(self):
        return self.register_po.register_config_page.get_provision_file_modal.check_qrcode_scan_btn_exist()

    def check_open_camera_grant_dialog_exist(self):
        return self.register_po.register_config_page.get_provision_file_modal.allow_to_open_camera_modal.check_grant_dialog_exist()

    def click_allow_open_camera_in_use_time(self):
        self.register_po.register_config_page.get_provision_file_modal.allow_to_open_camera_modal.click_allow_foreground_only_btn()

    def check_qrcode_scan_btn_enabled(self):
        return self.register_po.register_config_page.get_provision_file_modal.get_qrcode_scan_btn_enabled_attr() \
            == "true"

    def check_file_browser_btn_exist(self):
        return self.register_po.register_config_page.get_provision_file_modal.check_file_browser_btn_exist()

    def click_file_browser_btn(self):
        return self.register_po.register_config_page.get_provision_file_modal.click_file_browser_btn()

    def check_file_browser_page_exist(self):
        return self.register_po.register_config_page.get_provision_file_modal.file_browser_page.check_file_browser_page_exist()

    def choose_udc_provision_json_file(self):
        return self.register_po.register_config_page.get_provision_file_modal.choose_udc_provision_json_file()

    def file_browser_set_udc_provision_json_file(self):
        return self.register_po.register_config_page.get_provision_file_modal.file_browser_set_udc_provision_json_file()

    def check_confirm_dialog_exist(self):
        return self.register_po.register_config_page.check_confirm_dialog_exist()

    def get_confirm_title(self):
        return self.register_po.register_config_page.confirm_modal.get_confirm_title()

    def click_confirm_btn(self):
        return self.register_po.register_config_page.confirm_modal.click_confirm_btn()

    def get_confirm_dialog_info(self):
        return self.register_po.register_config_page.get_confirm_dialog_info()

    def check_step4_provision_details_gone(self):
        return self.register_po.register_config_page.get_provision_file_modal.check_provision_details_gone()

    # ------ Step 4 End ------#

    # ------ Bottom Section Begin ------#

    def check_bottom_section_exist(self):
        return self.register_po.register_config_page.check_bottom_section_exist()

    def get_check_for_updates_btn_text(self):
        return self.register_po.register_config_page.bottom_section_modal.get_check_for_updates_btn_text()

    def get_udc_version_on_app(self):
        return self.register_po.register_config_page.bottom_section_modal.get_udc_version()

    def check_open_source_license_link_exist(self):
        return self.register_po.register_config_page.bottom_section_modal.check_open_source_license_link_exist()

    def click_open_source_license_link(self):
        return self.register_po.register_config_page.bottom_section_modal.click_open_source_license_link()

    def check_open_source_license_header_exist(self):
        return self.register_po.register_config_page.bottom_section_modal.open_source_license_page.check_licenses_header_exist()

    def click_open_source_license_close_button(self):
        return self.register_po.register_config_page.bottom_section_modal.open_source_license_page.click_close_button()

    # ------ Bottom Section End ------#

    def allow_enable_bluetooth(self):
        return self.register_po.allow_bluetooth_modal.click_allow_btn()

    def try_allow_enable_bluetooth(self):
        try:
            self.register_po.allow_bluetooth_modal.click_allow_btn()
        except uiautomator2.exceptions.UiObjectNotFoundError:
            log.info('No allow bluetooth button clickable')
            pass

    @allure.step('Claim Device')
    def claim_device(self, build_number=None, pkg_type='privapp', config_type="manual", env_type="test", build_type="release") -> Any:
        """RegisterFlow.claim_device

        Claim Device

        Parameters
        ----------
        :param build_number: str, e.g: 23.08.0.11
        :param pkg_type: str, e.g: privapp, genericapp
        :param config_type: str, e.g: manual, qrCode
        :param env_type: str, e.g: test, prod
        :return: Any
        """
        self.install_and_launch_udc(build_number, pkg_type, env_type,build_type)

        with allure_step_log("Configure Device"):
            if config_type.lower() == "manual":
                return self.register_po.register_with_provision_file()
            else:
                return self.register_po.register_with_qrcode()

    @allure.step('Claim Device')
    def claim_device_via_atx(self, stf_flow: AtxFlow, release_number, build_number, pkg_type='privapp',
                             config_type="manual") -> dict:
        """RegisterFlow.claim_device_via_stf

        Claim Device with using ATX install app

        :param stf_flow: AtxFlow
        :param release_number: str, e.g: release-23.08.0.0
        :param build_number: str, e.g: 11-23.08.0.11
        :param pkg_type: str, e.g: privapp, genericapp
        :param config_type: str, e.g: manual, qrCode
        :return: dict
        """
        is_uninstall = self.uninstall_udc()
        log.info(f"Uninstall UDC: {is_uninstall}")
        udc_build_url, apk_name, version = self.get_specified_udc_build_url(release_number, build_number,
                                                                            pkg_type=pkg_type)
        # Install app via ATX
        install_udc = stf_flow.install_app(udc_build_url)
        log.info(f"Install UDC: {install_udc}")
        log.info(f"Launch UDC")
        self.clear_udc(install_udc['packageName'])
        udc_version = self.get_udc_version(install_udc['packageName'])
        assert udc_version == version
        self.launch_udc(install_udc['packageName'])
        with allure_step_log("Configure Device"):
            if config_type.lower() == "manual":
                return self.register_po.register_with_provision_file()
            else:
                return self.register_po.register_with_qrcode()

    @staticmethod
    def replace_provision_bridgepolicy_with_diff_mqtt_type(request, mqtt_type: str = 'XCC'):
        project_path = get_cur_path()
        test_env = request.config.getoption("--profile")
        signed_bcp_filename = test_env + f'_{mqtt_type}_bridgepolicy.signed'
        signed_bcp_filepath = os.path.join(project_path, 'data', 'static', signed_bcp_filename)
        provision_file_path = get_temp_path('udc-provision.json')

        with open(signed_bcp_filepath, 'r', encoding='utf-8') as f1:
            signed_bcp_payload = f1.read()

        with open(provision_file_path, 'r', encoding='utf-8') as f2:
            provision_data = json.load(f2)
            provision_data["bridge_config_policy"] = signed_bcp_payload
        modified_provision_filepath = get_temp_path(f'{mqtt_type}_udc_provision.json')
        with open(modified_provision_filepath, 'w', encoding='utf-8') as f:
            json.dump(provision_data, f)
        return modified_provision_filepath

    @staticmethod
    def replace_provision_with_diff_device_auth_type(request, device_auth_type: str = 'XCC'):
        project_path = get_cur_path()
        test_env = request.config.getoption("--profile")
        signed_config_filename = test_env + f'_{device_auth_type}_configpolicy.signed'
        signed_config_filepath = os.path.join(project_path, 'data', 'static', signed_config_filename)
        provision_file_path = get_temp_path('udc-provision.json')

        with open(signed_config_filepath, 'r', encoding='utf-8') as f1:
            signed_config_payload = f1.read()

        with open(provision_file_path, 'r', encoding='utf-8') as f2:
            provision_data = json.load(f2)
            provision_data["config_policy"] = signed_config_payload
        modified_provision_filepath = get_temp_path(f'{device_auth_type}_udc_provision.json')
        with open(modified_provision_filepath, 'w', encoding='utf-8') as f:
            json.dump(provision_data, f)
        return modified_provision_filepath

    @staticmethod
    def replace_provision_with_operational_event(request):
        project_path = get_cur_path()
        test_env = request.config.getoption("--profile")
        signed_config_filename = test_env + '_operational_config.signed'
        signed_config_filepath = os.path.join(project_path, 'data', 'static', signed_config_filename)
        provision_file_path = get_temp_path('udc-provision.json')

        with open(signed_config_filepath, 'r', encoding='utf-8') as f1:
            signed_config_payload = f1.read()

        with open(provision_file_path, 'r', encoding='utf-8') as f2:
            provision_data = json.load(f2)
            provision_data["config_policy"] = signed_config_payload
        modified_provision_filepath = get_temp_path(f'operational_config_udc_provision.json')
        with open(modified_provision_filepath, 'w', encoding='utf-8') as f:
            json.dump(provision_data, f)
        return modified_provision_filepath

    def register_with_diff_device_auth_type_config_in_provision(self, request, device_auth_type: str = 'MTLS'):
        modified_provision = self.replace_provision_with_diff_device_auth_type(request, device_auth_type)
        self.push_udc_provisioning_file(modified_provision)
        self.launch_udc()
        self.register_po.re_register_with_provision_or_qr_code()

    def register_with_operational_event_in_provision(self, request):
        modified_provision = self.replace_provision_with_operational_event(request)
        self.push_udc_provisioning_file(modified_provision)
        self.launch_udc()
        self.register_po.re_register_with_provision_or_qr_code()

    def register_fail_scenario_in_provision_flow(self, request, device_auth_type: str = 'MTLS'):
        modified_provision = self.replace_provision_with_diff_device_auth_type(request, device_auth_type)
        self.push_udc_provisioning_file(modified_provision)
        self.launch_udc()
        self.register_po.re_register_with_provision_or_qr_code()

    def register_with_diff_mqtt_type_in_provision(self, request, mqtt_type: str = MqttType.SSL):
        modified_provision = self.replace_provision_bridgepolicy_with_diff_mqtt_type(request, mqtt_type)
        self.push_udc_provisioning_file(modified_provision)
        self.launch_udc()
        self.register_po.re_register_with_provision_or_qr_code()

    def re_register_udc(self):
        """
        You need reset self.device_id after you re-register device successfully!
        """
        self.launch_udc()
        return self.register_po.re_register_with_provision_or_qr_code()

    def register_with_expired_provision_token(self):
        expired_provision_path = get_static_path('expired_provision.json')
        self.push_udc_provisioning_file(expired_provision_path)
        self.launch_udc()
        self.register_po.re_register_with_provision_or_qr_code()

    def push_expired_provision_token(self):
        expired_provision_path = get_static_path('expired_provision.json')
        self.push_udc_provisioning_file(expired_provision_path)

    def get_expired_provision_path(self):
        pass

    def register_with_private_app(self, build_number=None, env_type="test",build_type="release"):
        # Claim device
        with allure_step_log(f"Deactivate Admin app - UDC"):
            self.deactivate_udc()

        with allure_step_log(f"Register Device"):
            # Claim Device
            register_result = self.claim_device(build_number=build_number, env_type=env_type,build_type=build_type)
            assert register_result is not None
            assert register_result.get(
                "title") == self.register_constant.REGISTER_SUCCESS, register_result

    def register_with_platform_app(self, build_number=None, env_type="test",build_type="release"):
        # Claim device
        with allure_step_log(f"Deactivate Admin app - UDC"):
            self.deactivate_udc()

        with allure_step_log(f"Register Device"):
            # Claim Device
            register_result = self.claim_device(build_number=build_number,pkg_type='platformapp', env_type=env_type,build_type=build_type)
            assert register_result is not None
            assert register_result.get(
                "title") == self.register_constant.REGISTER_SUCCESS, register_result


    def register_with_system_app(self, build_number, pkg_type: str = 'systemapp', env_type="test"):
        # Claim device
        with allure_step_log(f"Register Device"):
            # systemapp without UI configuration
            register_result = self.install_system_app_udc(build_number, pkg_type, env_type)
            time.sleep(30)

    def register_with_platform_tsv_app(self, build_number, pkg_type: str = 'platformapp', env_type="test"):
        # Claim device
        with allure_step_log(f"Register Device"):
            # platform app tsv without UI configuration
            register_result = self.install_platform_tsv_app_udc(build_number, pkg_type, env_type)
            time.sleep(30)

    @property
    def register_constant(self):
        language = self.get_language()
        return Register(language=language).register

    def click_check_for_updates_btn_text(self):
        return self.register_po.register_config_page.bottom_section_modal.click_check_for_updates_btn()

    def check_no_updates_available_text(self):
        return self.register_po.register_config_page.bottom_section_modal.check_no_updates_available_btn()

    def check_processing_loading_text(self):
        return self.register_po.register_config_page.bottom_section_modal.check_processing_loading_icon()

    def wait_for_processing_loading_gone(self):
        return self.register_po.register_config_page.bottom_section_modal.wait_processing_loading_disappear()

    def check_for_updates(self):
        self.launch_udc()
        self.click_check_for_updates_btn_text()
        self.wait_for_processing_loading_gone()
