def load_setting(key):
    # load from file
    with open('settings.txt', 'r') as file:
        lines = file.readlines()

    settings = {}
    for line in lines:
        k, value = line.strip().split('=', 1)
        settings[k] = value

    setting = settings.get(key, f'setting with key "{key}" not found')

    return setting

def save_setting(key, value):
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
