import argparse
import asyncio
import getpass
import json
import os
import pathlib

import flet
from flet_core import AppView

from domain.di.MainAppModule import MainAppModule
from presentation.auth_screen.AuthControl import AuthControl
from presentation.main_screen.MainControl import MainControl

config_dir = None
firebase_cnfg = None
s3_cnfg = None


def get_config_path(filename: str):
    if config_dir is None:
        return pathlib.Path(__file__).cwd().joinpath('config', filename).resolve()
    return pathlib.Path(config_dir).joinpath(filename).resolve()


def parse_from_file(read_file) -> dict:
    return json.load(read_file)


def load_into_file(file, content):
    with open(file, 'w') as f:
        json.dump(content, f)


def get_config(config_file_name: str) -> dict:
    src = get_config_path(config_file_name)
    with open(src, 'r') as config_file:
        return parse_from_file(config_file)


def add_to_auto_boot():
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % getpass.getuser()
    with open(bat_path + '\\' + "data_sync_bridge.bat", "w+") as bat_file:
        cnfg_path = os.path.join(os.getenv('appdata'), 'DataSyncBridge', 'Config')
        bat_file.writelines(
            [
                f'pip install -r {os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")}',
                '\n',
                f"py -u {os.path.realpath(__file__)} --config_dir={cnfg_path}"
            ]
        )


def main(page: flet.Page):
    page.title = 'DataSyncBridge Client App'
    page.theme_mode = flet.ThemeMode.SYSTEM
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.window_width = page.window_max_width = 760
    page.window_height = page.window_max_height = 700
    page.auto_scroll = True
    page.window_center()

    MainAppModule.inject_dependencies(
        firebase_config=firebase_cnfg,
        s3_config=s3_cnfg,
        local_storage=page.client_storage,
        on_fall_back=lambda _: print('Oops')
    )

    def enter_main_screen():
        def on_navigate():
            page.controls.clear()
            enter_auth_screen()

        main_control = MainControl(
            MainAppModule.provideMainControlViewModel(), page, on_navigate
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

    if MainAppModule.provideClientLocalRepository().is_default_local_user_set():
        enter_main_screen()
    else:
        MainAppModule.provideClientLocalRepository().set_default_downloading_directory(
            os.path.join(os.getenv('appdata'), 'DataSyncBridge', 'InternalStorage')
        )

        auto_load = config_dir is not None
        if not auto_load:
            add_to_auto_boot()

            os.makedirs(os.path.join(os.getenv('appdata'), 'DataSyncBridge', 'Config'), exist_ok=True)

            load_into_file(
                os.path.join(os.getenv('appdata'), 'DataSyncBridge', 'Config', 'firebase_config.json'), firebase_cnfg
            )
            load_into_file(
                os.path.join(os.getenv('appdata'), 'DataSyncBridge', 'Config', 's3_config.json'), s3_cnfg
            )

        enter_auth_screen()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_dir')
    config_dir = parser.parse_args().config_dir

    firebase_cnfg = get_config('firebase_config.json')
    s3_cnfg = get_config('s3_config.json')
    flet.app(target=main, view=AppView.FLET_APP, name='DataSyncBridge Client App')
