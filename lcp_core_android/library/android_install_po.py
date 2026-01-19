#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: android_security_po.py
@time: 9/11/2023 4:41 PM
@file_desc:
"""
import logging
import time

from uiautomator2 import Device

from common.u2_client import AndroidElement
from lcp_core_android.library.base_page import BasePage

NoneType = type(None)
log = logging.getLogger(__name__)


class AndroidInstallPo:
    def __init__(self, driver: Device):
        self.android_install_page = AndroidInstallPage(driver)
        self.android_uninstall_page = AndroidUninstallPage(driver)


class AndroidInstallPage(BasePage):
    installer_text = AndroidElement('id', 'com.android.packageinstaller:id/text')
    installer_app_name = AndroidElement('id', 'com.android.packageinstaller:id/app_name')
    app_install_source = AndroidElement('id', 'com.android.packageinstaller:id/app_install_source')
    app_install_version_name = AndroidElement('id', 'com.android.packageinstaller:id/app_install_version_name')
    app_install_apk_size = AndroidElement('id', 'com.android.packageinstaller:id/app_install_apk_size')
    install_text = AndroidElement('id', 'com.android.packageinstaller:id/text')
    install_btn = AndroidElement('id', 'com.android.packageinstaller:id/install_button')
    install_btn_14 = AndroidElement('id', 'com.android.packageinstaller:id/safe_install_button')
    cancel_btn = AndroidElement('id', 'com.android.packageinstaller:id/cancel_button')

    def __init__(self, driver: Device):
        super(AndroidInstallPage, self).__init__(driver)

    def get_installer_text(self):
        """AndroidInstallPage.get_installer_text

        get_alert_title

        Parameters
        ----------
        :return: str
        """
        if self.ct_wait_exist(self.installer_text, timeout=60):
            return self.ct_get_text(self.installer_text)

    def click_install_btn(self):
        """AndroidInstallPage.click_install_btn

        click_install_btn

        Parameters
        ----------
        :return: str
        """
        if self.ct_wait_exist(self.install_btn, timeout=60):
            self.ct_click(self.install_btn)
            return True
        elif self.ct_wait_exist(self.install_btn_14, timeout=60):
            self.ct_click(self.install_btn_14)
            return True

    def click_cancel_btn(self):
        """AndroidInstallPage.click_cancel_btn

        click_cancel_btn

        Parameters
        ----------
        :return: str
        """
        if self.ct_wait_exist(self.cancel_btn, timeout=30):
            self.ct_click(self.cancel_btn)
            return True


class AndroidUninstallPage(BasePage):
    alert_title = AndroidElement('id', 'android:id/alertTitle')
    alert_message = AndroidElement('id', 'android:id/message')
    ok_btn = AndroidElement('id', 'android:id/button1')
    cancel_btn = AndroidElement('id', 'android:id/button2')

    def __init__(self, driver: Device):
        super(AndroidUninstallPage, self).__init__(driver)

    def get_alert_title(self):
        """AndroidUninstallPage.get_alert_title

        get_alert_title

        Parameters
        ----------
        :return: str
        """
        if self.ct_wait_exist(self.alert_title, timeout=60):
            return self.ct_get_text(self.alert_title)

    def get_alert_message(self):
        """AndroidUninstallPage.get_alert_message

        get_alert_message

        Parameters
        ----------
        :return: str
        """
        if self.ct_wait_exist(self.alert_message, timeout=60):
            return self.ct_get_text(self.alert_message)

    def click_ok_btn(self):
        """AndroidUninstallPage.click_ok_btn

        click_ok_btn

        Parameters
        ----------
        :return: str
        """
        if self.ct_wait_exist(self.ok_btn, timeout=60):
            self.ct_click(self.ok_btn)
            return True

    def click_cancel_btn(self):
        """AndroidUninstallPage.click_cancel_btn

        click_cancel_btn

        Parameters
        ----------
        :return: str
        """
        if self.ct_wait_exist(self.cancel_btn, timeout=30):
            self.ct_click(self.cancel_btn)
            return True
