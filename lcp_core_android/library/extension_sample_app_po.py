# Project        : extension_sample_app_po.py
# @Jira Tests     : UDC-2675
# @Jira AT        : UDC-2683
# @Jira Dev       : UDC-2599
# @Author         : yuxc6@lenovo.com
# @dates          : 4/19/2024 1:39 PM
import logging
import subprocess
import time

import uiautomator2
from uiautomator2 import Device

from common.u2_client import AndroidElement

from lcp_core_android.library.base_page import BasePage
from lcp_core_android.library.components.confirm_modal import ConfirmModal
try:
    from data.template.smv2_relate import SMV2
    from utils.file_helper import sleep
except ImportError as e:
    SMV2 =None
    sleep=time.sleep
NoneType = type(None)
log = logging.getLogger(__name__)


class AndroidExtensionAppPo:
    def __init__(self, driver: Device):
        self.android_extension_app_page = AndroidExtensionAppPage(driver)
        self.confirm_modal = ConfirmModal(driver)
        self.invoke_http_request = InvokeHttpRequest(driver)


class AndroidExtensionAppPage(BasePage):
    enable_mqtt_button = AndroidElement('id', {
                                               'text': 'Enable Mqtt'})
    disable_mqtt_button = AndroidElement('id', {
                                                'text': 'Disable Mqtt'})
    publish_mqtt_button = AndroidElement('id', {
                                                'text': 'Publish Mqtt Message'})
    registration_button = AndroidElement('id', {
                                                "text": "File Picker"})
    get_udc_status_btn = AndroidElement('id', {
                                               "text": "Get UDC Status"})
    get_udc_status_btn_new_ui = AndroidElement('id', {
        "text": "Get UDC Status"})
    get_device_access_stamp = AndroidElement('id', {
                                                    "text": "Get device access stamp"})
    get_device_config_btn = AndroidElement('id', {
                                                  "text": "Get Device Config"})
    send_message_to_udc = AndroidElement('id', {
        "text": "Send Message to UDC"})
    attach_message_file_button = AndroidElement('id', {
        "text": "Attach Message File"})

    choice_pri_app_button = AndroidElement('id', {'resourceId': 'android:id/text1',
                                                  'text': 'Priv App'})
    choice_gen_app_button = AndroidElement('id', {'resourceId': 'android:id/text1',
                                                  'text': 'Generic App'})
    choice_platform_app_button = AndroidElement('id', {'resourceId': 'android:id/text1',
                                                       'text': 'Platform App'})
    get_alert_title = AndroidElement('id', {'resourceId': 'android:id/alertTitle'})
    get_alert_msg_btn = AndroidElement('id', {'resourceId': 'android:id/contentPanel'})
    get_alert_ok_btn = AndroidElement('id', {'resourceId': 'android:id/button1'})
    root_folder = AndroidElement('id', {
        "description": "Show roots"})
    download_folder = AndroidElement('id', {'resourceId': 'android:id/title', 'text': 'Downloads'})

    msg_digest_element = AndroidElement('id', {
        "text": SMV2.msg_digest})
    invalid_string_digest_element = AndroidElement('id', {
        "text": SMV2.invalid_str_digest})
    invalid_signature_digest_element = AndroidElement('id', {
        "text": SMV2.invalid_signature_digest})
    invalid_signature_message_element = AndroidElement('id', {
        "text": "msg21_Popup"})

    dismiss_btn = AndroidElement('id', {
        "text": "Dismiss"})
    ok_btn = AndroidElement('id', {'resourceId': 'android:id/button1', 'text': 'OK'})
    is_async_button = AndroidElement('xpath',
                                     '//android.view.ViewGroup/android.view.View[1]/android.view.View[1]/'
                                     'android.view.View[1]/android.view.View[1]/android.widget.RadioButton[1]')
    get_oem_config_element = AndroidElement('id', {
        "text": "Get OEM Device Config"})
    alert_msg_element = AndroidElement('id', {'resourceId': 'android:id/message'})

    def click_registration_button(self):
        if self.ct_wait_exist(self.registration_button, timeout=10):
            self.ct_click(self.registration_button)

    def __init__(self, driver: Device):
        super(AndroidExtensionAppPage, self).__init__(driver)

    def click_get_udc_status_btn(self):
        self.ct_scroll_to_element(self.get_udc_status_btn)
        if self.ct_wait_exist(self.get_udc_status_btn, timeout=10):
            self.ct_click(self.get_udc_status_btn)

    def click_get_udc_status_btn_new_ui(self):
        self.ct_scroll_to_element(self.get_udc_status_btn_new_ui)
        if self.ct_wait_exist(self.get_udc_status_btn_new_ui, timeout=10):
            self.ct_click(self.get_udc_status_btn_new_ui)

    def click_get_device_access_stamp_btn(self):
        self.ct_scroll_to_element(self.get_device_access_stamp)
        if self.ct_wait_exist(self.get_device_access_stamp, timeout=10):
            self.ct_click(self.get_device_access_stamp)

    def click_get_device_config_btn(self):
        self.ct_scroll_to_element(self.get_device_config_btn)
        if self.ct_wait_exist(self.get_device_config_btn, timeout=10):
            self.ct_click(self.get_device_config_btn)

    def click_enable_mqtt_button(self):
        if self.ct_wait_exist(self.enable_mqtt_button, timeout=10):
            self.ct_click(self.enable_mqtt_button)

    def click_disable_mqtt_button(self):
        if self.ct_wait_exist(self.disable_mqtt_button, timeout=10):
            self.ct_click(self.disable_mqtt_button)

    def click_publish_mqtt_button(self):
        if self.ct_wait_exist(self.publish_mqtt_button, timeout=10):
            self.ct_click(self.publish_mqtt_button)

    def click_publish_mqtt_force_by_coordinates(self,serial):
        """
            This func only suitable for private app, phone sn ZY22HHX3P9
        """
        self.ct_scroll_to_bottom()
        for i in range(5):
            self.ct_swipe(0.5, 0.5, 0.5, 0.7)
        sleep(1)
        subprocess.run(["adb", "-s", serial, "shell", "input", "tap", "509", "2100"])
        if self.ct_wait_exist(self.alert_msg_element,30):
            pass
        assert self.ct_exist(self.alert_msg_element), 'Not able to click publish message'
        sleep(5)
        return self.ct_get_text(self.alert_msg_element)


    def get_alert_title_text(self):
        if self.ct_wait_exist(self.get_alert_title, timeout=10):
            return self.ct_get_text(self.get_alert_title)

    def get_oem_config_flow(self):
        self.ct_scroll_to_element_slowly(self.get_oem_config_element)
        self.ct_scroll_up_to_element(self.get_oem_config_element, 30)
        self.ct_scroll_to_element(self.get_oem_config_element, 20)
        self.ct_scroll_up_to_element_quick(self.get_oem_config_element, 15)
        self.ct_scroll_to_element(self.get_oem_config_element, 15)
        self.ct_scroll_up_to_element(self.get_oem_config_element, 15)
        self.ct_click(self.get_oem_config_element)
        sleep(10)
        log.info(self.ct_get_text(self.alert_msg_element))
        return self.ct_get_text(self.alert_msg_element)

    def set_attached_digest(self, close_after_set: bool = False, attach_file: AndroidElement = msg_digest_element):
        log.info('Set attached digest in extension app')
        if self.ct_wait_exist(self.attach_message_file_button, timeout=10):

            self.ct_click(self.attach_message_file_button)
            if self.ct_wait_exist(attach_file, timeout=10):
                self.ct_click(attach_file)
            else:
                self.ct_click(self.root_folder)
                self.ct_click(self.download_folder)
                self.ct_click(attach_file)
        if close_after_set:
            if self.ct_wait_exist(self.dismiss_btn, timeout=10):
                self.ct_click(self.dismiss_btn)
            assert self.ct_wait_exist(attach_file, timeout=5)

    def click_send_message_btn(self):
        if self.ct_wait_exist(self.send_message_to_udc, timeout=5):
            self.ct_click(self.send_message_to_udc)
        else:
            self.ct_start_app(SMV2.extension_app_package_name)

    def scroll_to_message(self, digest_id, if_click_ok = True):
        digest_element = AndroidElement('id', {
            "text": digest_id})
        self.ct_scroll_to_element_slowly(digest_element, timeout=30)
        try:
            self.ct_click(digest_element)
            if if_click_ok:
                if self.ct_wait_exist(self.ok_btn, timeout= 120):
                    self.ct_click(self.ok_btn)
        except Exception as e:
            self.ct_scroll_up_to_element(digest_element, 30)
            self.ct_scroll_to_element(digest_element, 20)
            self.ct_scroll_up_to_element_quick(digest_element,15)
            self.ct_scroll_to_element(digest_element, 15)
            self.ct_scroll_up_to_element(digest_element, 15)
            if self.ct_wait_exist(digest_element,timeout=10):
                self.ct_click(digest_element)
            else:
                raise uiautomator2.UiObjectNotFoundError('Not find element')

    def scroll_to_element_up_and_down(self, android_element:AndroidElement, if_click_ok = False):
        self.ct_scroll_to_element_slowly(android_element, timeout=30)
        try:
            self.ct_click(android_element)
            if if_click_ok:
                if self.ct_wait_exist(self.ok_btn, timeout= 120):
                    self.ct_click(self.ok_btn)
        except Exception as e:
            self.ct_scroll_up_to_element(android_element, 30)
            self.ct_scroll_to_element(android_element, 20)
            self.ct_scroll_up_to_element_quick(android_element, 15)
            self.ct_scroll_to_element(android_element, 15)
            self.ct_scroll_up_to_element(android_element, 15)
            if self.ct_wait_exist(android_element, timeout=10):
                self.ct_click(android_element)
            else:
                raise uiautomator2.UiObjectNotFoundError('Not find element')


    def set_is_async_true(self):

        try:
            self.ct_click(self.is_async_button)
        except uiautomator2.exceptions.UiObjectNotFoundError as e:
            self.ct_scroll_up_to_element(self.is_async_button, 20)
            self.ct_click(self.is_async_button)

    def click_ok_button(self):
        if self.ct_wait_exist(self.ok_btn, timeout=10):
            self.ct_click(self.ok_btn)
        else:
            log.error('No click on button found')

    def get_alert_msg(self):
        if self.ct_wait_exist(self.get_alert_msg_btn, timeout=10):
            # return self.ct_get_text(self.get_alert_msg_btn)
            return self.driver(resourceId=self.get_alert_msg_btn).get_text()

    def click_get_alert_ok_btn(self):
        if self.ct_wait_exist(self.get_alert_ok_btn, timeout=10):
            return self.ct_click(self.get_alert_ok_btn)

    def click_choice_pri_app_button(self):
        if self.ct_wait_exist(self.choice_pri_app_button, timeout=60):
            return self.ct_click(self.choice_pri_app_button)

    def click_choice_generic_app_button(self):
        if self.ct_wait_exist(self.choice_gen_app_button, timeout=10):
            return self.ct_click(self.choice_gen_app_button)

    def click_choice_platform_app_button(self):
        if self.ct_wait_exist(self.choice_platform_app_button, timeout=10):
            return self.ct_click(self.choice_platform_app_button)

    def extension_init_launch_alert_with_platform_app(self):
        self.click_choice_platform_app_button()
        self.click_get_alert_ok_btn()

    def extension_init_launch_alert(self):
        self.click_choice_pri_app_button()
        self.click_get_alert_ok_btn()

    def extension_init_launch_alert_with_generic_app(self):
        self.click_choice_generic_app_button()
        self.click_get_alert_ok_btn()

    def ct_scroll_to_enable_mqtt_btn(self):
        self.scroll_to_element_up_and_down(self.enable_mqtt_button)

    def ct_scroll_to_disable_mqtt_btn(self):
        self.scroll_to_element_up_and_down(self.disable_mqtt_button)

    def ct_scroll_to_publish_mqtt_button(self):
        self.scroll_to_element_up_and_down(self.publish_mqtt_button)

    def wait_for_registration_btn_appear(self, time_out=120):
        is_exist = self.ct_wait_exist(self.registration_button, timeout=5)
        log.info("wait register element is {0}".format(is_exist))
        if self.ct_wait_exist(self.choice_pri_app_button, timeout=10) is True:
            self.extension_init_launch_alert()
        else:
            end_time = time.time() + time_out
            while time.time() < end_time:
                self.click_get_alert_ok_btn()
                self.click_choice_pri_app_button()
                self.click_get_alert_ok_btn()
                is_exist = self.ct_wait_exist(self.registration_button, timeout=5)
                if is_exist:
                    break
            assert is_exist is True, "wait register element is {0}".format(is_exist)

    def wait_for_gen_register_btn_appear(self, choice_type, time_out=120):
        is_exist = self.ct_wait_exist(self.registration_button, timeout=5)
        log.info("wait register element is {0}".format(is_exist))
        if self.ct_wait_exist(self.choice_gen_app_button, timeout=10) is True:
            self.extension_init_launch_alert_with_generic_app()
        else:
            end_time = time.time() + time_out
            while time.time() < end_time:
                self.click_get_alert_ok_btn()
                if choice_type == "privapp":
                    self.click_choice_pri_app_button()
                elif choice_type == "genericapp":
                    self.click_choice_generic_app_button()
                else:
                    raise EnvironmentError("Not support")
                self.click_get_alert_ok_btn()
                is_exist = self.ct_wait_exist(self.registration_button, timeout=5)
                if is_exist:
                    break
            assert is_exist is True, "wait register element is {0}".format(is_exist)

    def click_publish_flow(self):
        self.ct_scroll_to_publish_mqtt_button()
        self.click_publish_mqtt_button()

    def click_enable_mqtt_flow(self):
        self.ct_scroll_to_enable_mqtt_btn()
        self.click_enable_mqtt_button()

    def click_disable_mqtt_flow(self):
        self.ct_scroll_to_disable_mqtt_btn()
        self.click_disable_mqtt_button()


class InvokeHttpRequest(BasePage):
    relative_url_text = AndroidElement('id',
                                       {'resourceId': 'com.lenovo.example.extensionSampleApp:id/relativeUrlEditText'})
    headers_edit_text = AndroidElement('id', {'resourceId': 'com.lenovo.example.extensionSampleApp:id/headersEditText'})
    http_method_spinner = AndroidElement('id',
                                         {'resourceId': 'com.lenovo.example.extensionSampleApp:id/httpMethodSpinner'})
    payload_edit_text = AndroidElement('id', {'resourceId': 'com.lenovo.example.extensionSampleApp:id/payloadEditText'})
    get_text = AndroidElement('id', {'resourceId': 'android:id/text1', 'text': 'GET'})
    head_text = AndroidElement('id', {'resourceId': 'android:id/text1', 'text': 'HEAD'})
    delete_text = AndroidElement('id', {'resourceId': 'android:id/text1', 'text': 'DELETE'})
    put_text = AndroidElement('id', {'resourceId': 'android:id/text1', 'text': 'PUT'})
    invoke_http_request_btn = AndroidElement('id', {'resourceId': 'com.lenovo.example.extensionSampleApp:id/button',
                                                    'text': 'INVOKE HTTP REQUEST'})

    def __init__(self, driver: Device):
        super(InvokeHttpRequest, self).__init__(driver)

    def send_keys_relative_url_text(self, text):
        if self.ct_wait_exist(self.relative_url_text, timeout=10):
            self.ct_set_text(self.relative_url_text, text=text)

    def send_keys_headers_edit_text(self, text):
        if self.ct_wait_exist(self.headers_edit_text, timeout=10):
            self.ct_set_text(self.headers_edit_text, text)

    def send_keys_payload_edit_text(self, text):
        if self.ct_wait_exist(self.payload_edit_text, timeout=10):
            self.ct_set_text(self.payload_edit_text, text)

    def click_invoke_http_request_btn(self):
        if self.ct_wait_exist(self.invoke_http_request_btn, timeout=10):
            self.ct_click(self.invoke_http_request_btn)

    def click_http_method_spinner(self):
        if self.ct_wait_exist(self.http_method_spinner, timeout=10):
            self.ct_click(self.http_method_spinner)

    def click_get_text(self):
        if self.ct_wait_exist(self.get_text, timeout=10):
            self.ct_click(self.get_text)

    def click_head_text(self):
        if self.ct_wait_exist(self.head_text, timeout=10):
            self.ct_click(self.head_text)

    def click_delete_text(self):
        if self.ct_wait_exist(self.delete_text, timeout=10):
            self.ct_click(self.delete_text)

    def click_put_text(self):
        if self.ct_wait_exist(self.put_text, timeout=10):
            self.ct_click(self.put_text)

    def choose_get_method(self):
        self.click_http_method_spinner()
        self.click_get_text()

    def choose_head_method(self):
        self.click_http_method_spinner()
        self.click_head_text()

    def choose_delete_method(self):
        self.click_http_method_spinner()
        self.click_delete_text()

    def choose_put_method(self):
        self.click_http_method_spinner()
        self.click_put_text()
