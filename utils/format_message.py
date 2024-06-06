def format_message(message, changes):
    for key, value in changes.items():
        message = message.replace(key, value)
    return message
