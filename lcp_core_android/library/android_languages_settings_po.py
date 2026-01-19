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
from uiautomator2.xpath import XMLElement

from common.u2_client import AndroidElement
from lcp_core_android.library.base_page import BasePage
from lcp_core_android.library.constant.language import LANGUAGE_SETTING_EN, LANGUAGE_SETTING_ZH, \
    LANGUAGE_SETTING_ZH_FOR_MQTT

NoneType = type(None)
log = logging.getLogger(__name__)


class AndroidLanguagesSettingsPo:
    def __init__(self, driver: Device):
        self.languages_settings_page = LanguagesSettings(driver)

    def __set_target_language(self, target_language=LANGUAGE_SETTING_EN):
        languages_list = self.languages_settings_page.get_languages()
        first_lang = languages_list[0]
        if target_language == first_lang:
            return
        elif target_language == languages_list[-1]:
            return self.languages_settings_page.remove_language(language=languages_list[0])
        self.languages_settings_page.add_language(language=target_language)
        self.languages_settings_page.ct_go_home()
        time.sleep(4)
        self.languages_settings_page.ct_open_languages_settings()
        self.languages_settings_page.remove_language(language=first_lang)

    def set_language_en(self):
        self.__set_target_language()

    def set_language_en_for_mqtt(self):
        self.languages_settings_page.add_language(language=LANGUAGE_SETTING_EN)
        self.languages_settings_page.ct_go_home()
        time.sleep(4)
        self.languages_settings_page.ct_open_languages_settings()
        self.languages_settings_page.remove_language_to_en(language=LANGUAGE_SETTING_ZH_FOR_MQTT)

    def set_language_zh(self):
        self.__set_target_language(target_language=LANGUAGE_SETTING_ZH)


class LanguagesSettings(BasePage):
    language_label = AndroidElement('xpath', '//*[@resource-id="com.android.settings:id/label"]')
    first_language = AndroidElement('xpath',
                                    '//*[@resource-id="com.android.settings:id/dragList"]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]')
    second_language = AndroidElement('xpath',
                                     '//*[@resource-id="com.android.settings:id/dragList"]/android.widget.RelativeLayout[2]/android.widget.ImageView[1]')

    remove_btn = AndroidElement('id', 'android:id/title')
    add_language_btn = AndroidElement('id', 'com.android.settings:id/add_language')
    en_picker_item = AndroidElement('id', {'resourceId': 'android:id/language_picker_item',
                                           'text': 'English (United States)'})
    zh_picker_item = AndroidElement('id', {'resourceId': 'android:id/language_picker_item', 'text': '简体中文（中国）'})
    zh_lang_picker_item = AndroidElement('id', {'resourceId': 'android:id/language_picker_item', 'text': '简体中文'})
    zh_country_picker_item = AndroidElement('id', {'resourceId': 'android:id/language_picker_item', 'text': '中国'})

    # Remove selected language?
    confirm_remove_btn = AndroidElement('id', 'android:id/button1')

    def __init__(self, driver: Device):
        super().__init__(driver)
        self.language = LANGUAGE_SETTING_EN
        self.add_language_page = AddALanguagePage(driver)

    @staticmethod
    def language_checkbox(language=LANGUAGE_SETTING_EN):
        return AndroidElement('id', {'resourceId': 'com.android.settings:id/checkbox', 'text': f'{language}'})

    @staticmethod
    def more_options(language=LANGUAGE_SETTING_EN):
        if language == LANGUAGE_SETTING_EN:
            return AndroidElement('description', 'More options')
        elif language == LANGUAGE_SETTING_ZH:
            return AndroidElement('description', '更多选项')

    @staticmethod
    def remove_icon(language=LANGUAGE_SETTING_EN):
        if language == LANGUAGE_SETTING_EN:
            return AndroidElement('description', 'Remove')
        elif language == LANGUAGE_SETTING_ZH:
            return AndroidElement('description', '移除')

    def get_languages(self) -> list:
        languages_list = []
        language_labels = self.ct_get_elements(self.language_label)
        for language_label in language_labels:
            drag_handle_parent: XMLElement = language_label.parent()
            log.info(drag_handle_parent)
            log.info(language_label)
            # self.ct_long_click(self.language_label)
            # time.sleep(60)
            languages_list.append(language_label.text.strip())
        log.info(languages_list)
        self.language = languages_list[0]
        return languages_list

    def click_more_option(self, language=LANGUAGE_SETTING_EN):
        if self.ct_wait_exist(self.more_options(language=language), timeout=3):
            self.ct_click(self.more_options(language=language))

    def click_remove_btn(self):
        if self.ct_wait_exist(self.remove_btn, timeout=3):
            self.ct_click(self.remove_btn)

    def click_add_language_btn(self):
        if self.ct_wait_exist(self.add_language_btn, timeout=3):
            self.ct_click(self.add_language_btn)

    def click_remove_icon(self, language=LANGUAGE_SETTING_EN):
        if self.ct_wait_exist(self.remove_icon(language=language), timeout=3):
            self.ct_click(self.remove_icon(language=language))

    def choose_language(self, language=LANGUAGE_SETTING_EN):
        if self.ct_wait_exist(self.language_checkbox(language=language), timeout=3):
            self.ct_click(self.language_checkbox(language=language))

    def click_confirm_remove_btn(self):
        if self.ct_wait_exist(self.confirm_remove_btn, timeout=3):
            self.ct_click(self.confirm_remove_btn)

    def add_language(self, language=LANGUAGE_SETTING_EN):
        self.ct_wait_exist(self.add_language_btn, timeout=3)
        languages_list = self.get_languages()
        first_lang = languages_list[0]
        self.click_add_language_btn()
        if first_lang != language:
            if language == LANGUAGE_SETTING_EN:
                self.add_language_page.click_en_picker_item()
            elif language == LANGUAGE_SETTING_ZH:
                self.add_language_page.click_zh_picker_item()

    def remove_language(self, language=LANGUAGE_SETTING_ZH):
        self.ct_wait_exist(self.first_language, timeout=3)
        languages_list = self.get_languages()
        first_lang = languages_list[0]
        if language in languages_list:
            self.click_more_option(language=first_lang)
            self.click_remove_btn()
            self.choose_language(language=language)
            self.click_remove_icon(language=first_lang)
            self.click_confirm_remove_btn()

    def remove_language_to_en(self, language=LANGUAGE_SETTING_ZH_FOR_MQTT):
        self.ct_wait_exist(self.first_language, timeout=3)
        self.click_more_option(language=language)
        self.click_remove_btn()
        self.choose_language(language=language)
        self.click_remove_icon(language=language)
        self.click_confirm_remove_btn()


class AddALanguagePage(BasePage):
    en_picker_item = AndroidElement('id', {'resourceId': 'android:id/language_picker_item',
                                           'text': 'English (United States)'})
    zh_picker_item = AndroidElement('id', {'resourceId': 'android:id/language_picker_item', 'text': '简体中文（中国）'})
    en_lang_picker_item = AndroidElement('id', {'resourceId': 'android:id/language_picker_item', 'text': 'English'})
    en_country_picker_item = AndroidElement('id',
                                            {'resourceId': 'android:id/language_picker_item', 'text': 'United States'})
    zh_lang_picker_item = AndroidElement('id', {'resourceId': 'android:id/language_picker_item', 'text': '简体中文'})
    zh_country_picker_item = AndroidElement('id', {'resourceId': 'android:id/language_picker_item', 'text': '中国'})

    def __init__(self, driver: Device):
        super().__init__(driver)
        self.language = LANGUAGE_SETTING_EN

    def click_en_picker_item(self):
        if self.ct_wait_exist(self.en_picker_item, timeout=3):
            self.ct_click(self.en_picker_item)

    def click_zh_picker_item(self):
        if self.ct_wait_exist(self.zh_picker_item, timeout=3):
            self.ct_click(self.zh_picker_item)
        else:
            if self.ct_wait_exist(self.zh_lang_picker_item, timeout=3):
                self.ct_click(self.zh_lang_picker_item)
            if self.ct_wait_exist(self.zh_country_picker_item, timeout=3):
                self.ct_click(self.zh_country_picker_item)

    def click_en_lang_picker_item(self):
        if self.ct_wait_exist(self.en_lang_picker_item, timeout=3):
            self.ct_click(self.en_lang_picker_item)

    def click_en_country_picker_item(self):
        if self.ct_wait_exist(self.en_country_picker_item, timeout=3):
            self.ct_click(self.en_country_picker_item)
