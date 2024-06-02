from PyQt5.QtGui import QPixmap, QImage
import requests
from PyQt5.QtCore import Qt

def url_to_pixmap(url, size_x, size_y):
    if not url:
        return QPixmap("control_app/discordgrey.png").scaled(size_x, size_y, Qt.KeepAspectRatio)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image = QImage()
            image.loadFromData(response.content)
            return QPixmap(image).scaled(size_x, size_y, Qt.KeepAspectRatio)
    except Exception as e:
        print(f'error loading avatar: {e}')
    return QPixmap("control_app/discordgrey.png").scaled(size_x, size_y, Qt.KeepAspectRatio)
