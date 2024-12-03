from kivy.properties import StringProperty

from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemLabel,
    MDNavigationItemIcon,
)
from kivymd.app import MDApp

from containers import Containers
from adder import Adder

class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))


class Logistics(MDApp):
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        self.root.get_ids().screen_manager.current = item_text

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Olive"
        return MDBoxLayout(
            MDScreenManager(
                Containers(
                    name="Contenedores"
                ),
                Adder(
                    name="Agregar",
                ),
                id="screen_manager",
            ),
            MDNavigationBar(
                BaseMDNavigationItem(
                    icon="truck-cargo-container",
                    text="Contenedores",
                    active=True,
                ),
                BaseMDNavigationItem(
                    icon="ticket-outline",
                    text="Agregar",
                ),
                on_switch_tabs=self.on_switch_tabs,
            ),
            orientation="vertical",
            md_bg_color=self.theme_cls.backgroundColor,
        )

Logistics().run()