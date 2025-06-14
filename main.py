import os
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import requests
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

USER_FILE = 'user_data.json'

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
                if os.path.exists(USER_FILE):
                    os.remove(USER_FILE)
        return sm

    def on_start(self):
        self.load_orders()  # <- ide kerül át

    def search_barcode(self):
        screen = self.root.get_screen('main')  # mindig így!
        barcode = screen.ids.barcode_input.text.strip()
        if not barcode:
            screen.ids.result_label.text = "Adja meg a vonalkódot!"
            return 
        try:
            response = requests.get("http://localhost/raktar_api/api.php", params={"barcode": barcode})
            data = response.json()
            if data.get("found"):
                screen.ids.result_label.text = f"Termék: {data['name']} \nMegrendelő: {data['owner']}"
            else:
                screen.ids.result_label.text = "Termék nem található."
        except Exception as e:
            screen.ids.result_label.text = f"Hiba: {str(e)}"

    def load_orders(self):
        try:
            response = requests.get("http://localhost/raktar_api/orders.php?direction=outgoing")
            data = response.json()

            order_list = self.root.get_screen('main').ids.order_list
            order_list.clear_widgets()

            for item in data.get("orders", []):
                label = Label(text=f"{item['barcode']} - {item['name']} ({item['owner']})")
                order_list.add_widget(label)

            self.root.get_screen('main').ids.result_label.text = "Rendelések betöltve."
        except Exception as e:  
            self.root.get_screen('main').ids.result_label.text = f"Hiba: {str(e)}"

    def delete_orders(self):
        screen = self.root.get_screen('main')
        barcode = screen.ids.barcode_input.text.strip()

        if not barcode :
            screen.ids.result_label.text = "Nincs beolvasott vonalkód!"
            return
        
        try:
            response = requests.post("http://localhost/raktar_api/confirmation.php", data={"barcode": barcode})
            data = response.json()

            if data.get("success"):
                screen.ids.result_label.text = f"Termék ({barcode}) státusza: KISZÁLLÍTVA"
                screen.ids.barcode_input.text = ''
                self.load_orders()  # frissíti a listát
            else:
                screen.ids.result_label.text = f"Hiba: {data.get('error', 'Ismeretlen')}"
        except Exception as e:
            screen.ids.result_label.text = f"Hálózati hiba: {str(e)}"

    CONFIG_FILE = 'config.json'

    def save_config(self, api_url):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({'api_url': api_url}, f)
            print("Konfiguráció mentve.")
        except Exception as e:
            print(f"Hiba konfiguráció mentésekor: {e}")

if __name__ == '__main__':
    RaktarApp().run()
