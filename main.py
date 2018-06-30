#coding: utf-8

#author: Aderbal Machado Ribeiro

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

class Login(Screen):

    def login(self):

        #if self.ids.login.text == "real" and self.ids.passw.text == "real@1480":
        self.manager.current = "Destrava"

class Destrava(Screen):

    def destrava(self):

        self.ids.msg.text = "Destrava\r\nBlackout"

class ScreenManagement(ScreenManager):

    pass

class BlackoutApp(App):

    def on_stop(self):

        Window.close()

if __name__ == '__main__': BlackoutApp().run()