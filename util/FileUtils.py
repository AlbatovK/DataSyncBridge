import json
import os
import pathlib


def get_config_path(filename: str):
    return pathlib.Path(__file__).cwd().joinpath('config', filename).resolve()


def get_config(config_file_name: str) -> str:
    src = get_config_path(config_file_name)
    with open(src, 'r') as config_file:
        return parse_from_file(config_file)


def parse_from_file(read_file) -> str:
    return json.load(read_file)


def get_s3_config():
    return get_config('s3_config.json')


def get_firebase_config():
    return get_config('firebase_config.json')


def get_bot_config():
    return get_config('bot_config.json')


def delete_file(filepath):
    os.remove(filepath)


def get_absolute_cwd():
    return pathlib.Path(__file__).cwd().resolve()


def clear_photo(filename: str):
    delete_file(
        get_absolute_cwd().joinpath(filename).resolve()
    )
