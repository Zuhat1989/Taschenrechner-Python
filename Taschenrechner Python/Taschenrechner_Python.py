import tkinter as tk
import math

# ----- THEMES -----
themes = {
    "Modern Hell": {
        "bg": "#f0f0f0", "fg": "#000000",
        "entry_bg": "#ffffff", "entry_fg": "#000000",
        "button_bg": "#e0e0e0", "op_bg": "#ff9500",
        "fn_bg": "#007aff", "equal_bg": "#34c759"
    },
    "Dark Mode": {
        "bg": "#1e1e1e", "fg": "#ffffff",
        "entry_bg": "#2e2e2e", "entry_fg": "#ffffff",
        "button_bg": "#3a3a3a", "op_bg": "#ff9500",
        "fn_bg": "#0a84ff", "equal_bg": "#30d158"
    }
}

current_theme = "Modern Hell"

# ----- HAUPTFENSTER -----
fenster = tk.Tk()
fenster.title("Taschenrechner Deluxe")
fenster.geometry("300x520")
fenster.resizable(False, False)

# ----- EINGABEFELD -----
eingabe = tk.Entry(fenster, font=("Arial", 20), justify="right", bd=0, relief="flat")
eingabe.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(15, 10), ipady=10)

# ----- FUNKTIONEN -----
def taste_einfuegen(wert):
    eingabe.insert(tk.END, wert)

def clear():
    eingabe.delete(0, tk.END)

def rueckschritt():
    eingabe.delete(len(eingabe.get()) - 1)

def berechne():
    try:
        ausdruck = eingabe.get()
        ausdruck = ausdruck.replace("π", str(math.pi))
        ausdruck = ausdruck.replace("^", "**")
        ausdruck = ausdruck.replace("×", "*").replace("÷", "/").replace(",", ".")
        ergebnis = eval(ausdruck)
        eingabe.delete(0, tk.END)
        eingabe.insert(0, str(ergebnis).replace(".", ","))
    except:
        eingabe.delete(0, tk.END)
        eingabe.insert(0, "Fehler")

def theme_wechseln(name):
    global current_theme
    current_theme = name
    theme = themes[name]
    fenster.configure(bg=theme["bg"])
    eingabe.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])

    for btn in buttons:
        typ = buttons[btn]
        if typ == "zahl":
            btn.configure(bg=theme["button_bg"], fg=theme["fg"])
        elif typ == "op":
            btn.configure(bg=theme["op_bg"], fg="#ffffff")
        elif typ == "fn":
            btn.configure(bg=theme["fn_bg"], fg="#ffffff")
        elif typ == "equal":
            btn.configure(bg=theme["equal_bg"], fg="#ffffff")

def taste_von_tastatur(event):
    zeichen = event.char
    if zeichen in "0123456789+-*/().,^%":
        taste_einfuegen(zeichen)
    elif event.keysym == "Return":
        berechne()
    elif event.keysym == "BackSpace":
        rueckschritt()
    elif event.keysym == "Delete":
        clear()
    else:
        return "break"

# Eingabe sperren und Tastaturfunktion aktivieren
eingabe.bind("<Key>", taste_von_tastatur)
fenster.bind("<Key>", taste_von_tastatur)

# ----- MENÜBAND -----
menuleiste = tk.Menu(fenster)
design_menu = tk.Menu(menuleiste, tearoff=0)
for name in themes:
    design_menu.add_command(label=name, command=lambda n=name: theme_wechseln(n))
menuleiste.add_cascade(label="Design wählen", menu=design_menu)
fenster.config(menu=menuleiste)

# ----- BUTTONS DEFINIEREN -----
button_defs = [
    ("(", "fn", 3, 0), (")", "fn", 3, 1), ("xʸ", "fn", 2, 2), ("%", "fn", 2, 3),
    ("log", "fn", 1, 0), ("ln", "fn", 1, 1), ("C", "fn", 3, 2), ("⌫", "fn", 3, 3),
    ("x²", "fn", 2, 0), ("√", "fn", 2, 1), ("1/x", "fn", 1, 2), ("π", "fn", 1, 3),
    ("7", "zahl", 4, 0), ("8", "zahl", 4, 1), ("9", "zahl", 4, 2), ("+", "op", 4, 3),
    ("4", "zahl", 5, 0), ("5", "zahl", 5, 1), ("6", "zahl", 5, 2), ("-", "op", 5, 3),
    ("1", "zahl", 6, 0), ("2", "zahl", 6, 1), ("3", "zahl", 6, 2), ("×", "op", 6, 3),
    (",", "zahl", 7, 0), ("0", "zahl", 7, 1), ("=", "equal", 7, 2), ("÷", "op", 7, 3)
]

buttons = {}

# ----- BUTTONS ERSTELLEN -----
for (text, typ, r, c) in button_defs:
    if text == "":
        continue
    cmd = (
        rueckschritt if text == "⌫" else
        clear if text == "C" else
        berechne if text == "=" else
        lambda t=text: taste_einfuegen("^") if t == "xʸ" else taste_einfuegen(t)
    )
    btn = tk.Button(fenster, text=text, font=("Arial", 14), command=cmd, relief="flat", bd=0)
    btn.grid(row=r, column=c, padx=4, pady=4, ipadx=5, ipady=10, sticky="nsew")
    buttons[btn] = typ

# ----- LAYOUT ANPASSUNG -----
for i in range(8):
    fenster.grid_rowconfigure(i, weight=1)
for j in range(4):
    fenster.grid_columnconfigure(j, weight=1)

# ----- STANDARD DESIGN LADEN -----
theme_wechseln(current_theme)

# ----- START -----
fenster.mainloop()
