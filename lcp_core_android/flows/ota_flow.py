#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: register_flow.py
@time: 8/22/2023 3:04 PM
@file_desc:
"""
import logging

from lcp_core_api.flows.apps_flow import AppsFlow
from lcp_core_android.flows.android_install_flow import AndroidInstallFlow
from lcp_core_android.flows.base_mobile_flow import BaseAndroidFlow
from utils.soft_assert import assert_equal

NoneType = type(None)
log = logging.getLogger(__name__)


class OTAFlow(BaseAndroidFlow):
    def __init__(self, auth_token, driver):
        super(OTAFlow, self).__init__(driver)
        self.apps_flow = AppsFlow(auth_token)
        self.install_flow = AndroidInstallFlow(driver)
        self.package_name = None
        self.org_app_id = None

    def add_app(self, app_name=None):
        org_app_id, package_name = self.apps_flow.add_app_flow(app_name)
        self.org_app_id = org_app_id
        self.package_name = package_name
        return org_app_id, package_name

    def delete_app(self):
        return self.apps_flow.delete_app_flow()

    def deploy_app_to_device(self, device_id):
        # Deploy app to device from UDS portal
        rsp, _ = self.apps_flow.deploy_app_to_device(device_id)
        assert rsp.status_code == 200
        # Device pops up to ask permission to trust UDC install
        exist_install = self.install_flow.click_install_btn()
        assert exist_install

    def cancel_deploy_app_to_device(self, device_id):
        # Deploy app to device from UDS portal
        rsp, _ = self.apps_flow.deploy_app_to_device(device_id)
        assert rsp.status_code == 200
        # Device pops up to ask permission to trust UDC install
        exist_install = self.install_flow.click_install_cancel_btn()
        assert exist_install

    def cancel_undeploy_app_from_device(self, device_id):
        # Undeploy app from device from UDS portal
        rsp, _ = self.apps_flow.undeploy_app_from_device(device_id)
        assert rsp.status_code == 202
        # Device pops up ask to uninstall the APK
        alert_message = self.install_flow.get_uninstall_alert_message()
        assert_equal(alert_message, "Do you want to uninstall this app?")
        self.install_flow.click_uninstall_cancel_btn()

    def deploy_app_to_device_in_silence(self, device_id):
        # Deploy app to device from UDS portal
        rsp, _ = self.apps_flow.deploy_app_to_device(device_id)
        assert rsp.status_code == 200
        # assert exist_install

    def deploy_app_to_device_in_silence_without_waiting(self, device_id):
        # Deploy app to device from UDS portal
        self.apps_flow.deploy_app_to_device_without_waiting(device_id)
        # assert rsp.status_code == 200

    def undeploy_app_from_device(self, device_id):
        # Undeploy app from device from UDS portal
        rsp, _ = self.apps_flow.undeploy_app_from_device(device_id)
        assert rsp.status_code == 202
        # Device pops up ask to uninstall the APK
        alert_message = self.install_flow.get_uninstall_alert_message()
        assert_equal(alert_message, "Do you want to uninstall this app?")
        exist_ok = self.install_flow.click_uninstall_ok_btn()
        assert exist_ok

    def undeploy_app_from_device_in_silence(self, device_id):
        # Undeploy app from device from UDS portal
        rsp, _ = self.apps_flow.undeploy_app_from_device(device_id)
        assert rsp.status_code == 202
