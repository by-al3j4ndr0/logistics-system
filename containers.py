from kivymd.uix.list import (
    MDListItem, 
    MDListItemHeadlineText,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
    MDListItemTertiaryText,
    MDList,
)

from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldMaxLengthText,
)

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout

from kivy.uix.scrollview import ScrollView

import pandas as pd
    
class Containers(MDScreen):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = pd.read_csv("database.csv")
        self.df = pd.DataFrame(self.database)
        self.main_layout = MDFloatLayout()
        self.list_layout()
        self.search_layout()
        self.add_widget(self.main_layout)

    def list_layout(self):
        self.scroll = ScrollView(pos_hint={"x": 0.03, "center_y": 0.3},)
        self.main_layout.add_widget(self.scroll)
        self.lcl = MDList()
        self.scroll.add_widget(self.lcl)

        for index, row in self.df.iterrows():
            containers = MDListItem(
                MDListItemLeadingIcon(
                    icon="truck-cargo-container",
                ),
                MDListItemHeadlineText(
                    text="No. " + str(row["number"]),
                ),
                MDListItemSupportingText(
                    text="Cliente: " + str(row["client"]),
                ),
                MDListItemTertiaryText(
                    text="Extraccion: " + str(row["ext_date"]) + " | " + str(row["ext_driver"]) + 
                        "\nDevolucion: " + str(row["dev_date"]) + " | " + str(row["dev_driver"]),
                    adaptive_size = True,
                ),
            )
            self.lcl.add_widget(containers)

    def search_layout(self):
        self.search_field = MDTextField(
            MDTextFieldHintText(
                text="Contenedor No.",
            ),
            MDTextFieldMaxLengthText(
                max_text_length=11,
            ),
            mode="outlined",
            size_hint_x=None,
            width="320dp",
            pos_hint={"x": 0.05, "center_y": 0.9},
        )
        self.search_button = MDButton(
            MDButtonText(
                text = "Buscar",
            ),
            pos_hint ={"center_x": 0.55, "center_y": 0.9},
            on_release = lambda x: self.search_function(self.search_field.text)
        )
        self.clear_button = MDButton(
            MDButtonText(
                text = "Limpiar",
            ),
            pos_hint ={"center_x": 0.68, "center_y": 0.9},
            on_release = lambda x: self.clear_function()
        )

        self.main_layout.add_widget(self.search_field)
        self.main_layout.add_widget(self.search_button)
        self.main_layout.add_widget(self.clear_button)

    def search_function(self, search_value):
        if search_value == "":
            self.lcl.clear_widgets()
            self.list_layout()
        else:
            matches = self.df.apply(lambda col: col.astype(str).str.contains(search_value, case=False))
            rows, cols = matches.values.nonzero()

            self.lcl.clear_widgets()

            for row, col in zip(rows, cols):
                containers = MDListItem(
                    MDListItemLeadingIcon(
                        icon="truck-cargo-container",
                    ),
                    MDListItemHeadlineText(
                        text="No. " + str(self.df.at[row, "number"]),
                    ),
                    MDListItemSupportingText(
                        text="Cliente: " + str(self.df.at[row, "client"]),
                    ),
                    MDListItemTertiaryText(
                        text="Extraccion: " + str(self.df.at[row, "ext_date"]) + " | " + str(self.df.at[row, "ext_driver"]) + 
                            "\nDevolucion: " + str(self.df.at[row, "dev_date"]) + " | " + str(self.df.at[row, "dev_driver"]),
                        adaptive_size = True,
                    ),
                )
                self.lcl.add_widget(containers)

    def clear_function(self):
        self.search_field.text = ""
        self.lcl.clear_widgets()
        self.list_layout()