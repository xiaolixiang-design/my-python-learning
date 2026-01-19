#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: main_po.py
@time: 8/22/2023 2:57 PM
@file_desc:
"""
import logging
from typing import Any

from uiautomator2 import Device

from lcp_core_android.library.base_page import BasePage

NoneType = type(None)

log = logging.getLogger(__name__)


class MainPo:

    def __init__(self, driver: Device):
        self.driver = driver
        self.base_page = BasePage(driver)
        self.base_page.ct_go_home()

    def launch_app(self, app_name="udc.lenovo.com.udclient") -> NoneType:
        """MainPo.launch_app

        Launch app

        Parameters
        ----------
        :param app_name: str, app name
        :return: NoneType
        """
        return self.base_page.ct_start_app(app_name)

    def stop_app(self, app_name="udc.lenovo.com.udclient") -> NoneType:
        """MainPo.stop_app

        Stop app

        Parameters
        ----------
        :param app_name: str, app name
        :return: NoneType
        """
        return self.base_page.ct_stop_app(app_name)

    def splash_launch_app(self, app_name="udc.lenovo.com.udclient") -> NoneType:
        """MainPo.splash_launch_app

        Splash Launch app, am start udc.lenovo.com.udclient/udc.lenovo.com.udclient.service.initialize.SplashScreen

        Parameters
        ----------
        :param app_name: str, app name
        :return: NoneType
        """
        return self.base_page.ct_launch_splash_screen(app_name)

    def get_app_list(self, app_name="udc.lenovo.com.udclient") -> list:
        """MainPo.get_app_info

        Get app list

        Parameters
        ----------
        :param app_name: str, app name
        :return: list
        """
        return self.base_page.ct_app_list(app_name)

    def get_app_info(self, app_name="udc.lenovo.com.udclient") -> dict:
        """MainPo.get_app_info

        Get app info

        Parameters
        ----------
        :param app_name: str, app name
        :return: dict
        """
        return self.base_page.ct_app_info(app_name)

    def uninstall_app(self, app_name="udc.lenovo.com.udclient") -> bool:
        """MainPo.uninstall_app

        Uninstall app

        Parameters
        ----------
        :param app_name:
        :return: bool
        """
        return self.base_page.ct_uninstall_app(app_name)

    def clear_app(self, app_name="udc.lenovo.com.udclient") -> NoneType:
        """MainPo.clear_app

        Clear app

        Parameters
        ----------
        :param app_name:
        :return: NoneType
        """
        return self.base_page.ct_clear_app(app_name)

    def install_app_via_path(self, app_path) -> Any:
        """MainPo.install_app_via_path

        Install app via file path

        Parameters
        ----------
        :param app_path: str
        :return: Any
        """
        return self.base_page.ct_install_app(app_path)

    def push_file(self, src, dst) -> dict:
        """MainPo.push_file

        Push file to device

        Parameters
        ----------
        :param src: path or fileobj, source file
        :param dst: str, destination can be folder or file path
        :return: dict
        """
        return self.base_page.ct_push_file(src, dst)

    def match_image(self, image_path):
        match_dict = self.base_page.ct_match_image(image_path)
        log.info(match_dict)
        return match_dict.get("similarity") > 0.95

    def go_home(self) -> NoneType:
        """MainPo.go_home

        Unlock and Go to home screen

        Parameters
        ----------
        :return: NoneType
        """
        self.base_page.ct_go_home()

    def press_back(self) -> NoneType:
        """MainPo.press_back

        Press back

        Parameters
        ----------
        :return: NoneType
        """
        self.base_page.ct_press("back")

    def scroll_to_top(self) -> NoneType:
        """MainPo.scroll_to_top

        Scroll to top

        Parameters
        ----------
        :return: NoneType
        """
        self.base_page.ct_scroll_to_top()

    def scroll_to_bottom(self) -> NoneType:
        """MainPo.scroll_to_bottom

        Scroll to bottom

        Parameters
        ----------
        :return: NoneType
        """
        self.base_page.ct_scroll_to_bottom()

    def attach_screenshot(self, png_file_name) -> str:
        """MainPo.attach_screenshot

        Attach png file

        Parameters
        ----------
        :param png_file_name: str
        :return: str
        """
        return self.base_page.ct_attach_screenshot(png_file_name)

    def open_settings_page(self):
        self.base_page.ct_open_settings()

    def open_security_settings_page(self):
        self.base_page.ct_open_security_settings()

    def clear_settings(self):
        self.base_page.ct_clear_settings()

    def open_languages_settings_page(self):
        self.base_page.ct_open_languages_settings()

    def open_date_time_settings_page(self):
        self.base_page.ct_open_date_time_settings()

    def open_device_info_settings_page(self):
        self.base_page.ct_open_device_info_settings()

    def get_locale_language(self):
        return self.base_page.ct_get_language()

    def reboot(self):
        self.base_page.ct_reboot()

    def disable_wifi(self):
        return self.base_page.ct_disable_wifi()

    def enable_wifi(self):
        return self.base_page.ct_enable_wifi()

    def get_camera_client(self):
        return self.base_page.ct_get_camera_client()
