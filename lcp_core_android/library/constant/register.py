#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youwp1@lenovo.com
@file: register.py
@time: 8/31/2023 9:03 AM
@file_desc:
"""


class Register:
    def __init__(self, language: str = 'zh'):
        if hasattr(self, f"_{self.__class__.__name__}__{self.__class__.__name__}{language.upper()}"):
            self.register = getattr(self, f"_{self.__class__.__name__}__{self.__class__.__name__}{language.upper()}")

    class __RegisterEN:
        INSTRUCTION = "Follow these steps to complete the registration and configuration process."
        AGREEMENTS = "AGREEMENTS"
        DEVICE_ADMIN = "DEVICE ADMIN"
        APP_PERMISSION = "APP PERMISSION"
        DEVICE_OFFLINE = "Device is offline"
        REGISTER_SUCCESS = "Registration Successful"
        REGISTER_FAIL = "Registration failed"
        CHECK_FOR_UPDATES = "CHECK FOR UPDATES"

    class __RegisterZH:
        REGISTER_SUCCESS = "注册成功"
        REGISTER_FAIL = "注册失败"
