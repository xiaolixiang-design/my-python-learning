#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: base_page.py
@time: 8/21/2023 3:36 PM
@file_desc:
"""
import logging

from uiautomator2 import Device

from common.u2_client import UiAutomator2Client, AndroidElement

NoneType = type(None)

log = logging.getLogger(__name__)


class BasePage(UiAutomator2Client):
    loading_spinner = AndroidElement('xpath', '//android.widget.ProgressBar[contains(@resource-id, "loading_spinner")]')

    def __init__(self, driver: Device):
        super(BasePage, self).__init__(driver)
        self.driver = driver

    def wait_loading_disappear(self):
        """MainPo.wait_loading_disappear

        Wait for loading icon disappear

        Parameters
        ----------
        :return: None
        """
        self.ct_wait_exist(self.loading_spinner, timeout=30)
        self.ct_exist(self.loading_spinner)
        self.ct_wait_disappear(self.loading_spinner, timeout=90)
