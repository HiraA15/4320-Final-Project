# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 22:51:47 2016

@author: Austin
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class TestApp(App):
    def build(self):
        return TextInput(text='Hello World')

TestApp().run()