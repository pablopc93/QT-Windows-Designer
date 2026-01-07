from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt

'''
Etiqueta de imagen que puede detectar clics del ratón
'''

class ClickeableLabel(QLabel):
    '''
    Clase personalizada que extiende QLabel para detectar clics del ratón

    Defino la señal de clickear, que tmb la tienen los labels
    '''
    clicked = Signal()

    '''
    constructor de la clase
    '''
    def __init__(self, parent=None):
        super().__init__(parent)

    '''
    Este evento detecta cuando presiono el botón izquierdo del ratón
    y emite la señal clicked definida arriba
    '''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            '''
            Emito la señal clicked cuando se detecta un clic izquierdo
            '''
            self.clicked.emit()
        super().mousePressEvent(event)