#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: android_security_po.py
@time: 9/11/2023 4:41 PM
@file_desc:
"""
import logging

from uiautomator2 import Device

from common.u2_client import AndroidElement
from lcp_core_android.library.base_page import BasePage

NoneType = type(None)
log = logging.getLogger(__name__)


class AndroidSecurityPo:
    def __init__(self, driver: Device):
        self.android_security_page = AndroidSecurityPage(driver)

    def deactivate_admin_udc(self):
        self.android_security_page.deactivate_admin_app_udc()


class AndroidSecurityPage(BasePage):
    device_admin_apps_text = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Device admin apps'})
    no_active_apps_summary = AndroidElement('id', {'resourceId': 'android:id/summary', 'text': 'No active apps'})
    other_security_settings = AndroidElement('id',
                                             {'resourceId': 'android:id/title', 'text': 'Other security settings'})
    more_security_settings = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'More security settings'})
    more_security_privacy = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'More security & privacy'})

    def __init__(self, driver: Device):
        super(AndroidSecurityPage, self).__init__(driver)
        self.device_admin_apps = self.DeviceAdminApps(driver)
        self.device_admin_app = self.DeviceAdminApp(driver)

    def click_device_admin_apps_text(self):
        """AndroidSecurityPage.click_device_admin_apps_text

        Click device_admin_apps_text

        Parameters
        ----------
        :return: None
        """
        return self.ct_click(self.device_admin_apps_text)
    def click_more_security_privacy(self):
        """AndroidSecurityPage.click_more_security_settings

        Click other_security_settings

        Parameters
        ----------
        :return: None
        """
        return self.ct_click(self.more_security_privacy)

    def check_no_active_apps_summary(self) -> bool:
        """AndroidSecurityPage.check_no_active_apps_summary

        check no_active_apps_summary

        Parameters
        ----------
        :return: bool
        """
        return self.ct_exist(self.no_active_apps_summary)

    def check_other_security_settings(self) -> bool:
        """AndroidSecurityPage.check_other_security_settings

        check other_security_settings

        Parameters
        ----------
        :return: bool
        """
        return self.ct_exist(self.other_security_settings)

    def click_more_security_settings(self):
        """AndroidSecurityPage.click_more_security_settings

        Click other_security_settings

        Parameters
        ----------
        :return: None
        """
        return self.ct_click(self.more_security_settings)

    def click_other_security_settings(self):
        """AndroidSecurityPage.click_other_security_settings

        Click other_security_settings

        Parameters
        ----------
        :return: None
        """
        return self.ct_click(self.other_security_settings)

    def deactivate_admin_app_udc(self):
        if self.ct_wait_exist(self.more_security_settings, timeout=3):
            self.click_more_security_settings()
        elif self.ct_wait_exist(self.other_security_settings, timeout=3):
            self.click_other_security_settings()
        elif self.ct_wait_exist(self.more_security_privacy, timeout=3):
            self.click_more_security_privacy()
            self.ct_scroll_to_bottom()
        self.ct_wait_exist(self.no_active_apps_summary, timeout=10)
        exist = self.check_no_active_apps_summary()
        if not exist:
            self.click_device_admin_apps_text()
            self.device_admin_apps.click_udc_app_text()
            self.device_admin_app.deactivate_udc()
        self.ct_press('back')
        self.ct_press('back')
        self.ct_press('back')
        self.ct_press('back')

    class DeviceAdminApps(BasePage):
        udc_app_text = AndroidElement('id',
                                      {'resourceId': 'android:id/title', 'text': 'Lenovo Universal Device Client'})

        def click_udc_app_text(self):
            """DeviceAdminApps.click_udc_app_text

            Click udc_app_text

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_exist(self.udc_app_text, timeout=3)
            self.ct_click(self.udc_app_text)

    class DeviceAdminApp(BasePage):
        restricted_action_btn = AndroidElement('id', 'com.android.settings:id/restricted_action')
        confirm_btn = AndroidElement('id', 'android:id/button1')
        cancel_btn = AndroidElement('id', 'com.android.settings:id/cancel_button')
        device_admin_chex = AndroidElement('id', 'com.android.settings:id/checkbox')
        set_storage_encryption = AndroidElement('id',
                                                {'resourceId': 'android:id/permission_group',
                                                 'text': 'Set storage encryption'})
        erase_all_data = AndroidElement('id',
                                        {'resourceId': 'android:id/permission_group',
                                         'text': 'Erase all data'})

        def click_restricted_action(self):
            """DeviceAdminApp.click_restricted_action

            Click click_restricted_action

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_exist(self.restricted_action_btn, timeout=3)
            self.ct_click(self.restricted_action_btn)

        def click_cancel_btn(self):
            """DeviceAdminApp.click_confirm_btn

            Click confirm_btn

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_exist(self.cancel_btn, timeout=3)
            self.ct_click(self.cancel_btn)

        def click_confirm_btn(self):
            """DeviceAdminApp.click_confirm_btn

            Click confirm_btn

            Parameters
            ----------
            :return: None
            """
            self.ct_wait_exist(self.confirm_btn, timeout=3)
            self.ct_click(self.confirm_btn)

        def deactivate_udc(self):
            self.ct_scroll_to_bottom()
            self.click_restricted_action()
            self.click_confirm_btn()
