from tkinter import *
import time
import threading

raiz = Tk()
miFrame = Frame(raiz)
miFrame.pack()

milisegundos = StringVar()

pantalla = Entry(miFrame, textvariable=milisegundos)
pantalla.grid(row=1, column=2, padx=5, pady=7, columnspan=3, rowspan=2)

# Variable para almacenar la hora ingresada en formato "horas:minutos:segundos"
hora_ingresada = StringVar()
pantalla_hora = Entry(miFrame, textvariable=hora_ingresada)
pantalla_hora.grid(row=4, column=2, padx=5, pady=7, columnspan=3)
pantalla.config(background="black", fg = '#03f943')

# Variables globales para controlar el cronómetro
cronometro_activo = False  # El cronómetro no inicia automáticamente
inicio = None
tiempo_pausado = 0
cronometro_thread = None


def obtener_tiempo_formateado(tiempo_ms):
    # Descomponer el tiempo transcurrido en horas, minutos, segundos y milisegundos
    horas, ms_restantes = divmod(tiempo_ms, 3600000)  # 1 hora = 3600000 ms
    minutos, ms_restantes = divmod(ms_restantes, 60000)  # 1 minuto = 60000 ms
    segundos, milisegundos = divmod(ms_restantes, 1000)

    return f"{horas:02d}:{minutos:02d}:{segundos:02d}.{milisegundos:02d}"


def convertir_a_milisegundos(hora_str):
    # Convertir la hora en formato "horas:minutos:segundos" a milisegundos
    try:
        horas, minutos, segundos = map(int, hora_str.split(":"))
        return (horas * 3600 + minutos * 60 + segundos) * 1000
    except ValueError:
        return 0


def cronometro():
    global inicio, tiempo_pausado

    while True:
        if cronometro_activo:  # El cronómetro solo cuenta cuando cronometro_activo es True
            if inicio is None:
                inicio = time.time() - tiempo_pausado
            else:
                tiempo_actual = time.time()
                tiempo_pausado = tiempo_actual - inicio

            ms_actual = int(tiempo_pausado * 1000)
            tiempo_formateado = obtener_tiempo_formateado(ms_actual)
            milisegundos.set(f"Time: {tiempo_formateado}")
        time.sleep(0.1)


def Stop():
    global cronometro_activo
    cronometro_activo = False
    global inicio
    inicio = None


def Start():
    global cronometro_activo
    cronometro_activo = True


def Validar():
    # Obtener el tiempo ingresado en milisegundos y utilizarlo para inicializar el cronómetro
    tiempo_ms = convertir_a_milisegundos(hora_ingresada.get())
    global inicio, tiempo_pausado
    inicio = time.time() - tiempo_ms / 1000
    tiempo_pausado = tiempo_ms / 1000


cronometro_thread = threading.Thread(target=cronometro)
cronometro_thread.daemon = True
cronometro_thread.start()

# ----------------------boton Stop----------------------
botonStop = Button(miFrame, text='Stop', width=3, command=Stop)
botonStop.grid(row=6, column=2)

# ----------------------boton Start------------------
botonStart = Button(miFrame, text='Start', width=3, command=Start)
botonStart.grid(row=6, column=4)

# ----------------------boton Validar------------------
botonValidar = Button(miFrame, text='Validar', width=6, command=Validar)
botonValidar.grid(row=3, column=2, padx=5, pady=7, columnspan=3)


raiz.mainloop()
