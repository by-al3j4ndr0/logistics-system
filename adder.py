from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldMaxLengthText,
    MDTextFieldHelperText,
)

from kivymd.uix.screen import MDScreen
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import (
    MDButton,
    MDButtonText,
)

from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogButtonContainer,
)

from kivy.uix.widget import Widget

import pandas as pd

class Adder(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = pd.read_csv("database.csv", index_col=False)
        self.df = pd.DataFrame(self.database)
        self.insert_layout()
        self.add_widget(self.icl)

    def insert_layout(self):
        self.icl = MDRelativeLayout()

        self.insert_label = MDLabel(
                text="Agregar contenedor",
                halign="left",
                font_style = "Headline",
                role = "small",
                pos_hint={"x": 0.05, "center_y": 0.93},
        )
        self.number = MDTextField(
                MDTextFieldHintText(
                    text="Contenedor No.",
                ),
                MDTextFieldMaxLengthText(
                    max_text_length=11,
                ),
                mode="outlined",
                size_hint_x=None,
                width="320dp",
                pos_hint={"center_x": 0.25, "center_y": 0.83},
        )
        self.client = MDTextField(
                MDTextFieldHintText(
                    text="Cliente",
                ),
                mode="outlined",
                size_hint_x=None,
                width="320dp",
                pos_hint={"center_x": 0.75, "center_y": 0.83},
        )
        self.ext_date = MDTextField(
                MDTextFieldHintText(
                    text = "Fecha de Extraccion",
                ),
                MDTextFieldHelperText(
                    text = "DD/MM/YYYY",
                    mode = "persistent",
                ),
                mode = "outlined",
                validator = "date",
                date_format = "dd/mm/yyyy",
                pos_hint={"center_x": 0.2, "center_y": 0.66},
                size_hint_x = .3,
        )
        self.ext_driver = MDTextField(
                MDTextFieldHintText(
                    text="Chofer Extraccion",
                ),
                mode="outlined",
                size_hint_x=None,
                width="440dp",
                pos_hint={"center_x": 0.675, "center_y": 0.66},
        )
        self.dev_date = MDTextField(
                MDTextFieldHintText(
                    text = "Fecha de Devolucion",
                ),
                MDTextFieldHelperText(
                    text = "DD/MM/YYYY",
                    mode = "persistent",
                ),
                mode = "outlined",
                validator = "date",
                date_format = "dd/mm/yyyy",
                pos_hint={"center_x": 0.2, "center_y": 0.48},
                size_hint_x = .3,
        )
        self.dev_driver = MDTextField(
                MDTextFieldHintText(
                    text="Chofer Devolucion",
                ),
                mode="outlined",
                size_hint_x=None,
                width="440dp",
                pos_hint={"center_x": 0.675, "center_y": 0.48},
        )
        self.add_button = MDButton(
                MDButtonText(
                    text = "Agregar",
                ),
                pos_hint ={"center_x": 0.73, "center_y": 0.33},
                on_release = lambda x: self.insert(self.number.text, 
                                                self.client.text, 
                                                self.ext_date.text, 
                                                self.ext_driver.text, 
                                                self.dev_date.text, 
                                                self.dev_driver.text
                                                ),
        )
        self.update_button = MDButton(
                MDButtonText(
                    text = "Actualizar",
                ),
                pos_hint ={"center_x": 0.875, "center_y": 0.33},
                on_release = lambda x: self.update(self.number.text, 
                                                self.client.text, 
                                                self.ext_date.text, 
                                                self.ext_driver.text, 
                                                self.dev_date.text, 
                                                self.dev_driver.text
                                                ),
        )

        self.icl.add_widget(self.insert_label)
        self.icl.add_widget(self.number)
        self.icl.add_widget(self.client)
        self.icl.add_widget(self.ext_date)
        self.icl.add_widget(self.ext_driver)
        self.icl.add_widget(self.dev_date)
        self.icl.add_widget(self.dev_driver)
        self.icl.add_widget(self.add_button)
        self.icl.add_widget(self.update_button)
    
    def insert(self, number, client, ext_date, ext_driver, dev_date, dev_driver):
        if dev_date == "":
            dev_date = "--/--/----"

        if self.check_container(number) == True:
            self.show_exist_dialog(True)
        else:
            self.df.loc[len(self.df)] = (number, client, ext_date, ext_driver, dev_date, dev_driver)
            self.df.to_csv("database.csv", index=False)

    def update(self, number, client, ext_date, ext_driver, dev_date, dev_driver):
        if dev_date == "":
            dev_date = "--/--/----"

        if self.check_container(number) == False:
            self.show_exist_dialog(False)
        else:
            if client != "":
                self.df.loc[self.df["number"] == number, "client"] = client
            if ext_date != "":
                self.df.loc[self.df["number"] == number, "ext_date"] = ext_date
            if ext_driver != "":
                self.df.loc[self.df["number"] == number, "ext_driver"] = ext_driver
            if dev_date != "":
                self.df.loc[self.df["number"] == number, "dev_date"] = dev_date
            if dev_driver != "":
                self.df.loc[self.df["number"] == number, "dev_driver"] = dev_driver
            self.df.to_csv("database.csv", index=False)
            
    def show_exist_dialog(self, existance):
        def close_dialog(obj):
            dialog.dismiss()
            
        if existance == True:
            exist_text = "El contenedor especificado ya existe"
        elif existance == False:
            exist_text = "El contenedor especificado no existe"

        dialog = MDDialog(
            MDDialogIcon(
                icon = "alert",
            ),
            MDDialogHeadlineText(
                text = exist_text,
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Aceptar"),
                    style="text",
                    on_release = close_dialog
                ),
                spacing="8dp",
            ),
        )
        dialog.open()

    def check_container(self, number):
        existance = False

        for i in range(0, len(self.df)):
            if number in self.df.at[i, "number"]:
                existance = True
                break
            
        return existance