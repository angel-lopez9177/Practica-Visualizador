import tkinter as tk
from tkinter import ttk
import random
import time

# Parámetros generales
ANCHO = 1200
ALTO = 800
N_BARRAS = 25
VAL_MIN, VAL_MAX = 5, 100
RETARDO_MS = 100 

# Lista que almacena los tiempos de ejecución
tiempos_algoritmos = {}

# Algoritmo: Selection Sort
def selection_sort_steps(data, draw_callback):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_callback(activos=[i, j, min_idx]); yield
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_callback(activos=[i, min_idx]); yield
    draw_callback(activos=[])

# Algoritmo: Bubble sort
def bubble_sort_steps(data, draw_callback):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            draw_callback(activos=[j, j+1]); yield
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                draw_callback(activos=[j, j+1]); yield
    draw_callback(activos=[])

# Algoritmo: Quick sort 
def quick_sort_steps(data, draw_callback):
    stack = [(0, len(data) - 1)]
    
    while stack:
        low, high = stack.pop()
        
        if low < high:
            # Particionar
            pivot_index = yield from particionar_steps(data, low, high, draw_callback)
            
            # Agregar subarrays al stack
            stack.append((pivot_index + 1, high))
            stack.append((low, pivot_index - 1))
    
    draw_callback(activos=[], pivote=None, rango=None)

def particionar_steps(data, low, high, draw_callback):
    pivot = data[high]
    i = low - 1
    
    draw_callback(activos=[], pivote=high, rango=[low, high]); yield
    
    for j in range(low, high):
        draw_callback(activos=[j, high], pivote=high, rango=[low, high]); yield
        
        if data[j] <= pivot:
            i += 1
            if i != j:
                data[i], data[j] = data[j], data[i]
                draw_callback(activos=[i, j], pivote=high, rango=[low, high]); yield
    
    data[i + 1], data[high] = data[high], data[i + 1]
    draw_callback(activos=[i+1, high], pivote=i+1, rango=[low, high]); yield
    
    return i + 1

# Algoritmo: Merge sort 
def merge_sort_steps(data, draw_callback):
    n = len(data)
    current_size = 1
    
    while current_size < n:
        left = 0
        while left < n - 1:
            mid = min(left + current_size - 1, n - 1)
            right = min(left + 2 * current_size - 1, n - 1)
            
            draw_callback(activos=[], fusionando=[left, right]); yield
            yield from merge_steps(data, left, mid, right, draw_callback)
            
            left += 2 * current_size
        
        current_size *= 2
    
    draw_callback(activos=[], fusionando=None)

def merge_steps(data, left, mid, right, draw_callback):
    left_arr = data[left:mid + 1]
    right_arr = data[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    draw_callback(activos=[], fusionando=[left, right]); yield
    
    while i < len(left_arr) and j < len(right_arr):
        draw_callback(activos=[left + i, mid + 1 + j], fusionando=[left, right]); yield
        
        if left_arr[i] <= right_arr[j]:
            data[k] = left_arr[i]
            draw_callback(activos=[k], fusionando=[left, right]); yield
            i += 1
        else:
            data[k] = right_arr[j]
            draw_callback(activos=[k], fusionando=[left, right]); yield
            j += 1
        k += 1
    
    while i < len(left_arr):
        data[k] = left_arr[i]
        draw_callback(activos=[k], fusionando=[left, right]); yield
        i += 1
        k += 1
    
    while j < len(right_arr):
        data[k] = right_arr[j]
        draw_callback(activos=[k], fusionando=[left, right]); yield
        j += 1
        k += 1

# Función de dibujo 

def dibujar_barras(canvas, datos, activos=None, pivote=None, rango=None, fusionando=None):
    canvas.delete("all")
    if not datos: return
    n = len(datos)
    margen = 10
    ancho_disp = ANCHO - 2 * margen
    alto_disp = ALTO - 2 * margen
    w = ancho_disp / n
    esc = alto_disp / max(datos)
    
    for i, v in enumerate(datos):
        x0 = margen + i * w
        x1 = x0 + w * 0.9
        h = v * esc
        y0 = ALTO - margen - h
        y1 = ALTO - margen
        
        color = "#4F34D9"  
        
        # Quick Sort - Pivote
        if pivote is not None and i == pivote:
            color = "#60FAF8"  
        
        # Quick Sort - Rango actual
        if rango and rango[0] <= i <= rango[1]:
            if color == "#4F34D9":
                color = "#7d6ae0"  
        
        # Merge Sort - Rango de fusión
        if fusionando and fusionando[0] <= i <= fusionando[1]:
            color = "#EBA4D2"  # Verde
        
        # Elementos activos (comparando)
        if activos and i in activos:
            color = "#E843CD"  
        
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
    
    canvas.create_text(6, 6, anchor="nw", text=f"n={len(datos)}", fill="#666")

# Función de generación de datos

def generar():
    global datos
    random.seed(time.time())
    datos = [random.randint(VAL_MIN, VAL_MAX) for _ in range(N_BARRAS)]
    dibujar_barras(canvas, datos)

# Función para ordenar los datos dependiendo del algoritmo seleccionado

def ordenar():
    if not datos: return
    algoritmo_seleccionado = combobox.get()
    
    if algoritmo_seleccionado == 'Selection sort':
        gen = selection_sort_steps(datos, lambda activos=None: dibujar_barras(canvas, datos, activos))
    elif algoritmo_seleccionado == 'Bubble sort':
        gen = bubble_sort_steps(datos, lambda activos=None: dibujar_barras(canvas, datos, activos))
    elif algoritmo_seleccionado == 'Quick sort':
        gen = quick_sort_steps(datos, lambda activos=None, pivote=None, rango=None: 
                              dibujar_barras(canvas, datos, activos, pivote, rango))
    elif algoritmo_seleccionado == 'Merge sort':
        gen = merge_sort_steps(datos, lambda activos=None, fusionando=None: 
                              dibujar_barras(canvas, datos, activos, None, None, fusionando))
    else:
        return


    inicio = time.perf_counter()  # Inicia 

    def paso():
        try: 
            next(gen)
            root.after(RETARDO_MS, paso)
        except StopIteration:
            fin = time.perf_counter()
            duracion_ms = (fin - inicio) * 1000
            tiempos_algoritmos[algoritmo_seleccionado] = duracion_ms
            mostrar_tiempos()

    paso()

# Función para establecer el tamaño de n

def set_n_size():
    global N_BARRAS
    try:
        number = int(entry_n.get())
        if number < 0:
            status_label.config(text="Ingresa valores positivos enteros", fg="red")
            return
        if number > 1000:
            status_label.config(text="Máximo 100 elementos", fg="red")
            return
            
        N_BARRAS = number
        status_label.config(text=f"n={number} establecido", fg="#112E49")
        generar()  
    except ValueError:
        status_label.config(text="Ingrese un número válido", fg="red")

#Función para mezclar los datos del array

def shuffle_arr():
    global datos  
    random.shuffle(datos)  
    dibujar_barras(canvas, datos)  

# Función para cambiar el tiempo de retardo en ms

def change_speed(speed):
    global RETARDO_MS
    RETARDO_MS = int(float(speed))

# Función para limpiar 

def clean():
    if datos: 
        dibujar_barras(canvas, datos, activos=[], pivote=None, rango=None, fusionando=None)

# Funbción para medir el tiempo de ejecución

def mostrar_tiempos():
    """Actualizar la lista de tiempos en el frame de tiempos"""
    for widget in times_frame.winfo_children():
        widget.destroy()
    if not tiempos_algoritmos:
        tk.Label(times_frame, text="Sin datos", bg="#f0f0f0").pack(anchor="w")
        return
    for alg, t in tiempos_algoritmos.items():
        tk.Label(times_frame, text=f"{alg}: {t:.2f} ms", bg="#f0f0f0",
                 font=("Arial", 9)).pack(anchor="w")

    

# Aplicación principal
datos = []
root = tk.Tk()
root.title("Visualizador de Algoritmos de Ordenamiento")
root.geometry("1400x800")  

# Frame principal que divide izquierda y derecha
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Frame izquierdo para controles
left_frame = tk.Frame(main_frame, width=250, bg="#f0f0f0")
left_frame.pack(side="left", fill="y", padx=(0, 10))
left_frame.pack_propagate(False)  

# Frame derecho para la gráfica
right_frame = tk.Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True)

# Título en el panel izquierdo
title_label = tk.Label(left_frame, text="Controles", font=("Arial", 12, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Controles de tamaño
size_frame = tk.Frame(left_frame, bg="#f0f0f0")
size_frame.pack(pady=10, padx=10, fill="x")

tk.Label(size_frame, text="Tamaño del array (n):", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w")

entry_frame = tk.Frame(size_frame, bg="#f0f0f0")
entry_frame.pack(fill="x", pady=5)

entry_n = tk.Entry(entry_frame, width=10, justify="center", font=("Arial", 10))
entry_n.insert(0, str(N_BARRAS))
entry_n.pack(side="left", padx=(0, 5))

set_button = tk.Button(entry_frame, text="Establecer", command=set_n_size, 
                      bg="#C252E1", fg="white", font=("Arial", 9))
set_button.pack(side="left")

status_label = tk.Label(size_frame, text=f"n={N_BARRAS}", fg="#112E49", 
                       bg="#f0f0f0", font=("Arial", 9))
status_label.pack(anchor="w", pady=5)

# Separador
separator = ttk.Separator(left_frame, orient="horizontal")
separator.pack(fill="x", pady=10)

# Controles de algoritmo
algoritmo_frame = tk.Frame(left_frame, bg="#f0f0f0")
algoritmo_frame.pack(pady=10, padx=10, fill="x")

tk.Label(algoritmo_frame, text="Algoritmo:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w")

opciones_algoritmo = ['Selection sort', 'Bubble sort', 'Quick sort', 'Merge sort']
combobox = ttk.Combobox(algoritmo_frame, values=opciones_algoritmo, state="readonly", 
                       width=15, font=("Arial", 10))
combobox.pack(pady=5, fill="x")
combobox.set('Selection sort')

# Botones de acción
button_frame = tk.Frame(algoritmo_frame, bg="#f0f0f0")
button_frame.pack(fill="x", pady=10)

generate_button = tk.Button(button_frame, text="Generar Array", command=generar,
                           bg="#0F1546", fg="white", font=("Arial", 10), width=12)
generate_button.pack(pady=5)

sort_button = tk.Button(button_frame, text="Ordenar", command=ordenar,
                       bg="#2843AD", fg="white", font=("Arial", 10), width=12)
sort_button.pack(pady=5)

shuffle_button = tk.Button(button_frame, text = "Mezclar", command=shuffle_arr,
                           bg="#818DE0", fg="white",font=("Arial", 10), width=12) 
shuffle_button.pack(pady=5)

clear_button = tk.Button(button_frame, text="Limpiar", command=clean,
                         bg="#AB95B8", fg="white", font=("Arial", 10), width=12)
clear_button.pack(pady=5)

# Frame de tiempos de ejecución 

separator2 = ttk.Separator(left_frame, orient="horizontal")
separator2.pack(fill="x", pady=10)

times_label = tk.Label(left_frame, text="Tiempos de ejecución (ms):", 
                      font=("Arial", 10, "bold"), bg="#f0f0f0")
times_label.pack(anchor="w", padx=10)

times_frame = tk.Frame(left_frame, bg="#f0f0f0")
times_frame.pack(padx=10, pady=5, fill="x")

mostrar_tiempos()

# Cambio de velocidad

scale_frame = tk.Frame(algoritmo_frame, bg="#f0f0f0")
scale_frame.pack(fill="x", pady=10)

scale_label = tk.Label(scale_frame, text="Velocidad: ", bg="#f0f0f0", font=("Arial", 10))
scale_label.pack(anchor="w")

scale_value = tk.Scale(scale_frame, from_=0, to=200, orient=tk.HORIZONTAL, command=change_speed)
scale_value.pack(pady=5)
scale_value.set(RETARDO_MS)
scale_value.pack(pady=10, fill="x")


# Canvas para visualización 
canvas = tk.Canvas(right_frame, width=ANCHO, height=ALTO, bg="white", relief="sunken", bd=2)
canvas.pack(fill="both", expand=True, padx=10, pady=10)

generar()
root.mainloop()