# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *


# app = QApplication([]) # Incia la aplicación
# window = QMainWindow() # Genera una ventana 
# window.show()
# app.exec_()            # Ejecuta la App



import json
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
import sys
import time
import datetime

# horas = 1
# def guardar_horas_estudio(horas):
#     fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
#     data = {'fecha': fecha_actual, 'horas': horas}

#     try:
#         with open('registro_estudio.json', 'w') as f:
#                 json.dump(data, f)
#     except FileNotFoundError:
#         pass  # Opcional: Manejar la excepción si es necesario
# guardar_horas_estudio(horas)







def guardar_horas_estudio(horas):
    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
    registro_nuevo = {'fecha': fecha_actual, 'horas': horas}

    # Crear la estructura de datos si el archivo no existe o está vacío
    if not os.path.exists('registro_estudio.json') or os.path.getsize('registro_estudio.json') == 0:
        data = {'fechas_y_horas': [registro_nuevo]}
    else:
        try:
            with open('registro_estudio.json', 'r') as f:
                data = json.load(f)
        except Exception as e:
            print('Error al leer el archivo:', e)
            return

        # Verificar si ya hay un registro para la fecha actual
        for registro in data['fechas_y_horas']:
            if registro['fecha'] == fecha_actual:
                print('Ya existe un registro para la fecha actual.')
                return
        
        # Agregar el nuevo registro a la lista
        data['fechas_y_horas'].append(registro_nuevo)

    # Guardar los datos actualizados en el archivo JSON
    try:
        with open('registro_estudio.json', 'w') as f:
            json.dump(data, f, indent=2)
            print('Registro guardado exitosamente.')
    except Exception as e:
        print('Error al guardar el registro:', e)

horas = 1
guardar_horas_estudio(horas)


