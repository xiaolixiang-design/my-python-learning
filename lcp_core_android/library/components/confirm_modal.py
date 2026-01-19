#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: confirm_modal.py
@time: 9/14/2023 1:53 PM
@file_desc:
"""
from common.u2_client import AndroidElement
from lcp_core_android.library.base_page import BasePage


class ConfirmModal(BasePage):
    confirm_dialog = AndroidElement('id', 'android:id/content')
    confirm_btn = AndroidElement('id', 'android:id/button1')
    confirm_title = AndroidElement('id', 'android:id/alertTitle')
    confirm_message = AndroidElement('id', 'android:id/message')

    def check_confirm_dialog_gone(self) -> bool:
        """ConfirmModal.check_confirm_dialog_gone

        Check confirm_dialog gone or not

        Parameters
        ----------
        :return: bool
        """
        return self.ct_wait_disappear(self.confirm_dialog, timeout=5)

    def wait_for_confirm_dialog(self) -> bool:
        """ConfirmModal.wait_for_confirm_dialog

        Wait for confirm dialog

        Parameters
        ----------
        :return: bool
        """
        self.ct_wait_exist(self.confirm_dialog, timeout=60)
        return self.ct_wait_exist(self.confirm_title, timeout=60)

    def exist_confirm_title(self) -> bool:
        """ConfirmModal.exist_confirm_title

        Check alert title exist

        Parameters
        ----------
        :return: bool
        """
        return self.ct_exist(self.confirm_title)

    def get_confirm_dialog_info(self) -> dict:
        """ConfirmModal.get_confirm_dialog_info

        Get Confirm Dialog info

        Parameters
        ----------
        :return: dict
        """
        dialog_info = {}
        if self.exist_confirm_title():
            dialog_info.setdefault("title", self.ct_get_text(self.confirm_title))
            dialog_info.setdefault("message", self.ct_get_text(self.confirm_message))
            dialog_info.setdefault("button", self.ct_get_text(self.confirm_btn))
        return dialog_info

    def get_confirm_title(self) -> str:
        """ConfirmModal.get_confirm_title

        Get Confirm Dialog title text

        Parameters
        ----------
        :return: str
        """
        return self.ct_get_text(self.confirm_title)

    def click_confirm_btn(self):
        """ConfirmModal.click_confirm_btn

        Click confirm button

        Parameters
        ----------
        :return: NoneType
        """
        if self.ct_wait_exist(self.confirm_btn, timeout=3):
            self.ct_click(self.confirm_btn)
