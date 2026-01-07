import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox,QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QPixmap

from etiqueta_clicable import ClickeableLabel 

'''
Documentación:
Este programa carga una interfaz gráfica desde un archivo .ui que contiene varias etiquetas de imagen clicables
'''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        '''
        configuración inicial de la ventana (posición y tamaño)
        abro en la posición (100, 100) con un tamaño de 800x700
        '''
        self.setGeometry(100, 100, 800, 700)
        self.setWindowTitle("Pokedex Viewer")

        '''
        1. Cargar el archivo .ui
        Compruebo que el archivo se abre correctamente, si no, muestro un error y salgo
        2. Cargo la interfaz usando QUiLoader
        '''
        ui_file_name = "EjercicioFotos.ui"
        ui_file = QFile(ui_file_name)

        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Error: No se pudo abrir el archivo {ui_file_name}")
            sys.exit(-1)

        loader = QUiLoader()
        
        '''
        Registro la clase personalizada ClickeableLabel para que el cargador pueda reconocerla
        al cargar el archivo .ui que la contiene.
        '''
        loader.registerCustomWidget(ClickeableLabel)
        
        '''
        Cargo la interfaz desde el archivo .ui
        y la almaceno en una variable temporal window_cargada
        '''
        window_cargada = loader.load(ui_file)
        ui_file.close()

        '''
        Importo la barra de menú y el widget central desde la interfaz cargada
        se mueven manualmente porque estamos cargando una QMainWindow dentro de otra
        '''
        self.setMenuBar(window_cargada.menuBar()) 

        '''
        Establezco el widget central de la ventana principal
        Intento coger el widget central del diseño cargado. Si no existe, uso el widget completo.
        '''
        try:
            self.setCentralWidget(window_cargada.centralWidget())
        except AttributeError:
            self.setCentralWidget(window_cargada)
        
        '''
        Guardo la referencia de la interfaz cargada en self.ui para usarla luego
        Conecto las acciones del menú a sus funciones correspondientes
        '''
        self.ui = window_cargada

        self.ui.findChild(QAction, "actionAbout").triggered.connect(self.mostrar_informacion)
        self.ui.findChild(QAction, "actionGuardar").triggered.connect(self.abrir_navegador)
        
        '''
        Lista de pokemons (etiquetas clicables)
        Añado las etiquetas clicables a una lista para conectarlas
        '''
        self.mis_pokemons = [                
            self.ui.poke_1, 
            self.ui.poke_2, 
            self.ui.poke_3, 
            self.ui.poke_4,
            self.ui.poke_5, 
            self.ui.poke_6, 
            self.ui.poke_7, 
            self.ui.poke_8,
            self.ui.poke_9, 
            self.ui.poke_10,
            self.ui.poke_11, 
            self.ui.poke_12
        ]

        '''
        Conecto todos los pokemons a la función cambiar_foto cuando se hace clic en ellos
        También cambio el cursor a una mano para indicar que son clicables
        '''
        for pokemon in self.mis_pokemons:

            pokemon.clicked.connect(self.cambiar_foto)
            pokemon.setCursor(Qt.PointingHandCursor)

    '''
    Metodo que muestra un mensaje de información al hacer clic en About del menú
    '''
    def mostrar_informacion(self):
        QMessageBox.about(self, 
                          "Acerca de Pokedex", 
                          "Esta es una Pokedex creada con PySide6.\n\n"
                          "Selecciona un Pokémon de la lista inferior para verlo en grande.")

    '''
    Metodo para abrir el navegador de carpetas y seleccionar una carpeta
    Mostramos tambien la carpeta seleccionada en un mensaje informativo
    '''
    def abrir_navegador(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Open Folder")
        if carpeta:
            QMessageBox.information(self, "Carpeta", f"Carpeta seleccionada:\n{carpeta}")


    '''
    Metodo que cambia la foto grande por la del pokemon clicado
    Y Al seleccionar una carpeta de imagenes la añado al programa
    '''
    def abrir_navegador(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        
        if carpeta:
            '''
            Listo todo el proceso de carga de imágenes desde la carpeta seleccionada
            '''
            archivos = os.listdir(carpeta)
            
            '''
            Filtro solo los archivos de imagen comunes            
            '''
            imagenes = [f for f in archivos if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            '''
            Ordeno las imágenes alfabéticamente
            '''
            imagenes.sort()

            '''
            Limpio las etiquetas antiguas y cargo las nuevas imágenes
            '''
            for etiqueta in self.mis_pokemons:
                etiqueta.clear()

            '''
            Voy rellenandno las etiquetas con las fotos encontradas
            Uso 'zip' para juntar la lista de tus etiquetas con la lista de fotos
            '''
            for etiqueta, nombre_foto in zip(self.mis_pokemons, imagenes):
                
                ruta_completa = os.path.join(carpeta, nombre_foto)
                pixmap_nuevo = QPixmap(ruta_completa)
                
                if not pixmap_nuevo.isNull():
                    etiqueta.setPixmap(pixmap_nuevo)
            
            QMessageBox.information(self, "Carga Completada", f"Se han cargado {len(imagenes)} fotos.")

    '''
    Metodo que cambia la foto grande por la del pokemon clicado

    label_clicado: etiqueta que ha sido clicada
    imagen_origen: imagen del label clicado
    '''
    def cambiar_foto(self):
        label_clicado = self.sender()
        imagen_origen = label_clicado.pixmap()
        
        '''
        Escalo la imagen al tamaño del label grande manteniendo la proporción
        y la asigno al label grande
        '''
        if imagen_origen:
            w = self.ui.foto_grande.width()
            h = self.ui.foto_grande.height()
            imagen_escalada = imagen_origen.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.foto_grande.setPixmap(imagen_escalada)
            self.ui.foto_grande.setAlignment(Qt.AlignCenter)
'''
Ejecución de la aplicación
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())