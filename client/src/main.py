import asyncio
import json
import os
import pathlib

import flet
from flet_core import AppView, FilePicker

from domain.di.MainAppModule import MainAppModule
from presentation.auth_screen.AuthControl import AuthControl
from presentation.main_screen.MainControl import MainControl


def get_config_path(filename: str):
    return pathlib.Path(__file__).cwd().joinpath('config', filename).resolve()


def parse_from_file(read_file) -> dict:
    return json.load(read_file)


def get_config(config_file_name: str) -> dict:
    src = get_config_path(config_file_name)
    with open(src, 'r') as config_file:
        return parse_from_file(config_file)


def main(page: flet.Page):
    page.theme_mode = flet.ThemeMode.SYSTEM
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.window_width = page.window_max_width = 760
    page.window_height = page.window_max_height = 700
    page.window_center()

    file_picker = FilePicker()
    page.overlay.append(file_picker)

    firebase_cnfg = get_config('firebase_config.json')
    s3_cnfg = get_config('s3_config.json')

    MainAppModule.inject_dependencies(
        firebase_config=firebase_cnfg,
        s3_config=s3_cnfg,
        local_storage=page.client_storage
    )

    def enter_main_screen():
        def on_navigate():
            page.controls.clear()
            enter_auth_screen()

        main_control = MainControl(
            MainAppModule.provideMainControlViewModel(), page, file_picker, on_navigate
        )

        page.add(main_control)
        main_control.opacity = 1

        async def animate_boot():
            await asyncio.sleep(0.2)
            page.update()

        asyncio.run(
            animate_boot()
        )

    def enter_auth_screen():
        def on_navigate():
            page.controls.clear()
            enter_main_screen()

        auth_control = AuthControl(
            MainAppModule.provideAuthControlViewModel(), page, on_navigate
        )

        page.add(auth_control)
        auth_control.opacity = 1

        async def animate_boot():
            await asyncio.sleep(0.2)
            page.update()

        asyncio.run(
            animate_boot()
        )

    if MainAppModule.provideClientLocalRepository().is_user_set():
        enter_main_screen()
    else:
        MainAppModule.provideClientLocalRepository().set_default_downloading_directory(
            os.getcwd()
        )
        enter_auth_screen()


if __name__ == "__main__":
    flet.app(target=main, view=AppView.FLET_APP, name='DataSyncBridge Client App')
