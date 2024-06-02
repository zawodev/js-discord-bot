import json
import os

def _load_setting(key): # deprecated
    # load from file
    with open('settings.txt', 'r') as file:
        lines = file.readlines()

    settings = {}
    for line in lines:
        k, value = line.strip().split('=', 1)
        settings[k] = value

    setting = settings.get(key, f'setting with key "{key}" not found')

    return setting

def _save_setting(key, value): # deprecated
    # load from file
    with open('settings.txt', 'r') as file:
        lines = file.readlines()

    # parse settings
    settings = {}
    for line in lines:
        k, v = line.strip().split('=', 1)
        settings[k] = v

    # update setting
    settings[key] = value

    # sort by key
    settings = dict(sorted(settings.items()))

    # save to file
    with open('settings.txt', 'w') as file:
        for k, v in settings.items():
            file.write(f'{k}={v}\n')

    print(f"saved {key}: {value}")

def load_setting_json(key):
    # create empty file if it doesn't exist
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w', encoding='utf-8') as file:
            json.dump({}, file)

    # load from file
    with open('settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)

    # get setting or return empty dict if key not found
    setting = settings.get(key, {})

    return setting

def save_setting_json(key, value):
    # create empty file if it doesn't exist
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w', encoding='utf-8') as file:
            json.dump({}, file)

    # load from file
    with open('settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)

    # update setting
    settings[key] = value

    # save to file
    with open('settings.json', 'w', encoding='utf-8') as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)
