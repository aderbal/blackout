#coding: utf-8

#author: Aderbal Machado Ribeiro

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import dp
from zbarcam import ZBarCam

import base64


class Login(Screen):

    h = None

    def __init__(self, **kwargs):

        super(Login, self).__init__(**kwargs)

        if platform in ('linux', 'windows', 'macosx'):
            self.h = dp(39)
        else:
            self.h = dp(29)

    def login(self):

        if self.ids.login.text == "real" and self.ids.passw.text == "real@1480":
            self.manager.current = "Destrava"
        else:
            self.ids.msg.text = "Usuário e/ou Senha Invalido(a)s"


class Destrava(Screen):

    h = None

    def __init__(self, **kwargs):

        super(Destrava, self).__init__(**kwargs)

        if platform in ('linux', 'windows', 'macosx'):
            self.h = dp(39)
        else:
            self.h = dp(27)

    def money(self, st="", r=True):

        st = "{:,.2f}".format(float(st))

        if not r: st = st.replace(".00", "")

        return "{}{}".format("R$ " if r else "", st.replace(",", "#").replace(".", ",").replace("#", "."))

    def ligar_qrcode(self, zbarcam=None):

        if zbarcam:
            self.ids.zbarcam.height = dp(self.height)
            zbarcam.start()

    def desligar_qrcode(self, zbarcam=None):

        if zbarcam:
            self.ids.zbarcam.height = dp(0)
            zbarcam.stop()

    def zbar(self, zbarcam=None, symbols=None):

        if zbarcam and symbols:
            ret = ', '.join([str(symbol.data) for symbol in symbols])
            self.desligar_qrcode(zbarcam=zbarcam)
        else:
            ret = self.ids.texto.text

        return ret

    def text(self, text):

        if text: self.destrava()

    def ultima(self):

        try:
            texto = open('crypt', 'r').read()
        except:
            texto = ""

        self.ids.texto.text = texto

    def destrava(self):

        botoes = {"a": "bola extra", "b": "troca numeros",  "c": "abre cartelas",  "d": "mais",
                  "e": "jogar", "f": "apostar", "g": "ajuda", "h": "menos", "j": "cobrar"}

        try:
            texto = base64.b64decode(self.ids.texto.text.replace("@", "I").replace("#", "l")).split(" ")
            self.ids.msg.text = """Casa: {} Numero: {}\n
Creditos:\n
    Cofre: {} Entrada: {} Saida: {} Saldo: {}
    Bonus: {} Percentual: {} % Entrada: {} Saida: {} Saldo: {}\n
Dinheiro:\n
    Cofre: {} Entrada: {} Saida: {} Saldo: {}
    Bonus: {} Percentual: {} % Entrada: {} Saida: {} Saldo: {}\n
Sequencia de botoes para o desbloqueio:\n
    {} ({}) {} ({}) {} ({}) {} ({}) {} ({})""".format(texto[0].split("_")[1],
                                                      texto[0].split("_")[0],
                                                      self.money(st=texto[1], r=False),
                                                      self.money(st=texto[2], r=False),
                                                      self.money(st=texto[3], r=False),
                                                      self.money(st=float(texto[2])-float(texto[3]), r=False),
                                                      self.money(st=texto[4], r=False),
                                                      self.money(st=texto[5], r=False),
                                                      self.money(st=texto[6], r=False),
                                                      self.money(st=texto[7], r=False),
                                                      self.money(st=float(texto[7])-float(texto[7]), r=False),
                                                      self.money(st=float(texto[1])/4),
                                                      self.money(st=float(texto[2])/4),
                                                      self.money(st=float(texto[3])/4),
                                                      self.money(st=(float(texto[2])-float(texto[3]))/4),
                                                      self.money(st=float(texto[4])/4),
                                                      self.money(st=float(texto[5])/4, r=False),
                                                      self.money(st=float(texto[6])/4, r=False),
                                                      self.money(st=float(texto[7])/4, r=False),
                                                      self.money(st=(float(texto[6])-float(texto[7]))/4, r=False),
                                                      botoes[texto[8]],  texto[8],
                                                      botoes[texto[9]],  texto[9],
                                                      botoes[texto[10]], texto[10],
                                                      botoes[texto[11]], texto[11],
                                                      botoes[texto[12]], texto[12])
            with open("crypt", 'w') as f: f.write(self.ids.texto.text)
        except:
            self.ids.msg.text = "Texto Invalido"


class ScreenManagement(ScreenManager):

    pass


class BlackoutApp(App):

    def __init__(self, **kwargs):

        super(BlackoutApp, self).__init__(**kwargs)

        if platform in ('linux', 'windows', 'macosx'): Window.size = (1200, 640)

    def on_stop(self):

        Window.close()

if __name__ == '__main__': BlackoutApp().run()