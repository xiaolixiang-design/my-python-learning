#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: register_po.py
@time: 8/21/2023 4:28 PM
@file_desc:
"""
import logging
import time

from uiautomator2 import Device

from common.u2_client import AndroidElement
from lcp_core_android.library.base_page import BasePage
from lcp_core_android.library.components.allow_permission_modal import AllowPermissionModal
from lcp_core_android.library.components.confirm_modal import ConfirmModal
from utils.file_helper import sleep
from utils.logger import allure_step_log

NoneType = type(None)
log = logging.getLogger(__name__)


class RegisterPo:
    def __init__(self, driver: Device):
        self.register_config_page = RegistrationAndConfigurationPage(driver)
        self.allow_bluetooth_modal = AllowToEnableBluetoothModal(driver)
        self.allow_location_permission_model  = AllowToAccessLocationModal(driver)
    def register_with_provision_file(self) -> dict:
        """RegisterPo.register_with_provision_file

        Register with provisioning file

        Parameters
        ----------
        :return: dict
        """
        return self.register_with_provision_or_qr_code()

    def register_with_qrcode(self) -> dict:
        """RegisterPo.register_with_qrcode

        Register with QR code

        Parameters
        ----------
        :return: dict
        """
        return self.register_with_provision_or_qr_code(register_type="qrcode")

    def register_with_provision_or_qr_code(self, register_type="provision") -> dict:
        """RegisterPo.register_with_provision_or_qr_code

        Register with QR code

        Parameters
        ----------
        :return: dict
        """
        with allure_step_log("STEP1: UDC SETUP - Accept UDC Privacy and Terms & Conditions."):
            self.register_config_page.accept_udc_tc_an_pp()
        with allure_step_log("STEP2: PERMISSIONS - Enable admin permissions"):
            time.sleep(0.5)
            self.register_config_page.ct_scroll_to_top()
            self.register_config_page.enable_device_admin_permission()
        with allure_step_log("STEP3: PERMISSIONS - Accept application permissions"):
            self.register_config_page.accept_application_permissions()
        if register_type == "provision":
            with allure_step_log("STEP4: GET PROVISIONING FILE - Download configuration file"):
                self.register_config_page.set_provision_file()
        elif register_type == "qrcode":
            with allure_step_log("STEP4: GET PROVISIONING FILE - Scan QR Code"):
                self.register_config_page.scan_qr_code()
        with allure_step_log("Wait for Confirm Dialog"):
            # self.register_config_page.wait_loading_disappear()
            # disable this wait to make sure it can click allow location permission
            sleep(15)
            log.info('wait for location permission launch')
            self.allow_location_permission_model.click_allow_location_permission_btn()
            return self.register_config_page.get_confirm_dialog_info()

    def accept_agreement_and_enable_admin(self):
        with allure_step_log("STEP1: UDC SETUP - Accept UDC Privacy and Terms & Conditions."):
            self.register_config_page.accept_udc_tc_an_pp()
        with allure_step_log("STEP2: PERMISSIONS - Enable admin permissions"):
            time.sleep(0.5)
            self.register_config_page.ct_scroll_to_top()
            self.register_config_page.enable_device_admin_permission()
        with allure_step_log("STEP3: PERMISSIONS - Accept application permissions"):
            self.register_config_page.accept_application_permissions()

    def re_register_with_provision_or_qr_code(self, register_type="provision") -> dict:
        """RegisterPo.register_with_provision_or_qr_code

        Register with QR code

        Parameters
        ----------
        :return: dict
        """
        with allure_step_log("STEP1: UDC SETUP - Accept UDC Privacy and Terms & Conditions."):
            self.register_config_page.accept_udc_tc_an_pp()
        with allure_step_log("STEP3: PERMISSIONS - Accept application permissions"):
            self.register_config_page.accept_application_permissions()
        if register_type == "provision":
            with allure_step_log("STEP4: GET PROVISIONING FILE - Download configuration file"):
                self.register_config_page.set_provision_file()
        elif register_type == "qrcode":
            with allure_step_log("STEP4: GET PROVISIONING FILE - Scan QR Code"):
                self.register_config_page.scan_qr_code()
        with allure_step_log("Wait for Confirm Dialog"):
            # self.register_config_page.wait_loading_disappear()
            log.info('wait for location permission launch')
            sleep(15)
            self.allow_location_permission_model.click_allow_location_permission_btn()
            return self.register_config_page.get_confirm_dialog_info()


class RegistrationAndConfigurationPage(BasePage):
    action_bar_root = AndroidElement('xpath',
                                     '//android.widget.LinearLayout[contains(@resource-id, "action_bar_root")]')
    instruction_header_text = AndroidElement('xpath',
                                             '//android.widget.TextView[contains(@resource-id, "instructionHeaderTextView")]')
    step1_agreements_layout = AndroidElement('xpath',
                                             '//android.widget.LinearLayout[contains(@resource-id, "step1_agreementsLayout")]')
    step2_device_admin_layout = AndroidElement('xpath',
                                               '//android.widget.LinearLayout[contains(@resource-id, "step2_deviceAdminLayout")]')
    step3_application_settings_layout = AndroidElement('xpath',
                                                       '//android.widget.LinearLayout[contains(@resource-id, "step3_applicationSettingsLayout")]')
    step4_get_provision_files = AndroidElement('xpath',
                                               '//android.widget.LinearLayout[contains(@resource-id, "step4_getProvisionFiles")]')

    bottom_section = AndroidElement('xpath', '//android.widget.LinearLayout[contains(@resource-id, "bottom_section")]')

    def __init__(self, driver: Device):
        super(RegistrationAndConfigurationPage, self).__init__(driver)
        self.accept_privacy_and_tc_modal = self.AcceptPrivacyAndTermsConditions(driver)
        self.enable_admin_permission_modal = self.EnableAdminPermissions(driver)
        self.accept_app_permission_modal = self.AcceptAppPermissions(driver)
        self.get_provision_file_modal = self.GetProvisioningFiles(driver)
        self.confirm_modal = ConfirmModal(driver)
        self.bottom_section_modal = self.BottomSection(driver)

    def check_bottom_section_exist(self) -> bool:
        """RegistrationAndConfigurationPage.check_bottom_section_exist

        Check bottom_section exist or not

        Parameters
        ----------
        :return: bool
        """
        return self.ct_wait_exist(self.bottom_section, timeout=3)

    def check_action_bar_root_exist(self) -> bool:
        """RegistrationAndConfigurationPage.check_action_bar_root_exist

        Check action_bar_root exist or not

        Parameters
        ----------
        :return: bool
        """
        return self.ct_wait_exist(self.action_bar_root, timeout=10)

    def wait_action_bar_root_gone(self) -> bool:
        """RegistrationAndConfigurationPage.wait_action_bar_root_gone

        Wait agreements_second_header_text disappear

        Parameters
        ----------
        :return: bool
        """
        return self.ct_wait_disappear(self.action_bar_root, timeout=5)

    def get_instruction_text(self):
        """RegistrationAndConfigurationPage.get_instruction_text

        Get instruction_header_text

        Parameters
        ----------
        :return: str
        """
        return self.ct_get_text(self.instruction_header_text)

    def click_step1_agreements_layout(self):
        """RegistrationAndConfigurationPage.click_step1_agreements_layout

        Click step1_agreements_layout

        Parameters
        ----------
        :return: None
        """
        self.ct_swipe_to_element_center(self.step1_agreements_layout)
        return self.ct_click(self.step1_agreements_layout)

    def click_step2_device_admin_layout(self):
        """RegistrationAndConfigurationPage.click_step2_device_admin_layout

        Click step2_device_admin_layout

        Parameters
        ----------
        :return: None
        """
        self.ct_swipe_to_element_center(self.step2_device_admin_layout)
        return self.ct_click(self.step2_device_admin_layout)

    def click_step3_application_settings_layout(self):
        """RegistrationAndConfigurationPage.click_step3_application_settings_layout

        Click step3_application_settings_layout

        Parameters
        ----------
        :return: None
        """
        self.ct_swipe_to_element_center(self.step3_application_settings_layout)
        return self.ct_click(self.step3_application_settings_layout)

    def click_step4_get_provision_files(self):
        """RegistrationAndConfigurationPage.click_step4_get_provision_files

        Click step4_get_provision_files

        Parameters
        ----------
        :return: None
        """
        self.ct_swipe_to_element_center(self.step4_get_provision_files)
        self.ct_swipe_to_element_center(self.get_provision_file_modal.provision_details_text)
        self.ct_swipe_to_element_center(self.get_provision_file_modal.provision_details_text)
        self.ct_swipe_to_element_center(self.get_provision_file_modal.qrcode_details)
        return self.ct_click(self.step4_get_provision_files)

    def accept_udc_tc_an_pp(self):
        self.accept_privacy_and_tc_modal.accept_tc_an_pp()

    def enable_device_admin_permission(self):
        self.enable_admin_permission_modal.enable_device_admin_permission()

    def accept_application_permissions(self):
        self.accept_install_unknown_app()
        self.allow_and_change_to_access_location_for_app_permission()
        self.allow_udc_display_over_other_apps()
        self.allow_udc_send_notification()

    def accept_install_unknown_app(self):
        self.accept_app_permission_modal.accept_install_unknown_app()

    def allow_and_change_to_access_location_for_app_permission(self):
        self.accept_app_permission_modal.allow_and_change_to_access_location()

    def allow_udc_display_over_other_apps(self):
        self.accept_app_permission_modal.allow_udc_display_over_other_apps()

    def allow_udc_send_notification(self):
        if self.accept_app_permission_modal.check_app_permission_btn_exist():
            self.accept_app_permission_modal.click_app_permission_btn()
        self.accept_app_permission_modal.allow_send_notification_modal.click_allow_btn()

    def scan_qr_code(self):
        self.get_provision_file_modal.scan_qr_code()

    def set_provision_file(self):
        self.get_provision_file_modal.get_and_set_provision_file()

    def check_confirm_dialog_exist(self):
        return self.confirm_modal.wait_for_confirm_dialog()

    def get_confirm_dialog_info(self):
        # assert self.check_confirm_dialog_exist()
        dialog_info = self.confirm_modal.get_confirm_dialog_info()
        self.confirm_modal.click_confirm_btn()
        return dialog_info

    class AcceptPrivacyAndTermsConditions(BasePage):
        # STEP 1: UDC SETUP - Accept UDC Privacy and Terms & Conditions.
        agreement_header_text = AndroidElement('xpath',
                                               '//android.widget.TextView[contains(@resource-id, "agreementHeaderTextView")]')
        agreements_second_header_text = AndroidElement('xpath',
                                                       '//android.widget.TextView[contains(@resource-id, "agreementsSecondHeaderTextView")]')
        agreements_explain = AndroidElement('xpath',
                                            '//android.widget.TextView[contains(@resource-id, "agreements_explain")]')
        agreements_btn = AndroidElement('xpath', '//android.widget.Button[contains(@resource-id, "agreementsButton")]')

        def __init__(self, driver: Device):
            super().__init__(driver)
            self.tc = TermsAndConditionsPage(driver)
            self.pp = PrivacyPolicyPage(driver)

        def check_agreement_header_exist(self) -> bool:
            """AcceptPrivacyAndTermsConditions.check_agreement_header_exist

            Check agreement_header_text exist or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_exist(self.agreement_header_text, timeout=3)

        def check_agreements_second_header_gone(self) -> bool:
            """AcceptPrivacyAndTermsConditions.check_agreements_second_header_gone

            Check agreements_second_header_text disappear or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_disappear(self.agreements_second_header_text, timeout=5)

        def get_agreement_header_text(self) -> str:
            """AcceptPrivacyAndTermsConditions.get_agreement_header_text

            Get agreement_header_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.agreement_header_text)

        def get_agreements_second_header_text(self) -> str:
            """AcceptPrivacyAndTermsConditions.get_agreements_second_header_text

            Get agreements_second_header_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.agreements_second_header_text)

        def get_agreements_explain(self) -> str:
            """AcceptPrivacyAndTermsConditions.get_agreements_explain

            Get agreements_explain

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.agreements_explain)

        def get_agreements_btn_enabled_attr(self):
            """AcceptPrivacyAndTermsConditions.get_agreements_btn_enabled_attr

            Get agreements Button attr enabled

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_for(self.agreements_btn, state="clickable", loop_count=3)
            return self.ct_get_attr(self.agreements_btn, "enabled")

        def get_agreements_btn_text(self):
            """AcceptPrivacyAndTermsConditions.get_agreements_btn_text

            Get agreements Button Text

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_exist(self.agreements_btn)
            return self.ct_get_text(self.agreements_btn)

        def click_agreements_btn(self):
            """AcceptPrivacyAndTermsConditions.click_agreements_btn

            Click agreements Button

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_exist(self.agreements_btn)
            return self.ct_click(self.agreements_btn)

        def accept_tc_an_pp(self):
            """AcceptPrivacyAndTermsConditions.accept_tc_an_pp

            Accept UDC Privacy and Terms & Conditions

            Parameters
            ----------
            :return: None
            """
            self.click_agreements_btn()
            self.tc.click_agreements_accept_btn()
            self.pp.click_agreements_accept_btn()

    class EnableAdminPermissions(BasePage):
        # STEP 2: PERMISSIONS - Enable admin permissions.
        device_admin_header_text = AndroidElement('xpath',
                                                  '//android.widget.TextView[contains(@resource-id, "deviceAdminHeaderTextView")]')
        device_admin_text = AndroidElement('xpath',
                                           '//android.widget.TextView[contains(@resource-id, "deviceAdminTextView")]')
        device_admin_explain_text = AndroidElement('xpath',
                                                   '//android.widget.TextView[contains(@resource-id, "deviceAdminExplainTextView")]')
        device_admin_btn = AndroidElement('xpath',
                                          '//android.widget.Button[contains(@resource-id, "deviceAdminButton")]')

        def __init__(self, driver: Device):
            super().__init__(driver)
            self.activate_device_admin_page = ActivateDeviceAdminAppPage(driver)

        def check_device_admin_header_exist(self) -> bool:
            """EnableAdminPermissions.check_device_admin_header_exist

            Check device_admin_header_text exist or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_exist(self.device_admin_header_text, timeout=3)

        def check_device_admin_text_gone(self) -> bool:
            """EnableAdminPermissions.check_device_admin_text_gone

            Check device_admin_text disappear or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_disappear(self.device_admin_text, timeout=5)

        def get_device_admin_header_text(self) -> str:
            """EnableAdminPermissions.get_device_admin_header_text

            Get device_admin_header_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.device_admin_header_text)

        def get_device_admin_text(self) -> str:
            """EnableAdminPermissions.get_device_admin_text

            Get device_admin_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.device_admin_text)

        def get_device_admin_explain_text(self) -> str:
            """EnableAdminPermissions.get_device_admin_explain_text

            Get device_admin_explain_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.device_admin_explain_text)

        def get_device_admin_btn_enabled_attr(self):
            """EnableAdminPermissions.get_device_admin_btn_enabled_attr

            Get device_admin_btn attr enabled

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_for(self.device_admin_btn, state="clickable", loop_count=3)
            return self.ct_get_attr(self.device_admin_btn, "enabled")

        def get_device_admin_btn_text(self):
            """EnableAdminPermissions.get_device_admin_btn_text

            Get device_admin_btn text

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_for(self.device_admin_btn)
            return self.ct_get_text(self.device_admin_btn)

        def click_device_admin_btn(self):
            """EnableAdminPermissions.click_device_admin_btn

            Click device_admin_btn

            Parameters
            ----------
            :return: None
            """
            if self.ct_wait_exist(self.device_admin_btn, timeout=3, capture=False):
                return self.ct_click(self.device_admin_btn)

        def enable_device_admin_permission(self):
            """EnableAdminPermissions.enable_device_admin_permission

            Enable device admin permission

            Parameters
            ----------
            :return: None
            """
            self.click_device_admin_btn()
            self.activate_device_admin_page.click_action_btn()

    class AcceptAppPermissions(BasePage):
        # STEP 3: PERMISSIONS - Accept app permissions.

        app_settings_header_text = AndroidElement('xpath',
                                                  '//android.widget.TextView[contains(@resource-id, "appSettingsHeaderTextView")]')
        app_settings_details_text = AndroidElement('xpath',
                                                   '//android.widget.TextView[contains(@resource-id, "appSettingsDetailsTextView")]')
        app_permission_explain_text = AndroidElement('xpath',
                                                     '//android.widget.TextView[contains(@resource-id, "appPermissionExplainTextView")]')
        app_permission_btn = AndroidElement('xpath',
                                            '//android.widget.Button[contains(@resource-id, "permissionButton")]')
        app_permission_btn_text = AndroidElement('id',
                                            {"text": "APP PERMISSION"})


        def __init__(self, driver: Device):
            super().__init__(driver)
            self.install_unknown_app_page = InstallUnknownAppsPage(driver)
            self.allow_to_access_location_modal = AllowToAccessLocationModal(driver)
            self.change_location_access_for_modal = ChangeLocationAccessForModal(driver)
            self.display_over_other_apps_page = DisplayOverOtherAppsPage(driver)
            self.allow_send_notification_modal = AllowToSendNotificationModal(driver)

        def check_app_settings_header_exist(self) -> bool:
            """AcceptAppPermissions.check_app_settings_header_exist

            Check app_settings_header_text exist or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_exist(self.app_settings_header_text, timeout=3)

        def check_app_settings_details_gone(self) -> bool:
            """AcceptAppPermissions.check_app_settings_details_text_gone

            Check app_settings_details_text disappear or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_disappear(self.app_settings_details_text, timeout=5)

        def get_app_settings_header_text(self) -> str:
            """AcceptAppPermissions.get_app_settings_header_text

            Get app_settings_header_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.app_settings_header_text)

        def get_app_settings_details(self) -> str:
            """AcceptAppPermissions.get_app_settings_details

            Get app_settings_details_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.app_settings_details_text)

        def get_app_permission_explain_text(self) -> str:
            """AcceptAppPermissions.get_app_permission_explain_text

            Get app_permission_explain_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.app_permission_explain_text)

        def get_app_permission_btn_enabled_attr(self):
            """AcceptAppPermissions.get_app_permission_btn_enabled_attr

            Get app_permission_btn attr enabled

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_for(self.app_permission_btn, state="clickable", loop_count=3)
            return self.ct_get_attr(self.app_permission_btn, "enabled")

        def get_app_permission_btn_text(self):
            """AcceptAppPermissions.get_app_permission_btn_text

            Get device_admin_btn text

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_for(self.app_permission_btn)
            return self.ct_get_text(self.app_permission_btn)

        def check_app_permission_btn_exist(self):
            """AcceptAppPermissions.check_app_permission_btn_exist

            Check app_permission_btn

            Parameters
            ----------
            :return: None
            """
            return self.ct_wait_exist(self.app_permission_btn, timeout=3)

        def click_app_permission_btn(self):
            """AcceptAppPermissions.click_app_permission_btn

            Click app_permission_btn

            Parameters
            ----------
            :return: None
            """
            if self.ct_wait_exist(self.app_permission_btn, timeout=3, capture=False):
                return self.ct_click(self.app_permission_btn)

        def accept_install_unknown_app(self):
            """AcceptAppPermissions.accept_install_unknown_app

            accept_install_unknown_app

            Parameters
            ----------
            :return: None
            """
            self.click_app_permission_btn()
            self.install_unknown_app_page.click_allow_for_this_source()
            self.install_unknown_app_page.click_navigate_up_btn()

        def allow_and_change_to_access_location(self):
            """AcceptAppPermissions.allow_and_change_to_access_location

            allow_and_change_to_access_location

            Parameters
            ----------
            :return: None
            """
            self.click_app_permission_btn()
            self.ct_wait_exist(self.allow_to_access_location_modal.deny_btn, timeout=2, capture=False)
            self.allow_to_access_location_modal.click_allow_foreground_only_btn()
            if self.allow_to_access_location_modal.exist_allow_btn():
                self.allow_to_access_location_modal.click_allow_btn()
            if self.ct_exist(self.app_permission_btn):
                self.click_app_permission_btn()
            self.change_location_access_for_modal.click_permission_no_upgrade_btn()
            if self.allow_to_access_location_modal.exist_allow_btn():
                self.allow_to_access_location_modal.click_allow_btn()

        def allow_udc_display_over_other_apps(self):
            self.display_over_other_apps_page.click_allow_modifying_system_settings()
            self.click_app_permission_btn()
            self.display_over_other_apps_page.set_udc_display_over_other_app()
            if self.ct_wait_exist(self.app_permission_btn_text,3,False):
                log.info('probably abdutils error happened , set display again')
                self.click_app_permission_btn()
                self.display_over_other_apps_page.set_udc_display_over_other_app()


        def allow_udc_send_notification(self):
            self.allow_send_notification_modal.click_allow_btn()

    class GetProvisioningFiles(BasePage):
        # STEP 4: GET PROVISIONING FILES
        provision_files_header_text = AndroidElement('xpath',
                                                     '//android.widget.TextView[contains(@resource-id, "getProvisionFilesHeaderTextView")]')
        provision_details_text = AndroidElement('xpath',
                                                '//android.widget.TextView[contains(@resource-id, "getProvisionDetailsTextView")]')
        scan_qrcode_text = AndroidElement('text', 'Scan QR-Code')
        download_config_link = AndroidElement('xpath',
                                              '//android.widget.TextView[contains(@resource-id, "tv_download_config_hyperlink")]')

        qrcode_title = AndroidElement('xpath', '//android.widget.TextView[contains(@resource-id, "tv_qrcode_title")]')
        qrcode_details = AndroidElement('xpath',
                                        '//android.widget.TextView[contains(@resource-id, "tv_qrcode_details")]')
        qrcode_scan_btn = AndroidElement('xpath', '//android.widget.Button[contains(@resource-id, "btn_qrcode_scan")]')
        qrcode_step1 = AndroidElement('xpath', '//android.widget.LinearLayout[contains(@resource-id, "liv_qr_step1")]')
        qrcode_step2 = AndroidElement('xpath', '//android.widget.LinearLayout[contains(@resource-id, "liv_qr_step2")]')
        qrcode_step3 = AndroidElement('xpath', '//android.widget.LinearLayout[contains(@resource-id, "liv_qr_step3")]')

        config_title = AndroidElement('xpath', '//android.widget.TextView[contains(@resource-id, "tv_config_title")]')
        config_details_steps_header = AndroidElement('xpath',
                                                     '//android.widget.TextView[contains(@resource-id, "tv_config_details_steps_header")]')
        config_step1 = AndroidElement('xpath',
                                      '//android.widget.LinearLayout[contains(@resource-id, "liv_config_step1")]')
        config_step2 = AndroidElement('xpath',
                                      '//android.widget.LinearLayout[contains(@resource-id, "liv_config_step2")]')
        config_step3 = AndroidElement('xpath',
                                      '//android.widget.LinearLayout[contains(@resource-id, "liv_config_step3")]')
        config_step4 = AndroidElement('xpath',
                                      '//android.widget.LinearLayout[contains(@resource-id, "liv_config_step4")]')
        config_step5 = AndroidElement('xpath',
                                      '//android.widget.LinearLayout[contains(@resource-id, "liv_config_step5")]')
        file_browser_btn = AndroidElement('xpath',
                                          '//android.widget.Button[contains(@resource-id, "btn_file_browser")]')
        config_step6 = AndroidElement('xpath',
                                      '//android.widget.LinearLayout[contains(@resource-id, "liv_config_step6")]')
        config_step7 = AndroidElement('xpath',
                                      '//android.widget.LinearLayout[contains(@resource-id, "liv_config_step7")]')

        def __init__(self, driver: Device):
            super().__init__(driver)
            self.file_browser_page = FileBrowserPage(driver)
            self.allow_to_open_camera_modal = AllowToOpenCameraModal(driver)

        def get_provision_files_header_text(self) -> str:
            """GetProvisioningFiles.get_provision_files_header_text

            Get provision_files_header_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.provision_files_header_text)

        def check_provision_details_gone(self) -> bool:
            """GetProvisioningFiles.check_provision_details_gone

            Check provision_details_text gone or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_disappear(self.provision_details_text)

        def get_provision_details_text(self) -> str:
            """GetProvisioningFiles.get_provision_details_text

            Get provision_details_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.provision_details_text)

        def check_download_config_link_exist(self) -> bool:
            """GetProvisioningFiles.check_download_config_link_exist

            Check download_config_link exist or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_exist(self.download_config_link, timeout=3)

        def click_download_config_link(self):
            """GetProvisioningFiles.click_download_config_link

            Click download_config_link

            Parameters
            ----------
            :return: bool
            """
            self.ct_wait_for(self.download_config_link, loop_count=2)
            self.ct_click(self.download_config_link)

        def check_qrcode_scan_btn_exist(self) -> bool:
            """GetProvisioningFiles.check_qrcode_scan_btn_exist

            Check qrcode_scan_btn exist or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_exist(self.qrcode_scan_btn, timeout=3)

        def get_qrcode_scan_btn_enabled_attr(self):
            """GetProvisioningFiles.get_qrcode_scan_btn_enabled_attr

            Get qrcode_scan_btn attr enabled

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_for(self.qrcode_scan_btn, state="clickable", loop_count=3)
            return self.ct_get_attr(self.qrcode_scan_btn, "enabled")

        def click_qrcode_scan_btn(self):
            """GetProvisioningFiles.click_qrcode_scan_btn

            Click qrcode_scan_btn

            Parameters
            ----------
            :return: None
            """
            if self.ct_wait_exist(self.qrcode_scan_btn, timeout=3):
                self.ct_click(self.qrcode_scan_btn)

        def scroll_to_qrcode_scan_btn(self):
            self.ct_scroll_to_element(self.qrcode_scan_btn)

        def scan_qr_code(self):
            self.scroll_to_qrcode_scan_btn()
            self.click_qrcode_scan_btn()
            self.allow_to_open_camera_modal.click_allow_one_time_btn()
            self.allow_to_open_camera_modal.click_allow_one_time_btn()

        def check_file_browser_btn_exist(self) -> bool:
            """GetProvisioningFiles.check_file_browser_btn_exist

            Check file_browser_btn exist or not

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_exist(self.file_browser_btn, timeout=3)

        def click_file_browser_btn(self):
            """GetProvisioningFiles.click_file_browser_btn

            Click qrcode_scan_btn

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_for(self.file_browser_btn)
            self.ct_click(self.file_browser_btn)

        def choose_udc_provision_json_file(self):
            """DownloadConfigFile.choose_udc_provision_json_file

            Select udc-provision.json

            Parameters
            ----------
            :return: None
            """
            self.file_browser_page.click_download_folder()
            self.file_browser_page.click_udc_provision_json_file()

        def file_browser_set_udc_provision_json_file(self):
            """DownloadConfigFile.set_udc_provision_json_file

            Select udc-provision.json

            Parameters
            ----------
            :return: None
            """
            self.click_file_browser_btn()
            self.file_browser_page.click_download_folder()
            self.file_browser_page.click_udc_provision_json_file()

        def get_and_set_provision_file(self):
            self.click_download_config_link()
            self.file_browser_set_udc_provision_json_file()

    class BottomSection(BasePage):
        check_for_updates_btn = AndroidElement('xpath',
                                               '//android.widget.Button[contains(@resource-id, "updateButton")]')
        udc_version_text = AndroidElement('xpath',
                                          '//android.widget.TextView[contains(@resource-id, "udcVersionTextView")]')
        android_id_text = AndroidElement('xpath',
                                         '//android.widget.TextView[contains(@resource-id, "androidIdTextView")]')
        open_source_license_link = AndroidElement('xpath',
                                                  '//android.widget.TextView[contains(@resource-id, "thirdPartyTextView")]')

        processing_loading = AndroidElement('xpath',
                                            '//*[@resource-id="com.lenovo.udcplatform:id/progressBarText"]')
        no_updates_available_btn = AndroidElement('xpath',
                                                  '//*[@resource-id="com.lenovo.udcplatform:id/thirdPartyTextView"]')

        def __init__(self, driver: Device):
            super().__init__(driver)
            self.open_source_license_page = self.OpenSourceLicensesPage(driver)

        def get_udc_version(self) -> str:
            """BottomSection.get_udc_version

            Get udc_version_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.udc_version_text)

        def get_android_id(self) -> str:
            """BottomSection.get_android_id

            Get android_id_text

            Parameters
            ----------
            :return: str
            """
            return self.ct_get_text(self.android_id_text)

        def get_check_for_updates_btn_text(self) -> str:
            """BottomSection.get_check_for_updates_btn_text

            Get check_for_updates_btn text

            Parameters
            ----------
            :return: str
            """
            self.ct_wait_for(self.check_for_updates_btn)
            return self.ct_get_text(self.check_for_updates_btn)

        def click_check_for_updates_btn(self):
            """BottomSection.click_check_for_updates_btn

            Click check_for_updates_btn

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_for(self.check_for_updates_btn)
            self.ct_click(self.check_for_updates_btn)

        def check_open_source_license_link_exist(self) -> bool:
            """BottomSection.check_open_source_license_link_exist

            Check open_source_license_link exist

            Parameters
            ----------
            :return: bool
            """
            return self.ct_wait_exist(self.open_source_license_link, timeout=3)

        def click_open_source_license_link(self):
            """BottomSection.click_open_source_license_link

            Click open_source_license_link

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_for(self.open_source_license_link)
            self.ct_click(self.open_source_license_link)

        def check_no_updates_available_btn(self):
            """BottomSection.check_no_updates_available_btn

            Get no_updates_available_btn text

            Parameters
            ----------
            :return: str
            """
            self.ct_wait_for(self.no_updates_available_btn)
            return self.ct_get_text(self.no_updates_available_btn)

        def check_processing_loading_icon(self):
            """BottomSection.check_processing_loading_icon

            Get processing_loading text

            Parameters
            ----------
            :return: str
            """
            self.ct_wait_for(self.processing_loading)
            return self.ct_get_text(self.processing_loading)

        def wait_processing_loading_disappear(self):
            self.ct_wait_disappear(self.processing_loading, timeout=30)

        class OpenSourceLicensesPage(BasePage):
            licenses_header = AndroidElement('xpath',
                                             '//android.widget.TextView[contains(@resource-id, "third_party_licenses_header")]')
            licenses_web_view = AndroidElement('xpath',
                                               '//android.webkit.WebView[contains(@resource-id, "third_party_licenses_WebView")]')
            close_button = AndroidElement('xpath',
                                          '//android.widget.Button[contains(@resource-id, "third_party_licenses_close_button")]')

            def check_licenses_header_exist(self) -> bool:
                """TermsAndConditionsPage.check_licenses_header_exist

                Check licenses_header exist or not

                Parameters
                ----------
                :return: bool
                """
                return self.ct_wait_exist(self.licenses_header, timeout=3)

            def check_licenses_web_view_exist(self) -> bool:
                """TermsAndConditionsPage.check_licenses_web_view_exist

                Check licenses_web_view exist or not

                Parameters
                ----------
                :return: bool
                """
                return self.ct_wait_exist(self.licenses_web_view, timeout=3)

            def click_close_button(self):
                """BottomSection.click_close_button

                Click close_button

                Parameters
                ----------
                :return: None
                """
                self.ct_wait_for(self.close_button)
                self.ct_click(self.close_button)


class TermsAndConditionsPage(BasePage):
    agreements_header = AndroidElement('xpath',
                                       '//android.widget.TextView[contains(@resource-id, "agreements_header")]')
    agreements_close_btn = AndroidElement('xpath',
                                          '//android.widget.Button[contains(@resource-id, "agreements_CloseButton")]')
    agreements_accept_btn = AndroidElement('xpath',
                                           '//android.widget.Button[contains(@resource-id, "agreements_AcceptButton")]')

    def __init__(self, driver: Device):
        super(TermsAndConditionsPage, self).__init__(driver)

    def check_agreements_header_exist(self) -> bool:
        """TermsAndConditionsPage.check_agreements_header_exist

        Check agreements_header exist or not

        Parameters
        ----------
        :return: bool
        """
        return self.ct_wait_exist(self.agreements_header, timeout=5)

    def check_agreements_header_gone(self) -> bool:
        """TermsAndConditionsPage.check_agreements_header_gone

        Check agreements_header gone or not

        Parameters
        ----------
        :return: bool
        """
        return self.ct_wait_disappear(self.agreements_header, timeout=5)

    def click_agreements_close_btn(self):
        """TermsAndConditionsPage.click_agreements_close_btn

        Click agreements_close_btn

        Parameters
        ----------
        :return: None
        """
        self.ct_wait_for(self.agreements_close_btn)
        self.ct_click(self.agreements_close_btn)

    def get_agreements_accept_btn_enabled(self):
        """TermsAndConditionsPage.get_agreements_accept_btn_enabled

        Get agreements_accept_btn attr enabled

        Parameters
        ----------
        :return: str
        """
        return self.ct_get_attr(self.agreements_accept_btn, "enabled")

    def click_agreements_accept_btn(self):
        """TermsAndConditionsPage.click_agreements_accept_btn

        Click agreements_accept_btn

        Parameters
        ----------
        :return: None
        """
        self.ct_wait_exist(self.agreements_close_btn, timeout=3)
        self.ct_scroll_to(steps=5)
        self.ct_wait_for(self.agreements_accept_btn)
        self.ct_click(self.agreements_accept_btn)


class PrivacyPolicyPage(TermsAndConditionsPage):
    pass


class ActivateDeviceAdminAppPage(BasePage):
    admin_name = AndroidElement('id', 'com.android.settings:id/admin_name')
    action_btn = AndroidElement('id', 'com.android.settings:id/action_button')
    cancel_btn = AndroidElement('id', 'com.android.settings:id/cancel_button')

    def __init__(self, driver: Device):
        super(ActivateDeviceAdminAppPage, self).__init__(driver)

    def check_admin_name_exist(self) -> bool:
        """ActivateDeviceAdminAppPage.check_admin_name_exist

        Check content_frame exist or not

        Parameters
        ----------
        :return: bool
        """
        return self.ct_wait_exist(self.admin_name, timeout=3)

    def check_content_frame_gone(self) -> bool:
        """ActivateDeviceAdminAppPage.check_content_frame_gone

        Check content_frame gone or not

        Parameters
        ----------
        :return: bool
        """
        return self.ct_wait_disappear(self.admin_name, timeout=5)

    def click_action_btn(self):
        """ActivateDeviceAdminAppPage.click_action_btn

        Click action_btn

        Parameters
        ----------
        :return: None
        """
        if self.check_admin_name_exist():
            self.ct_scroll_to_bottom()
            if self.ct_wait_exist(self.action_btn, timeout=3, capture=False):
                self.ct_click(self.action_btn)

    def click_cancel_btn(self):
        """ActivateDeviceAdminAppPage.click_cancel_btn

        Click cancel_btn

        Parameters
        ----------
        :return: None
        """
        self.ct_scroll_to_bottom()
        self.ct_wait_for(self.cancel_btn, loop_count=2)
        self.ct_click(self.cancel_btn)


class InstallUnknownAppsPage(BasePage):
    # allow_for_this_source = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Allow from this source'})
    allow_for_this_source_for_14 = AndroidElement('text', 'Allow from this source')
    navigate_up_btn = AndroidElement('description', 'Navigate up')
    collapse_btn = AndroidElement('description', 'Collapse')

    def __init__(self, driver: Device):
        super(InstallUnknownAppsPage, self).__init__(driver)

    def click_allow_for_this_source(self):
        """ActivateDeviceAdminApp.click_allow_for_this_source

        Click click_allow_for_this_source

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.allow_for_this_source_for_14, timeout=2, capture=False):
            self.ct_click(self.allow_for_this_source_for_14)

    def click_navigate_up_btn(self):
        """DisplayOverOtherAppsPage.click_navigate_up_btn

        Click navigate_up_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.navigate_up_btn, timeout=2, capture=False):
            self.ct_click(self.navigate_up_btn)


class ChangeLocationAccessForModal(BasePage):
    permission_allow_always_btn = AndroidElement('id',
                                                 'com.android.permissioncontroller:id/permission_allow_always_button')
    permission_no_upgrade_btn = AndroidElement('id',
                                               'com.android.permissioncontroller:id/permission_no_upgrade_button')

    def __init__(self, driver: Device):
        super(ChangeLocationAccessForModal, self).__init__(driver)

    def click_permission_allow_always_btn(self):
        """ChangeLocationAccessFor.click_permission_allow_always_btn

        Click permission_allow_always_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.permission_allow_always_btn, timeout=2, capture=False):
            self.ct_click(self.permission_allow_always_btn)

    def click_permission_no_upgrade_btn(self):
        """ChangeLocationAccessFor.click_permission_no_upgrade_btn

        Click permission_no_upgrade_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.permission_no_upgrade_btn, timeout=2, capture=False):
            self.ct_click(self.permission_no_upgrade_btn)


class DisplayOverOtherAppsPage(BasePage):
    search_app_list_menu = AndroidElement('id', 'com.android.settings:id/search_app_list_menu')
    search_app_list_menu_for_14 = AndroidElement('description', 'Search')
    search_text_input = AndroidElement('id', 'android:id/search_src_text')
    search_text_input_for_14 = AndroidElement('text', 'Search…')
    switch_widget = AndroidElement('id', 'android:id/switch_widget')
    app_title = AndroidElement('id', {'resourceId': 'android:id/title',
                                      'text': 'Lenovo Universal Device Client'})
    app_title_for_14 = AndroidElement('text', 'Not allowed')
    whats_input = AndroidElement('id', 'com.buscode.whatsinput:id/tvIP')
    navigate_up_btn = AndroidElement('description', 'Navigate up')
    collapse_btn = AndroidElement('description', 'Collapse')
    allow_display_over_other_apps_text = AndroidElement('id', {'resourceId': 'android:id/title',
                                                               'text': 'Allow display over other apps'})
    allow_display_over_other_apps_text_for_14 = AndroidElement('text', 'Allow display over other apps')
    appear_on_top = AndroidElement('text', 'Appear on top')
    permission_message = AndroidElement('id', 'com.android.permissioncontroller:id/permission_message')
    allow_btn = AndroidElement('id', 'com.android.permissioncontroller:id/permission_allow_button')
    deny_btn = AndroidElement('id', 'com.android.permissioncontroller:id/permission_deny_button')
    allow_modify_system_settings_btn = AndroidElement('text', 'Allow modifying system settings')
    def __init__(self, driver: Device):
        super(DisplayOverOtherAppsPage, self).__init__(driver)

    def click_permission_allow_button(self):
        if self.ct_wait_exist(self.allow_btn, timeout=3, capture=False):
            self.ct_click(self.allow_btn)

    def click_search_app_list_menu(self):
        """DisplayOverOtherAppsPage.click_search_app_list_menu

        Click search_app_list_menu

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.search_app_list_menu, timeout=2, capture=False):
            self.ct_click(self.search_app_list_menu)
        if self.ct_wait_exist(self.search_app_list_menu_for_14, timeout=2, capture=False):
            self.ct_click(self.search_app_list_menu_for_14)

    def search_udc(self):
        """DisplayOverOtherAppsPage.search_udc

        Search udc

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.search_text_input, timeout=2, capture=False):
            self.ct_input("Lenovo Universal Device Client")
        if self.ct_wait_exist(self.search_text_input_for_14, timeout=2, capture=False):
            sleep(2)
            self.ct_input_without_clear("Lenovo Universal Device Client")
            sleep(2)

    def click_app_title(self):
        """DisplayOverOtherAppsPage.click_app_title

        Click app_title

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.app_title, timeout=3, capture=False):
            self.ct_click(self.app_title)
        if self.ct_wait_exist(self.app_title_for_14, timeout=3, capture=False):
            self.ct_click(self.app_title_for_14)

    def click_navigate_up_btn(self):
        """DisplayOverOtherAppsPage.click_navigate_up_btn

        Click navigate_up_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.navigate_up_btn, timeout=2, capture=False):
            self.ct_click(self.navigate_up_btn)
    def click_allow_modifying_system_settings(self):
        """AllowPermissionModal.click_allow_foreground_only_btn

        Click allow_foreground_only_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.allow_modify_system_settings_btn, timeout=6, capture=False):
            self.ct_click(self.allow_modify_system_settings_btn)
            self.click_navigate_up_btn()
    def click_collapse_btn(self):
        """DisplayOverOtherAppsPage.click_collapse_btn

        Click collapse_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.collapse_btn, timeout=3, capture=False):
            self.ct_click(self.collapse_btn)

    def click_allow_display_over_other_apps(self):
        """DisplayOverOtherAppsPage.click_allow_display_over_other_apps

        Click allow_display_over_other_apps_text

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.allow_display_over_other_apps_text, timeout=3, capture=False):
            self.ct_click(self.allow_display_over_other_apps_text)
        elif self.ct_wait_exist(self.allow_display_over_other_apps_text_for_14, timeout=3, capture=False):
            self.ct_click(self.allow_display_over_other_apps_text_for_14)
        elif self.ct_wait_exist(self.permission_message, timeout=3, capture=False):
            self.ct_click(self.allow_btn)

    def set_udc_display_over_other_app(self):
        if self.ct_wait_exist(self.search_app_list_menu, timeout=2, capture=False) or \
                self.ct_wait_exist(self.search_app_list_menu_for_14, timeout=2, capture=False):
            self.click_search_app_list_menu()
            self.search_udc()
            if self.ct_exist(self.switch_widget):
                log.info("generic app")
                self.click_collapse_btn()
                self.click_udc_over_other_apps_generic()
            else:
                log.info("private app")
                self.click_udc_over_other_apps_private()

    def click_udc_over_other_apps_private(self):
        self.click_app_title()
        self.click_allow_display_over_other_apps()
        self.click_navigate_up_btn()
        self.click_collapse_btn()
        self.click_navigate_up_btn()

    def click_udc_over_other_apps_generic(self):
        self.click_app_title()
        # self.ct_press("back")
        self.click_navigate_up_btn()
        if self.ct_wait_exist(self.appear_on_top, timeout=3):
            self.click_app_title()
            # self.ct_press("back")
            self.click_navigate_up_btn()
        self.click_allow_display_over_other_apps()


class FileBrowserPage(BasePage):
    action_bar_root = AndroidElement('id', 'com.google.android.documentsui:id/action_bar_root')
    download_folder = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Download'})
    udc_provision_json_file = AndroidElement('xpath', '//*[@text="udc-provision.json"]')

    def check_file_browser_page_exist(self) -> bool:
        """FileBrowserPage.check_file_browser_page_exist

        Check File browser page should pop up

        Parameters
        ----------
        :return: bool
        """
        return self.ct_wait_exist(self.action_bar_root, timeout=3)

    def click_download_folder(self):
        """FileBrowserPage.click_download_folder

        Click Download folder

        Parameters
        ----------
        :return: None
        """
        if self.ct_exist(self.download_folder):
            self.ct_click(self.download_folder)

    def click_udc_provision_json_file(self):
        """FileBrowserPage.click_udc_provision_json_file

        Click udc-provision.json

        Parameters
        ----------
        :return: None
        """
        self.ct_wait_for(self.udc_provision_json_file)
        self.ct_click(self.udc_provision_json_file)


class AllowToSendNotificationModal(AllowPermissionModal):
    pass


class AllowToEnableBluetoothModal(AllowPermissionModal):
    def click_allow_btn(self):
        """AllowPermissionModal.click_allow_btn

        Click allow_one_time_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.allow_btn, timeout=30):
            self.ct_click(self.allow_btn)


class AllowToOpenCameraModal(AllowPermissionModal):
    pass


class AllowToAccessLocationModal(AllowPermissionModal):
    location_permission = AndroidElement('id', 'com.android.permissioncontroller:id/permission_allow_button')

    def click_allow_location_permission_btn(self):
        """AllowPermissionModal.click_allow_btn

        Click allow_one_time_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.location_permission, timeout=90):
            self.ct_click(self.location_permission)