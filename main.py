from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import requests
from kivy.uix.label import Label

class MainScreen(BoxLayout):
    pass

class RaktarApp(App):
    def build(self):
        Builder.load_file('ui.kv')
        self.root = MainScreen()
        return self.root

    def on_start(self):
        self.load_orders()  # <- ide kerül át

    def search_barcode(self):
        barcode = self.root.ids.barcode_input.text.strip()
        if not barcode:
            self.root.ids.result_label.text = "Adja meg a vonalkódot!"
            return 
        try:
            response = requests.get("http://localhost/raktar_api/api.php", params={"barcode": barcode})
            data = response.json()
            if data.get("found"):
                self.root.ids.result_label.text = f"Termék: {data['name']} \n Megrendelő: {data['owner']}"
            else:
                self.root.ids.result_label.text = "Termék nem található."
        except Exception as e:
            self.root.ids.result_label.text = f"Hiba: {str(e)}"

    def load_orders(self):
        try:
            response = requests.get("http://localhost/raktar_api/orders.php?direction=outgoing")
            data = response.json()

            order_list = self.root.ids.order_list
            order_list.clear_widgets()

            for item in data.get("orders", []):
                label = Label(text=f"{item['barcode']} - {item['name']} ({item['owner']})")
                order_list.add_widget(label)

            self.root.ids.result_label.text = "Rendelések betöltve."
        except Exception as e:  
            self.root.ids.result_label.text = f"Hiba: {str(e)}"


if __name__ == '__main__':
    RaktarApp().run()
