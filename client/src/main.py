import json
import pathlib
from threading import Thread

import flet
import pyrebase.pyrebase
import requests.exceptions
from flet_core import AppView


def main(page: flet.Page):
    page.theme_mode = flet.ThemeMode.SYSTEM
    page.window_center()
    page.vertical_alignment = flet.MainAxisAlignment.CENTER

    page.window_width = page.window_max_width = 700
    page.window_height = page.window_max_height = 700
    page.update()

    first_boot = not page.client_storage.contains_key('first_boot')
    if first_boot:
        def on_data_submit(e):
            data = txt_field.value

            if not data.isdigit() or data is None:
                txt_field.error_text = 'Неверный ввод данных'
                txt_field.update()
                return

            pr_ring.opacity = 1
            pr_ring.update()

            def on_firebase_init():
                def get_config_path(filename: str):
                    return pathlib.Path(__file__).cwd().joinpath(filename).resolve()

                def parse_from_file(read_file) -> str:
                    return json.load(read_file)

                def get_config(config_file_name: str) -> str:
                    src = get_config_path(config_file_name)
                    with open(src, 'r') as config_file:
                        return parse_from_file(config_file)

                config = get_config('firebase_config.json')
                firebase = pyrebase.initialize_app(config)
                user_id = int(data)
                try:
                    user = firebase.database().child('users').child(user_id).get().val()
                except requests.exceptions.ConnectionError:
                    user = None
                    txt_field.error_text = 'Отсутствие подключения к серверу'
                    txt_field.update()
                print(user)
                pr_ring.opacity = 0
                pr_ring.update()

                if user is None:
                    txt_field.error_text = 'Данный пользователь не существует'
                    txt_field.update()

            Thread(target=on_firebase_init).start()

        pr_ring = flet.ProgressRing(
            opacity=0,
            width=70,
            height=70,
            stroke_width=7,
            animate_opacity=200,
        )

        pr_container = flet.Container(
            margin=30,
            content=pr_ring,
        )

        def on_txt_field_data_changed(e):
            txt_field.error_text = ''
            txt_field.update()

        txt_field = flet.TextField(
            password=True,
            prefix_icon=flet.icons.VERIFIED_USER,
            can_reveal_password=True,
            border_color=flet.colors.BLUE_200,
            keyboard_type=flet.KeyboardType.NUMBER,
            label='Введите код пользователя',
            on_change=on_txt_field_data_changed
        )

        btn = flet.ElevatedButton(
            text='Подтвердить',
            on_click=on_data_submit,
        )

        column = flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                pr_container,
                txt_field,
                btn,
            ]
        )

        container = flet.Container(
            margin=70,
            padding=10,
            content=column,
        )

        page.add(
            container
        )


flet.app(
    target=main,
    view=AppView.FLET_APP
)
