import tkinter as tk
import requests
from tkinter import messagebox, scrolledtext

BASE_URL = "https://66eb027855ad32cda47b5321.mockapi.io/IoTCarStatus"

def create_item():
    name = entry_name.get()
    data = {
        "status": "status 1",  # Valor fijo
        "date": 1726677702,    # Valor fijo
        "ipClient": "46.0.186.219",  # Valor fijo
        "name": name,
        "id": None  # El ID se generará automáticamente en MockAPI
    }

    response = requests.post(BASE_URL, json=data)
    if response.status_code == 201:
        messagebox.showinfo("Éxito", "Elemento creado con éxito")
        load_last_records()  # Actualizar la visualización después de crear un elemento
    else:
        messagebox.showerror("Error", "No se pudo crear el elemento")

def load_last_records():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        records = response.json()
        # Ordenar registros por ID de mayor a menor
        records.sort(key=lambda x: int(x['id']), reverse=True)
        last_records = records[:10]  # Obtener los últimos 10 registros
        display_records(last_records)
    else:
        messagebox.showerror("Error", "No se pudieron cargar los registros")

def display_records(records):
    text_area.delete(1.0, tk.END)  # Limpiar el área de texto
    for record in records:
        text_area.insert(tk.END, f"ID: {record['id']}\n"
                                  f"Name: {record['name']}\n"
                                  f"Status: {record['status']}\n"
                                  f"IP: {record['ipClient']}\n"
                                  f"Date: {record['date']}\n\n")  # Formato deseado

# Crear la ventana
ventana = tk.Tk()
ventana.title("Crear y Visualizar Elementos")

# Campo de entrada para el nombre
tk.Label(ventana, text="Name:").pack()
entry_name = tk.Entry(ventana)
entry_name.pack()

# Botón para enviar los datos
boton_crear = tk.Button(ventana, text="Crear", command=create_item)
boton_crear.pack()

# Botón para cargar los últimos registros
boton_cargar = tk.Button(ventana, text="Cargar Últimos 10 Registros", command=load_last_records)
boton_cargar.pack()

# Área de texto para mostrar los registros
text_area = scrolledtext.ScrolledText(ventana, width=50, height=15)
text_area.pack()

ventana.mainloop()
