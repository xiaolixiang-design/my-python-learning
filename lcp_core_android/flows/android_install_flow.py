#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: register_flow.py
@time: 8/22/2023 3:04 PM
@file_desc:
"""
import logging

from lcp_core_android.flows.base_mobile_flow import BaseAndroidFlow
from lcp_core_android.library.android_install_po import AndroidInstallPo

NoneType = type(None)
log = logging.getLogger(__name__)


class AndroidInstallFlow(BaseAndroidFlow):
    def __init__(self, driver):
        super(AndroidInstallFlow, self).__init__(driver)
        self.android_install_po = AndroidInstallPo(driver)

    def click_install_btn(self):
        exist_install = self.android_install_po.android_install_page.click_install_btn()
        return exist_install

    def click_install_cancel_btn(self):
        exist_install = self.android_install_po.android_install_page.click_cancel_btn()
        return exist_install

    def click_uninstall_cancel_btn(self):
        exist_ok = self.android_install_po.android_uninstall_page.click_cancel_btn()
        return exist_ok

    def get_uninstall_alert_message(self):
        alert_message = self.android_install_po.android_uninstall_page.get_alert_message()
        return alert_message

    def click_uninstall_ok_btn(self):
        exist_ok = self.android_install_po.android_uninstall_page.click_ok_btn()
        return exist_ok
