#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: allow_permission_modal.py
@time: 10/13/2023 2:49 PM
@file_desc:
"""
from uiautomator2 import Device
from common.u2_client import AndroidElement
from lcp_core_android.library.base_page import BasePage


class AllowPermissionModal(BasePage):
    grant_dialog = AndroidElement('id', 'com.android.permissioncontroller:id/grant_dialog')
    permission_message = AndroidElement('id', 'com.android.permissioncontroller:id/permission_message')
    allow_btn = AndroidElement('id', 'com.android.permissioncontroller:id/permission_allow_button')
    deny_btn = AndroidElement('id', 'com.android.permissioncontroller:id/permission_deny_button')
    allow_foreground_only_btn = AndroidElement('id',
                                               'com.android.permissioncontroller:id/permission_allow_foreground_only_button')
    allow_one_time_btn = AndroidElement('id', 'com.android.permissioncontroller:id/permission_allow_one_time_button')

    def __init__(self, driver: Device):
        super(AllowPermissionModal, self).__init__(driver)

    def check_grant_dialog_exist(self) -> bool:
        """AllowPermissionModal.check_grant_dialog_exist

        Click allow_foreground_only_btn

        Parameters
        ----------
        :return: str
        """
        return self.ct_wait_exist(self.grant_dialog, timeout=3)

    def get_permission_message(self) -> str:
        """AllowPermissionModal.get_permission_message

        Click allow_foreground_only_btn

        Parameters
        ----------
        :return: str
        """
        if self.ct_wait_exist(self.permission_message, timeout=3):
            return self.ct_get_text(self.permission_message)

    def exist_allow_btn(self) -> bool:
        """AllowPermissionModal.exist_allow_btn

        Check allow_btn exist

        Parameters
        ----------
        :return: bool
        """
        return self.ct_exist(self.allow_btn)

    def click_allow_btn(self):
        """AllowPermissionModal.click_allow_btn

        Click allow_one_time_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.allow_btn, timeout=5, capture=False):
            self.ct_click(self.allow_btn)

    def click_deny_btn(self):
        """AllowPermissionModal.click_deny_btn

        Click deny_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.deny_btn, timeout=3, capture=False):
            self.ct_click(self.deny_btn)

    def click_allow_foreground_only_btn(self):
        """AllowPermissionModal.click_allow_foreground_only_btn

        Click allow_foreground_only_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.allow_foreground_only_btn, timeout=3, capture=False):
            self.ct_click(self.allow_foreground_only_btn)

    def click_allow_one_time_btn(self):
        """AllowPermissionModal.click_allow_one_time_btn

        Click allow_one_time_btn

        Parameters
        ----------
        :return: None
        """
        if self.ct_wait_exist(self.allow_one_time_btn, timeout=3, capture=False):
            self.ct_click(self.allow_one_time_btn)
