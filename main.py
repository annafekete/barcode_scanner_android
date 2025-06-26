import os
import json
import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button

from config import USER_FILE, CONFIG_FILE, DEFAULT_API_URL
from utils import log_error


class LoginScreen(Screen):
    def login(self):
        username = self.ids.username.text.strip()
        if username:
            is_admin = username.lower() == "admin"
            with open(USER_FILE, 'w') as f:
                json.dump({'username': username, 'admin': is_admin}, f)
            self.manager.current = 'menu'
        else:
            self.ids.status.text = "Név megadása kötelező!"


class MenuScreen(Screen):
    def on_pre_enter(self):
        if os.path.exists(USER_FILE):
            with open(USER_FILE) as f:
                data = json.load(f)
                if data.get('admin'):
                    self.ids.settings_button.opacity = 1
                    self.ids.settings_button.disabled = False
                else:
                    self.ids.settings_button.opacity = 0
                    self.ids.settings_button.disabled = True

    def logout(self):
        if os.path.exists(USER_FILE):
            os.remove(USER_FILE)
        self.manager.current = 'login'


class SettingsScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class RaktarApp(App):
    def build(self):
        Builder.load_file('ui.kv')
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))

        if os.path.exists(USER_FILE):
            try:
                with open(USER_FILE) as f:
                    data = json.load(f)
                    if data.get('username'):
                        sm.current = 'menu'
            except Exception as e:
                print("Hibás user_data.json, törlés...")
                os.remove(USER_FILE)

        return sm

    def on_start(self):
        self.load_orders()

    def get_api_url(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE) as f:
                    data = json.load(f)
                    return data.get('api_url', DEFAULT_API_URL)
            except Exception as e:
                print(f"Nem sikerült beolvasni a konfigurációt: {e}")
        return DEFAULT_API_URL

    def search_barcode(self):
        screen = self.root.get_screen('main')
        barcode = screen.ids.barcode_input.text.strip()
        result_label = screen.ids.result_label
        result_container = screen.ids.barcode_results

        if not barcode:
            result_label.text = "Adja meg a vonalkódot!"
            return

        result_container.clear_widgets()

        try:
            api_url = self.get_api_url()
            response = requests.get(f"{api_url}/api.php", params={"ALKAT": barcode})
            data = response.json()

            if data.get("found") and "items" in data:
                result_label.text = f"{len(data['items'])} találat:"
                for item in data["items"]:
                    btn = Button(
                        text=f"{item['name']} ({item['id']})",
                        size_hint_y=None,
                        height=40,
                        on_press=lambda btn, i=item: self.select_item(i)
                    )
                    result_container.add_widget(btn)
            else:
                result_label.text = "Termék nem található."
        except Exception as e:
            result_label.text = log_error(e, "Vonalkód keresés")

    def select_item(self, item):
        screen = self.root.get_screen('main')
        screen.ids.result_label.text = f"Kiválasztott termék:\n{item['name']} ({item['id']})"

    def load_orders(self):
        try:
            api_url = self.get_api_url()
            response = requests.get(f"{api_url}/orders.php")
            if response.status_code != 200:
                raise Exception(f"Hibás státuszkód: {response.status_code}")

            try:
                data = response.json()
            except json.JSONDecodeError:
                raise Exception(f"Nem JSON válasz: {response.text}")

            order_list = self.root.get_screen('main').ids.order_list
            order_list.clear_widgets()

            for item in data.get("orders", []):
                label = Label(text=f"{item['HNEV']} - {item['TAZ']} ({item['ALKAT']})")
                order_list.add_widget(label)

            self.root.get_screen('main').ids.result_label.text = "Rendelések betöltve."
        except Exception as e:
            self.root.get_screen('main').ids.result_label.text = log_error(e, "Termékek betöltése")

    def save_config(self, api_url):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({'api_url': api_url}, f)
            print("Konfiguráció mentve.")
        except Exception as e:
            log_error(e, "Konfiguráció mentése")


if __name__ == '__main__':
    RaktarApp().run()
