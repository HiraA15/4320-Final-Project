# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 22:51:47 2016

@author: Austin
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.pagelayout import PageLayout
from kivy.uix.scrollview import ScrollView

def ResultsView():
    view = ModalView(auto_dismiss=False)
    button = Button(text = "Return", size_hint=(.2,.1))
    
    button.bind(on_press=view.dismiss)
    
    layout = BoxLayout(orientation='vertical')
    resultsDisplay = PageLayout()
    resultsDisplay.add_widget(Button(text="0n3"))
    resultsDisplay.add_widget(Button(text="two"))
    resultsDisplay.add_widget(Button(text="thr33"))
    
    layout.add_widget(button)
    layout.add_widget(resultsDisplay)
    
    
    view.add_widget(layout)  
    
    return view

class MainView(Widget):
    pass

class TestApp(App):
    def build(self):
        rView = ResultsView()
        
        button = Button(text="Hello") 
        button.bind(on_press = rView.open)
        
        mainView = button 
        
        return mainView
    

TestApp().run()