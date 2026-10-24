import tkinter as tk
from tkinter import ttk

CAPACIDAD = 8

# (letra, operación, nombre del elemento / variable destino)
OPERACIONES = [
    ("a", "insertar", "X"),
    ("b", "insertar", "Y"),
    ("c", "eliminar", "Z"),
    ("d", "eliminar", "T"),
    ("e", "eliminar", "U"),
    ("f", "insertar", "V"),
    ("g", "insertar", "W"),
    ("h", "eliminar", "p"),
    ("i", "insertar", "R"),
]

# Colores
BG = "#1e2233"
PANEL = "#272d45"
CELDA_VACIA = "#323a5a"
CELDA_LLENA = "#4a90e2"
VERDE = "#2ecc71"
ROJO = "#e74c3c"
AMARILLO = "#f1c40f"
TEXTO = "#ecf0f1"


def calcular_estados():
    """Ejecuta todas las operaciones y guarda una 'foto' de cada estado."""
    pila = [None] * CAPACIDAD
    tope = 0
    estados = [{
        "titulo": "Estado inicial",
        "pila": pila.copy(), "tope": tope,
        "tipo": "inicio", "cambio": None,
        "mensaje": "Pila vacía (TOPE = 0). Capacidad máxima: 8 elementos.",
    }]

    for letra, op, nombre in OPERACIONES:
        if op == "insertar":
            if tope == CAPACIDAD:
                tipo, cambio = "error", None
                msg = "DESBORDAMIENTO: la pila está llena."
            else:
                pila[tope] = nombre
                tope += 1
                tipo, cambio = "insertar", tope
                msg = f"Se inserta {nombre} en la posición {tope}. TOPE sube a {tope}."
            titulo = f"{letra}) Insertar (PILA, {nombre})"
        else:
            if tope == 0:
                tipo, cambio = "error", None
                msg = (f"SUBDESBORDAMIENTO: la pila está vacía, no hay nada que "
                       f"eliminar. {nombre} queda sin valor.")
            else:
                valor = pila[tope - 1]
                pila[tope - 1] = None
                cambio = tope
                tope -= 1
                tipo = "eliminar"
                msg = f"Se elimina {valor} y se guarda en {nombre} ({nombre} = {valor}). TOPE baja a {tope}."
            titulo = f"{letra}) Eliminar (PILA, {nombre})"

        estados.append({
            "titulo": titulo, "pila": pila.copy(), "tope": tope,
            "tipo": tipo, "cambio": cambio, "mensaje": msg,
        })
    return estados


class App:
    def __init__(self, root):
        self.root = root
        self.estados = calcular_estados()
        self.i = 0
        self.auto = False

        root.title("Simulador de PILA")
        root.configure(bg=BG)
        root.resizable(False, False)

        # ----- Título -----
        tk.Label(root, text="SIMULADOR DE PILA", font=("Segoe UI", 20, "bold"),
                 bg=BG, fg=AMARILLO).grid(row=0, column=0, columnspan=2, pady=(12, 0))
        self.lbl_titulo = tk.Label(root, text="", font=("Segoe UI", 13, "bold"),
                                   bg=BG, fg=TEXTO)
        self.lbl_titulo.grid(row=1, column=0, columnspan=2, pady=(2, 6))

        # ----- Canvas de la pila -----
        self.canvas = tk.Canvas(root, width=360, height=520, bg=PANEL,
                                highlightthickness=0)
        self.canvas.grid(row=2, column=0, padx=(14, 7), pady=4)

        # ----- Panel derecho: lista de operaciones -----
        der = tk.Frame(root, bg=BG)
        der.grid(row=2, column=1, padx=(7, 14), pady=4, sticky="n")

        tk.Label(der, text="Operaciones", font=("Segoe UI", 12, "bold"),
                 bg=BG, fg=TEXTO).pack(anchor="w")

        self.lista = tk.Listbox(der, width=30, height=10, font=("Consolas", 11),
                                bg=PANEL, fg=TEXTO, selectbackground=AMARILLO,
                                selectforeground="black", activestyle="none",
                                highlightthickness=0, bd=0)
        self.lista.pack(pady=(2, 10))
        self.lista.insert(tk.END, "  Estado inicial")
        for letra, op, nombre in OPERACIONES:
            etiqueta = "Insertar" if op == "insertar" else "Eliminar"
            self.lista.insert(tk.END, f"  {letra}) {etiqueta} (PILA, {nombre})")
        self.lista.bind("<<ListboxSelect>>", self.al_seleccionar)

        tk.Label(der, text="Qué pasó", font=("Segoe UI", 12, "bold"),
                 bg=BG, fg=TEXTO).pack(anchor="w")
        self.lbl_msg = tk.Label(der, text="", wraplength=250, justify="left",
                                font=("Segoe UI", 11), bg=PANEL, fg=TEXTO,
                                width=30, height=6, anchor="nw", padx=8, pady=8)
        self.lbl_msg.pack(pady=(2, 8))

        self.lbl_tope = tk.Label(der, text="", font=("Consolas", 18, "bold"),
                                 bg=BG, fg=AMARILLO)
        self.lbl_tope.pack()

        # ----- Botones -----
        barra = tk.Frame(root, bg=BG)
        barra.grid(row=3, column=0, columnspan=2, pady=(6, 14))

        estilo = dict(font=("Segoe UI", 11, "bold"), width=13, bd=0,
                      fg="white", cursor="hand2", pady=6)
        tk.Button(barra, text="⏮ Reiniciar", bg="#7f8c8d",
                  command=self.reiniciar, **estilo).pack(side="left", padx=4)
        tk.Button(barra, text="◀ Anterior", bg="#8e44ad",
                  command=self.anterior, **estilo).pack(side="left", padx=4)
        tk.Button(barra, text="Siguiente ▶", bg="#27ae60",
                  command=self.siguiente, **estilo).pack(side="left", padx=4)
        self.btn_auto = tk.Button(barra, text="▶▶ Automático", bg="#e67e22",
                                  command=self.alternar_auto, **estilo)
        self.btn_auto.pack(side="left", padx=4)

        root.bind("<Right>", lambda e: self.siguiente())
        root.bind("<Left>", lambda e: self.anterior())

        self.dibujar()

    # ---------- Navegación ----------
    def siguiente(self):
        if self.i < len(self.estados) - 1:
            self.i += 1
            self.dibujar()
        else:
            self.detener_auto()

    def anterior(self):
        if self.i > 0:
            self.i -= 1
            self.dibujar()

    def reiniciar(self):
        self.detener_auto()
        self.i = 0
        self.dibujar()

    def al_seleccionar(self, _):
        sel = self.lista.curselection()
        if sel:
            self.detener_auto()
            self.i = sel[0]
            self.dibujar()

    def alternar_auto(self):
        if self.auto:
            self.detener_auto()
        else:
            if self.i >= len(self.estados) - 1:
                self.i = 0
                self.dibujar()
            self.auto = True
            self.btn_auto.config(text="⏸ Pausar")
            self.paso_auto()

    def paso_auto(self):
        if not self.auto:
            return
        if self.i < len(self.estados) - 1:
            self.i += 1
            self.dibujar()
            self.root.after(1300, self.paso_auto)
        else:
            self.detener_auto()

    def detener_auto(self):
        self.auto = False
        self.btn_auto.config(text="▶▶ Automático")

    # ---------- Dibujo ----------
    def dibujar(self):
        e = self.estados[self.i]
        c = self.canvas
        c.delete("all")

        x0, x1 = 150, 330
        alto = 52
        base = 480  # y del fondo de la pila

        # Posiciones 1..8 (1 abajo)
        for pos in range(1, CAPACIDAD + 1):
            y1 = base - (pos - 1) * alto
            y0 = y1 - alto + 4
            valor = e["pila"][pos - 1]

            if valor is None:
                color, borde = CELDA_VACIA, "#4a5378"
            else:
                color, borde = CELDA_LLENA, "white"

            # Resaltar la casilla que acaba de cambiar
            if e["cambio"] == pos:
                if e["tipo"] == "insertar":
                    color = VERDE
                elif e["tipo"] == "eliminar":
                    color, borde = "#4a3037", ROJO

            c.create_rectangle(x0, y0, x1, y1, fill=color, outline=borde, width=2)
            c.create_text(x0 - 30, (y0 + y1) / 2, text=str(pos),
                          fill="#8c95b8", font=("Consolas", 13, "bold"))
            if valor is not None:
                c.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=valor,
                              fill="white", font=("Segoe UI", 22, "bold"))

        # Base de la pila
        c.create_line(x0 - 10, base + 2, x1 + 10, base + 2, fill="white", width=4)

        # Flecha de TOPE
        if e["tope"] == 0:
            ya = base + 22
            c.create_text(x0 - 10, ya, text="TOPE = 0 (vacía)", anchor="e",
                          fill=AMARILLO, font=("Segoe UI", 11, "bold"))
        else:
            ya = base - (e["tope"] - 1) * alto - alto / 2 + 2
            c.create_line(30, ya, x0 - 40, ya, fill=AMARILLO, width=4,
                          arrow=tk.LAST, arrowshape=(14, 16, 6))
            c.create_text(8, ya - 16, text="TOPE", anchor="w",
                          fill=AMARILLO, font=("Segoe UI", 12, "bold"))

        # Aviso de error sobre el dibujo
        if e["tipo"] == "error":
            c.create_rectangle(x0 - 10, 8, x1 + 10, 40, fill=ROJO, outline="")
            c.create_text((x0 + x1) / 2, 24, text="¡ERROR!", fill="white",
                          font=("Segoe UI", 14, "bold"))

        # Textos del panel
        colores = {"error": ROJO, "insertar": VERDE, "eliminar": "#ff8a80",
                   "inicio": TEXTO}
        self.lbl_titulo.config(text=e["titulo"], fg=colores[e["tipo"]])
        self.lbl_msg.config(text=e["mensaje"])
        self.lbl_tope.config(text=f"TOPE = {e['tope']}")

        self.lista.selection_clear(0, tk.END)
        self.lista.selection_set(self.i)
        self.lista.see(self.i)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()