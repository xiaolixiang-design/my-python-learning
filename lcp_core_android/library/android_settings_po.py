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

import uiautomator2
from uiautomator2 import Device

from common.load_profile import LoadNetworkProfile
from common.u2_client import AndroidElement
from data.template.src.context import NetworkType, ProxyMode
from lcp_core_android.library.base_page import BasePage
from lcp_core_android.library.constant.language import LANGUAGE_SETTING_EN, LANGUAGE_SETTING_ZH
from utils.file_helper import sleep

NoneType = type(None)
log = logging.getLogger(__name__)


class AndroidSettingsPo:
    def __init__(self, driver: Device):
        self.android_settings_page = AndroidSettingsPage(driver)

    def swipe_to_setting_storage(self):
        self.android_settings_page.swipe_to_setting_storage()

    def get_storage_usage(self):
        return self.android_settings_page.get_storage_usage()

    def forget_network_settings(self, ssid):
        self.android_settings_page.forget_network(ssid)

    def check_screen_time_out_exist_po(self, timeout_type) -> str:
        return self.android_settings_page.check_screen_time_out_five_exist(timeout_type=timeout_type)


class AndroidSettingsPage(BasePage):
    ssid_add_network = AndroidElement('id', {'resourceId': 'com.android.settings:id/ssid'})
    wifi_security = AndroidElement('id', {'resourceId': 'com.android.settings:id/security'})
    advanced_options = AndroidElement('id', {'resourceId': 'com.android.settings:id/wifi_advanced_togglebox'})
    save_button = AndroidElement('id', {'resourceId': 'android:id/button1', 'text': 'Save'})
    add_network_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Add network'})
    password_input_moto = AndroidElement('id', {'resourceId': 'com.android.settings:id/password'})
    proxy_mode_title = AndroidElement('id', {'resourceId': 'com.android.settings:id/proxy_settings'})
    proxy_hostname = AndroidElement('id', {'resourceId': 'com.android.settings:id/proxy_hostname'})
    proxy_port = AndroidElement('id', {'resourceId': 'com.android.settings:id/proxy_port'})
    proxy_pac = AndroidElement('id', {'resourceId': 'com.android.settings:id/proxy_pac'})
    storage_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Storage'})
    network_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Network & internet'})
    internet_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Internet'})
    internet_title_14 = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Wi-Fi'})
    saved_network_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Saved networks'})
    saved_network_title_tsv = AndroidElement('id', {'resourceId': 'com.tc.devicesettings:id/saved_network_title',
                                                    'text': 'Saved networks'})
    forget_button = AndroidElement('id', {'resourceId': 'com.android.settings:id/button1', 'text': 'Forget'})
    forget_button_tsv = AndroidElement('id', {'resourceId': 'android:id/button1', 'text': 'FORGET'})
    wlan_connection_state = AndroidElement('id', {'resourceId': 'com.android.settings:id/entity_header_summary'})
    wlan_connection_state_tsv = AndroidElement('id', {'resourceId': 'com.tc.devicesettings:id/tv_wifi_state'})
    wifi_title_tsv = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Wi‑Fi'})
    settings_in_tsv = AndroidElement('id', {'resourceId': 'com.microsoft.skype.teams.ipphone:id/fre_partner_settings'})
    device_settings_in_tsv = AndroidElement('id', {'resourceId':
                                                       'com.microsoft.skype.teams.ipphone:id/setting_welcome_label',
                                                   'text':
                                                       'Device settings'})
    wlan_title_tsv = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'WLAN'})
    udc_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Lenovo Universal Device Client'})
    display_over_title = AndroidElement('id', {'text': 'Display over other apps'})
    allow_display_over_title = AndroidElement('id', {'text': 'Allow display over other apps'})
    display_over_switch = AndroidElement('id', {'resourceId': 'android:id/switch_widget'})
    password_input = AndroidElement('id', {'resourceId': 'com.tc.devicesettings:id/password'})
    connect_button = AndroidElement('id', {'resourceId': 'android:id/button1', 'text': 'CONNECT'})
    wifi_name = AndroidElement('id', {'resourceId': 'com.tc.devicesettings:id/wifi_name'})
    wifi_status = AndroidElement('id', {'resourceId': 'com.tc.devicesettings:id/wifi_status'})
    open_attentive_display_five_ele = AndroidElement('id', {'resourceId': 'android:id/summary',
                                                            'text': 'After 5 minutes of inactivity'})
    open_attentive_display_null_ele = AndroidElement('id', {'resourceId': 'android:id/summary',
                                                            'text': 'After null of inactivity'})
    open_attentive_display_not_set_ele = AndroidElement('id', {'resourceId': 'android:id/summary',
                                                               'text': 'Not set'})
    open_attentive_display_ten_ele = AndroidElement('id', {'resourceId': 'android:id/summary',
                                                           'text': 'After 10 minutes of inactivity'})
    connections_title = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Connections'})
    switch_aiplane_button = AndroidElement('id',
                                           {'resourceId': 'android:id/switch_widget', 'description': 'Airplane mode'})
    setting_search_text_input = AndroidElement('id', {'resourceId': 'com.android.settings:id/search_action_bar_title', 'text': 'Search settings'})
    setting_search_src = AndroidElement('id', 'android:id/search_src_text')
    def __init__(self, driver: Device):
        super(AndroidSettingsPage, self).__init__(driver)

    def set_wlan_in_moto_device_settings(self, wlan_type, is_proxy_settings: bool = False,
                                         proxy_mode: ProxyMode = None):
        network_details = LoadNetworkProfile(wlan_type)
        network_detail = network_details.specific_network_details[0]
        ssid = network_detail['SSID']
        password = network_detail['password']
        proxy_address = network_detail['proxy_address']
        port = network_detail['port']
        proxy_script = network_detail['proxy_script']
        security_type = network_detail['security_type']
        wifi_selection = AndroidElement('id', {'resourceId': 'android:id/text1', 'text': security_type})
        try:
            self.ct_open_settings()
            self.ct_scroll_to_top()
            self.ct_exist(self.network_title)
            self.ct_click(self.network_title)
            if self.ct_exist(self.internet_title):
                self.ct_click(self.internet_title)
            if self.ct_exist(self.internet_title_14):
                self.ct_click(self.internet_title_14)
            try:
                self.ct_click(self.add_network_title)
            except uiautomator2.exceptions.UiObjectNotFoundError:
                self.ct_scroll_to_bottom()
                self.ct_click(self.add_network_title)
        except uiautomator2.exceptions.UiObjectNotFoundError:
            self.ct_open_settings()
            self.ct_scroll_to_top()
            self.ct_exist(self.network_title)
            self.ct_click(self.network_title)
            if self.ct_exist(self.internet_title):
                self.ct_click(self.internet_title)
            if self.ct_exist(self.internet_title_14):
                self.ct_click(self.internet_title_14)
            try:
                self.ct_click(self.add_network_title)
            except uiautomator2.exceptions.UiObjectNotFoundError:
                self.ct_scroll_to_bottom()
                self.ct_click(self.add_network_title)
        self.ct_fill_text(self.ssid_add_network, ssid)
        self.ct_click(self.wifi_security)
        self.ct_click(wifi_selection)
        if wlan_type != NetworkType.OPEN:
            self.ct_fill_text(self.password_input_moto, password)
        self.ct_click(self.advanced_options)
        self.ct_scroll_to_bottom()
        if is_proxy_settings:
            self.ct_click(self.proxy_mode_title)
            if proxy_mode == ProxyMode.MANUAL:
                proxy_mode_ui = AndroidElement('id', {'resourceId': 'android:id/text1',
                                                      'text': network_detail.get('manual_mode_in_ui')})
                self.ct_click(proxy_mode_ui)
                self.ct_scroll_to_bottom()
                self.ct_fill_text(self.proxy_hostname, proxy_address)
                self.ct_fill_text(self.proxy_port, port)
            elif proxy_mode == ProxyMode.AUTO:
                proxy_mode_ui = AndroidElement('id', {'resourceId': 'android:id/text1',
                                                      'text': network_detail.get('auto_mode_in_ui')})
                self.ct_click(proxy_mode_ui)
                self.ct_fill_text(self.proxy_pac, proxy_script)
            else:
                raise ValueError('Please select ProxyMode.MANUAL or ProxyMode.AUTO')
            self.ct_scroll_to_bottom()
            self.ct_click(self.save_button)
        self.ct_go_home()
        self.ct_open_settings()
        self.ct_scroll_to_top()
        self.ct_exist(self.network_title)
        self.ct_click(self.network_title)
        if self.ct_exist(self.internet_title):
            self.ct_click(self.internet_title)
        if self.ct_exist(self.internet_title_14):
            self.ct_click(self.internet_title_14)
        network_ssid_button = AndroidElement('id', {'resourceId': 'android:id/title', 'text': ssid})
        if self.ct_wait_exist(network_ssid_button, 20):
            self.ct_click(network_ssid_button)
        time.sleep(10)
        self.check_wlan_connection(ssid)

    def change_display_override_than_other_app_permission_flow(self):
        self.ct_go_home()
        self.ct_clear_settings()
        self.ct_open_settings()
        self.ct_scroll_to_top()
        if self.ct_wait_exist(self.udc_title, 10):
            self.ct_click(self.udc_title)
        else:
            self.ct_click(self.setting_search_text_input)
            sleep(2)
            self.ct_fill_text(self.setting_search_src, "Lenovo Universal Device Client")
            if self.ct_wait_exist(self.udc_title,10):
                self.ct_click(self.udc_title)
        self.ct_scroll_to_element(self.display_over_title)
        self.ct_click(self.display_over_title)
        sleep(2)
        self.ct_click(self.allow_display_over_title)
        self.ct_click_back()



    def click_to_connect_saved_network(self, ssid):
        self.ct_go_home()
        self.ct_open_settings()
        self.ct_scroll_to_top()
        self.ct_exist(self.network_title)
        self.ct_click(self.network_title)
        if self.ct_exist(self.internet_title):
            self.ct_click(self.internet_title)
        if self.ct_exist(self.internet_title_14):
            self.ct_click(self.internet_title_14)
        network_ssid_button = AndroidElement('id', {'resourceId': 'android:id/title', 'text': ssid})
        if self.ct_wait_exist(network_ssid_button, 20):
            self.ct_click(network_ssid_button)
        time.sleep(10)
        self.check_wlan_connection(ssid)

    def exist_storage_title(self):
        return self.ct_exist(self.storage_title)

    def check_wlan_connection(self, network_ssid):
        try:
            self.ct_open_settings()
            self.ct_scroll_to_top()
            self.ct_exist(self.network_title)
            self.ct_click(self.network_title)
            if self.ct_exist(self.internet_title):
                self.ct_click(self.internet_title)
            if self.ct_exist(self.internet_title_14):
                self.ct_click(self.internet_title_14)
            self.ct_scroll_to_bottom()
            self.ct_click(self.saved_network_title)
        except uiautomator2.exceptions.UiObjectNotFoundError:
            self.ct_open_settings()
            self.ct_scroll_to_top()
            self.ct_exist(self.network_title)
            self.ct_click(self.network_title)
            if self.ct_exist(self.internet_title):
                self.ct_click(self.internet_title)
            if self.ct_exist(self.internet_title_14):
                self.ct_click(self.internet_title_14)
            self.ct_scroll_to_bottom()
            self.ct_click(self.saved_network_title)
        check_network_element = AndroidElement('id', {'resourceId': 'android:id/title', 'text': network_ssid})
        self.ct_click(check_network_element)
        state = self.ct_get_text(self.wlan_connection_state)
        assert state == 'Connected', f'The network {network_ssid} is not apply successfully'
        # return self.ct_click(self.network_title)

    def check_wlan_connection_in_tsv(self, network_ssid):
        self.ct_go_home()
        self.ct_click(self.settings_in_tsv)
        self.ct_click(self.device_settings_in_tsv)
        self.ct_click(self.wlan_title_tsv)
        self.ct_click(self.wlan_connection_state_tsv)
        wifi_name = self.ct_get_text(self.wifi_name)
        wifi_status = self.ct_get_text(self.wifi_status)
        assert wifi_name == network_ssid, f'The network {network_ssid} is not apply successfully, Actual is {wifi_name}'
        assert wifi_status == 'Connected', f'The network {network_ssid} is not apply successfully, Actual is {wifi_status}'

    def connect_wlan_in_tsv(self, ssid, password=''):
        self.ct_go_home()
        self.ct_click(self.settings_in_tsv)
        self.ct_click(self.device_settings_in_tsv)
        self.ct_click(self.wlan_title_tsv)
        self.ct_click(AndroidElement('id', {'resourceId': 'com.tc.devicesettings:id/tv_wifi_ssid', 'text': ssid}))
        if self.ct_exist(self.password_input):
            self.ct_click(self.password_input)
            self.ct_input(password)
            self.ct_click(self.connect_button)

    def forget_default_proxy_network_in_tsv(self):
        network_details = LoadNetworkProfile(NetworkType.PROXY)
        ssid = network_details.specific_network_details[0]['SSID']
        self.forget_network_in_tsv(ssid)

    def forget_default_enterprise_network_in_tsv(self):
        network_details = LoadNetworkProfile(NetworkType.ENTERPRISE)
        ssid = network_details.specific_network_details[0]['SSID']
        self.forget_network_in_tsv(ssid)

    def forget_default_normal_network_in_tsv(self):
        network_details = LoadNetworkProfile(NetworkType.WPA2PSK_AES)
        ssid = network_details.specific_network_details[0]['SSID']
        self.forget_network_in_tsv(ssid)

    def forget_network_in_tsv(self, network_ssid):
        self.ct_go_home()
        self.ct_click(self.settings_in_tsv)
        self.ct_click(self.device_settings_in_tsv)
        self.ct_click(self.wlan_title_tsv)
        self.ct_swipe(720, 1005, 720, 80)
        self.ct_click(self.saved_network_title_tsv)
        try:
            forget_network_element = AndroidElement('id', {'resourceId':
                                                               'com.tc.devicesettings:id/saved_network_name',
                                                           'text': network_ssid})
            self.ct_click(forget_network_element)
            self.ct_click(self.forget_button_tsv)
        except uiautomator2.exceptions.UiObjectNotFoundError:
            log.info(f'{network_ssid} Network not save in saved network')
        finally:
            self.ct_go_home()

    def forget_network(self, network_ssid):
        log.info(f'forgetting network {network_ssid}')
        try:
            self.ct_open_settings()
            self.ct_scroll_to_top()
            self.ct_exist(self.network_title)
            self.ct_click(self.network_title)
            if self.ct_exist(self.internet_title):
                self.ct_click(self.internet_title)
            if self.ct_exist(self.internet_title_14):
                self.ct_click(self.internet_title_14)
            self.ct_scroll_to_bottom()
            self.ct_click(self.saved_network_title)
        except uiautomator2.exceptions.UiObjectNotFoundError:
            self.ct_open_settings()
            self.ct_scroll_to_top()
            self.ct_exist(self.network_title)
            self.ct_click(self.network_title)
            if self.ct_exist(self.internet_title):
                self.ct_click(self.internet_title)
            if self.ct_exist(self.internet_title_14):
                self.ct_click(self.internet_title_14)
            self.ct_scroll_to_bottom()
            self.ct_click(self.saved_network_title)
        try:
            forget_network_element = AndroidElement('id', {'resourceId': 'android:id/title', 'text': network_ssid})
            self.ct_click(forget_network_element)
            self.ct_click(self.forget_button)
        except uiautomator2.exceptions.UiObjectNotFoundError:
            log.info(f'{network_ssid} Network not save in saved network')
        finally:
            self.ct_go_home()

    def connect_default_network(self, ssid):
        self.ct_open_settings()
        self.ct_scroll_to_top()
        self.ct_exist(self.network_title)
        self.ct_click(self.network_title)
        if self.ct_exist(self.internet_title):
            self.ct_click(self.internet_title)
        if self.ct_exist(self.internet_title_14):
            self.ct_click(self.internet_title_14)
        network_button = AndroidElement('id', {'resourceId': 'com.android.settings:id/title', 'text': ssid})
        self.ct_click(network_button)

    def forgot_all_profile_network(self):
        for i in [NetworkType.WEP, NetworkType.OPEN, NetworkType.WPA2PSK_AES]:
            network_details = LoadNetworkProfile(i)
            ssid = network_details.specific_network_details[0]['SSID']
            self.forget_network(ssid)

    def forget_proxy_profile_network_in_tsv(self):
        network_details = LoadNetworkProfile(NetworkType.PROXY)
        ssid = network_details.specific_network_details[0]['SSID']
        self.forget_network_in_tsv(ssid)

    def swipe_to_setting_storage(self):
        self.ct_scroll_to_element(self.storage_title)

    def get_storage_usage(self):
        """AndroidSettingsPage.get_storage_usage

        Get storage usage

        Parameters
        ----------
        :return: str
        """
        try:
            return self.ct_find_element(self.storage_title).sibling(resourceId="android:id/summary").get_text()
        except Exception as error:
            self.ct_attach_screenshot()

    def check_screen_time_out_five_exist(self, timeout_type: int) -> str:
        if timeout_type == 5:
            if self.ct_wait_exist(self.open_attentive_display_five_ele, timeout=6) is True:
                context = self.ct_get_text(self.open_attentive_display_five_ele)
                # context = self.ct_get_text(self.open_attentive_display_btn)
                return context
        elif timeout_type == 10:
            if self.ct_wait_exist(self.open_attentive_display_ten_ele, timeout=6) is True:
                context = self.ct_get_text(self.open_attentive_display_ten_ele)
                return context
        else:
            if self.ct_wait_exist(self.open_attentive_display_null_ele, timeout=6) is True:
                context = self.ct_get_text(self.open_attentive_display_null_ele)
                return context
            if self.ct_wait_exist(self.open_attentive_display_not_set_ele, timeout=6) is True:
                context = self.ct_get_text(self.open_attentive_display_not_set_ele)
                return context

    def forget_default_proxy_network_in_moto(self):
        network_details = LoadNetworkProfile(NetworkType.PROXY)
        ssid = network_details.specific_network_details[0]['SSID']
        self.forget_network(ssid)

    def switch_airplane_mode_in_samsung_device(self):
        self.ct_open_settings()
        self.ct_scroll_to_top()
        self.ct_click(self.connections_title)
        self.ct_click(self.switch_aiplane_button)
