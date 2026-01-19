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


class AndroidDateTimeSettingsPo:
    def __init__(self, driver: Device):
        self.date_time_settings_page = DateTimeSettingsPage(driver)

    def set_time_zone(self, region="Albania"):
        self.date_time_settings_page.disable_set_time_auto()
        self.date_time_settings_page.disable_set_timezone_auto()
        self.date_time_settings_page.select_time_zone(region)

    def set_datetime_timezone_auto(self):
        self.date_time_settings_page.enable_set_time_auto()
        self.date_time_settings_page.enable_set_timezone_auto()

    def get_time_zone_value(self):
        return self.date_time_settings_page.get_timezone_select_text()


class DateTimeSettingsPage(BasePage):
    set_time_auto_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Set time automatically'})
    time_select_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Date'})
    set_timezone_auto_title = AndroidElement('id',
                                             {'resourceId': 'android:id/title', 'text': 'Set automatically'})
    timezone_select_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Time zone'})
    timezone_select_text = AndroidElement('xpath',
                                          '//*[@resource-id="com.android.settings:id/recycler_view"]/android.widget.LinearLayout[6]/android.widget.RelativeLayout[1]/android.widget.TextView[2]')
    timezone_select_text_14 = AndroidElement('xpath',
                                             '//*[@resource-id="com.android.settings:id/recycler_view"]/android.widget.LinearLayout[5]/android.widget.RelativeLayout[1]/android.widget.TextView[2]')

    def __init__(self, driver: Device):
        super().__init__(driver)
        self.select_timezone_page = SelectTimeZonePage(driver)

    def check_time_select_enable(self):
        if self.ct_wait_exist(self.time_select_title, timeout=5):
            return str(self.ct_get_attr(self.time_select_title, "enabled")).lower() == "true"

    def check_timezone_select_enable(self):
        if self.ct_wait_exist(self.timezone_select_text, timeout=3):
            return str(self.ct_get_attr(self.timezone_select_text, "enabled")).lower() == "true"
        if self.ct_wait_exist(self.timezone_select_text_14, timeout=3):
            return str(self.ct_get_attr(self.timezone_select_text_14, "enabled")).lower() == "true"
        
    def get_timezone_select_text(self):
        if self.ct_wait_exist(self.timezone_select_text, timeout=3):
            return self.ct_get_text(self.timezone_select_text).strip()
        if self.ct_wait_exist(self.timezone_select_text_14, timeout=3):
            return self.ct_get_text(self.timezone_select_text_14).strip()

    def click_set_time_auto_toggle(self):
        if self.ct_wait_exist(self.set_time_auto_title, timeout=3):
            self.ct_click(self.set_time_auto_title)

    def click_set_timezone_auto_toggle(self):
        if self.ct_wait_exist(self.set_timezone_auto_title, timeout=3):
            self.ct_click(self.set_timezone_auto_title)

    def click_timezone_select_text(self):
        if self.ct_wait_exist(self.timezone_select_text, timeout=5):
            self.ct_click(self.timezone_select_text)

    def enable_set_time_auto(self):
        if self.check_time_select_enable():
            self.click_set_time_auto_toggle()

    def disable_set_time_auto(self):
        if not self.check_time_select_enable():
            self.click_set_time_auto_toggle()

    def enable_set_timezone_auto(self):
        if self.check_timezone_select_enable():
            self.click_set_timezone_auto_toggle()


    def disable_set_timezone_auto(self):
        if not self.check_timezone_select_enable():
            self.click_set_timezone_auto_toggle()

    def select_time_zone(self, region="Albania"):
        self.click_timezone_select_text()
        self.select_timezone_page.search_region(region)


class SelectTimeZonePage(BasePage):
    region_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Region'})
    search_region_input = AndroidElement('id', 'android:id/search_src_text')
    navigate_up_btn = AndroidElement('description', 'Navigate up')
    search_region_result = AndroidElement('id', 'android:id/title')

    def __init__(self, driver: Device):
        super().__init__(driver)

    def click_region_title(self):
        if self.ct_wait_exist(self.region_title, timeout=3):
            self.ct_click(self.region_title)

    def input_search_region_text(self, region="Albania"):
        if self.ct_wait_exist(self.search_region_input, timeout=2, capture=False):
            self.ct_input(region)

    def click_search_region_result(self):
        if self.ct_wait_exist(self.search_region_result, timeout=3):
            self.ct_click(self.search_region_result)

    def click_navigate_up_btn(self):
        if self.ct_wait_exist(self.navigate_up_btn, timeout=3, capture=False):
            self.ct_click(self.navigate_up_btn)

    def search_region(self, region="Albania"):
        self.click_region_title()
        self.input_search_region_text(region)
        self.click_search_region_result()
        self.click_navigate_up_btn()
