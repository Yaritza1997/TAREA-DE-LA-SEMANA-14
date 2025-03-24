import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
from tkcalendar import Calendar

# Crear la clase de la aplicación
class AgendaApp:
    def __init__(self, root):
        # Titulo de la ventana principal
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("600x400")

        # Lista para almacenar los eventos
        self.eventos = []

        # Crear un Frame para la lista de eventos
        self.frame_lista = tk.Frame(self.root)
        self.frame_lista.pack(pady=10)

        # Crear un TreeView para mostrar los eventos
        self.treeview = ttk.Treeview(self.frame_lista, columns=("Fecha", "Hora", "Descripción"), show="headings")
        self.treeview.heading("Fecha", text="Fecha")
        self.treeview.heading("Hora", text="Hora")
        self.treeview.heading("Descripción", text="Descripción")
        self.treeview.pack()

        # Crear un Frame para los campos de entrada y botones
        self.frame_entrada = tk.Frame(self.root)
        self.frame_entrada.pack(pady=10)

        # Etiqueta y campo para la fecha
        self.label_fecha = tk.Label(self.frame_entrada, text="Fecha:")
        self.label_fecha.grid(row=0, column=0, padx=5, pady=5)
        self.calendario = Calendar(self.frame_entrada, date_pattern="yyyy-mm-dd")
        self.calendario.grid(row=0, column=1, padx=5, pady=5)

        # Etiqueta y campo para la hora
        self.label_hora = tk.Label(self.frame_entrada, text="Hora (HH:MM):")
        self.label_hora.grid(row=1, column=0, padx=5, pady=5)
        self.entry_hora = tk.Entry(self.frame_entrada)
        self.entry_hora.grid(row=1, column=1, padx=5, pady=5)

        # Etiqueta y campo para la descripción
        self.label_descripcion = tk.Label(self.frame_entrada, text="Descripción:")
        self.label_descripcion.grid(row=2, column=0, padx=5, pady=5)
        self.entry_descripcion = tk.Entry(self.frame_entrada)
        self.entry_descripcion.grid(row=2, column=1, padx=5, pady=5)

        # Botón para agregar evento
        self.boton_agregar = tk.Button(self.frame_entrada, text="Agregar Evento", command=self.agregar_evento)
        self.boton_agregar.grid(row=3, column=0, columnspan=2, pady=10)

        # Botón para eliminar evento seleccionado
        self.boton_eliminar = tk.Button(self.frame_entrada, text="Eliminar Evento Seleccionado", command=self.eliminar_evento)
        self.boton_eliminar.grid(row=4, column=0, columnspan=2, pady=10)

        # Botón para salir de la aplicación
        self.boton_salir = tk.Button(self.frame_entrada, text="Salir", command=self.salir)
        self.boton_salir.grid(row=5, column=0, columnspan=2, pady=10)

    def agregar_evento(self):
        """
        Agregar un evento a la lista de eventos y actualizar la visualización.
        """
        fecha = self.calendario.get_date()
        hora = self.entry_hora.get()
        descripcion = self.entry_descripcion.get()

        # Verificar que los campos no estén vacíos
        if not fecha or not hora or not descripcion:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        # Verificar formato de la hora (HH:MM)
        try:
            datetime.datetime.strptime(hora, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "El formato de hora debe ser HH:MM.")
            return

        # Agregar el evento a la lista
        self.eventos.append({"Fecha": fecha, "Hora": hora, "Descripción": descripcion})

        # Limpiar campos de entrada
        self.entry_hora.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)

        # Actualizar el TreeView
        self.actualizar_lista_eventos()

    def eliminar_evento(self):
        """
        Eliminar el evento seleccionado en el TreeView.
        """
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un evento para eliminar.")
            return

        # Confirmar la eliminación
        confirmar = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este evento?")
        if confirmar:
            for item in selected_item:
                # Eliminar el evento de la lista
                self.treeview.delete(item)

            # Eliminar el evento de la lista interna
            self.eventos = [evento for evento in self.eventos if not any(evento["Fecha"] == self.treeview.item(item)["values"][0] and evento["Hora"] == self.treeview.item(item)["values"][1] for item in selected_item)]

    def actualizar_lista_eventos(self):
        """
        Actualizar el TreeView con los eventos actuales.
        """
        # Limpiar el TreeView antes de actualizarlo
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Insertar los eventos actuales en el TreeView
        for evento in self.eventos:
            self.treeview.insert("", "end", values=(evento["Fecha"], evento["Hora"], evento["Descripción"]))

    def salir(self):
        """
        Salir de la aplicación.
        """
        self.root.quit()

# Crear la ventana principal y ejecutar la aplicación
root = tk.Tk()
app = AgendaApp(root)
root.mainloop()

