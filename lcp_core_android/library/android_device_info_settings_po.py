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
from lcp_core_android.library.components.confirm_modal import ConfirmModal

NoneType = type(None)
log = logging.getLogger(__name__)


class AndroidDeviceInfoSettingsPo:
    def __init__(self, driver: Device):
        self.device_info_settings_page = DeviceInfoSettings(driver)

    def exist_device_name(self):
        return self.device_info_settings_page.exist_device_name_title()

    def scroll_to_device_name(self):
        self.device_info_settings_page.swipe_to_device_name()

    def change_device_name(self, origin_device_name="motorola edge X30", change_device_name="motorola edge X30"):
        self.scroll_to_device_name()
        self.device_info_settings_page.click_device_name_summary(device_name=origin_device_name)
        self.device_info_settings_page.set_device_name_page.set_device_name(change_device_name=change_device_name)


class DeviceInfoSettings(BasePage):
    device_name_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Device name'})

    def __init__(self, driver: Device):
        super().__init__(driver)
        self.set_device_name_page = SetDeviceNamePage(driver)

    @staticmethod
    def device_name_summary(device_name="motorola edge X30"):
        return AndroidElement('id', {'resourceId': 'android:id/summary', 'text': f'{device_name}'})

    def exist_device_name_title(self):
        return self.ct_exist(self.device_name_title)

    def click_device_name_summary(self, device_name="motorola edge X30"):
        if self.ct_wait_exist(self.device_name_summary(device_name), timeout=3):
            self.ct_click(self.device_name_summary(device_name))

    def swipe_to_device_name(self):
        self.ct_scroll_to_element(self.device_name_title)


class SetDeviceNamePage(BasePage):
    device_name_input = AndroidElement('id', 'android:id/edit')
    ok_btn = AndroidElement('id', 'android:id/button1')
    cancel_btn = AndroidElement('id', 'android:id/button2')

    def __init__(self, driver: Device):
        super().__init__(driver)
        self.change_device_name_popup = ChangeDeviceNamePopUp(driver)

    def click_ok_btn(self):
        if self.ct_wait_exist(self.ok_btn, timeout=3):
            self.ct_click(self.ok_btn)

    def click_cancel_btn(self):
        if self.ct_wait_exist(self.cancel_btn, timeout=3):
            self.ct_click(self.cancel_btn)

    def input_device_name(self, change_device_name="motorola edge X30"):
        self.ct_fill_text(self.device_name_input, text=change_device_name)

    def set_device_name(self, change_device_name="motorola edge X30"):
        self.input_device_name(change_device_name)
        self.click_ok_btn()
        self.change_device_name_popup.click_confirm_btn()


class ChangeDeviceNamePopUp(ConfirmModal):
    pass
