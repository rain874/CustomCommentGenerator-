__author__ = "Rainer Schmitz <rainer.ch.franz@gmail.com>"
__copyright__ = "Rainer Schmitz <rainer.ch.franz@gmail.com>"
__version__ = "2.1.0"

import os.path
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import configparser
import pyperclip
import subprocess

# ToDo: Laden der Var aus dem Config file
config_paht = "C:/Users/BENUTZER/Projekt/configs/commentgen_config.ini"
todo_markdown_paht = "C:/Users/BENUTZER/Projekt/configs/markdown_doc/ToDo.md"
bugdoc_markdown_paht = "C:/Users/BENUTZER/Projekt/configs/markdown_doc/BugDoc.md"
doccom_markdown_paht = "C:/Users/BENUTZER/Projekt/configs/markdown_doc/DocCOM.md"

# Custom Comment Generator 
def load_and_save_config(config_file="ccg_settings.ini"):
    # Erstelle ein ConfigParser-Objekt
    config = configparser.ConfigParser()

    # Versuche, die Konfigurationsdatei zu laden
    if os.path.exists(config_file):
        config.read(config_file)
        config_path = config.get("Settings", "config_path", fallback="")
    else:
        config_path = ""

    # Wenn der Pfad noch nicht gespeichert wurde, frage den Benutzer nach der Datei
    if config_path == "":
        messagebox.showwarning("Keine Konfigurationsdatei der ccg_settings.ini", "Es wurde keine Datei ausgewählt.")
        config_path = filedialog.askopenfilename(
            title="Wählen Sie die Konfigurationsdatei aus (.ini)",
            filetypes=[("INI Dateien", "*.ini"), ("Alle Dateien", "*.*")])

        if config_path == "":
            messagebox.showwarning("Kein Pfad gewählt", "Es wurde keine Datei ausgewählt. Programm wird beendet.")
            sys.exit()

        # Wenn eine gültige .ini-Datei ausgewählt wurde, speichere den Pfad
        if not config_path.lower().endswith(".ini"):
            messagebox.showwarning("Ungültige Datei", "Bitte wählen Sie eine .ini-Datei.")
            sys.exit()

        # Speichere den Pfad in der Konfigurationsdatei
        if not config.has_section("Settings"):
            config.add_section("Settings")
        config.set("Settings", "config_path", config_path)

        with open(config_file, "w") as configfile:
            config.write(configfile)
    else:
        # Wenn der Pfad bereits gespeichert wurde
        print(f"Verwendete Konfigurationsdatei: {config_path}")

    return config_path


# Funktion zum Generieren von Dokumenten
def generate_docToDO():
    config = configparser.ConfigParser()
    config.read(config_paht)
    projektid = config.get('PerSet', 'projektid')
    developerid = config.get('PerSet', 'developerid')
    counter = config.getint('ToDOs', 'counter')
    counter += 1
    doctype = config.get('ToDOs', 'doctype')

    config.set('ToDOs', 'counter', str(counter))

    with open(config_paht, 'w') as configfile:
        config.write(configfile)
    timestamp = datetime.datetime.now().strftime('%Y%m%d-') + str(counter).zfill(5)
    respond = doctype + " " + projektid + "-" + timestamp + "-" + developerid

    return respond


def generate_docBugDoc():
    config = configparser.ConfigParser()
    config.read(config_paht)
    projektid = config.get('PerSet', 'projektid')
    developerid = config.get('PerSet', 'developerid')
    counter = config.getint('BugDoc', 'counter')
    counter += 1
    doctype = config.get('BugDoc', 'doctype')

    config.set('BugDoc', 'counter', str(counter))

    with open(config_paht, 'w') as configfile:
        config.write(configfile)
    timestamp = datetime.datetime.now().strftime('%Y%m%d-') + str(counter).zfill(5)
    respond = doctype + " " + projektid + "-" + timestamp + "-" + developerid

    return respond


def generate_docCOM():
    config = configparser.ConfigParser()
    config.read(config_paht)
    projektid = config.get('PerSet', 'projektid')
    developerid = config.get('PerSet', 'developerid')
    counter = config.getint('DocCOM', 'counter')
    counter += 1
    doctype = config.get('DocCOM', 'doctype')

    config.set('DocCOM', 'counter', str(counter))

    with open(config_paht, 'w') as configfile:
        config.write(configfile)
    timestamp = datetime.datetime.now().strftime('%Y%m%d-') + str(counter).zfill(5)
    respond = doctype + " " + projektid + "-" + timestamp + "-" + developerid

    return respond


def open_markdown_file():
    global todo_markdown_paht, bugdoc_markdown_paht, doccom_markdown_paht

    # Bestimmen Sie, welche Datei verwendet wird
    if comment_type.get() == "TD" and todo_markdown_paht:
        file_path = todo_markdown_paht
    elif comment_type.get() == "BD" and bugdoc_markdown_paht:
        file_path = bugdoc_markdown_paht
    elif comment_type.get() == "DC" and doccom_markdown_paht:
        file_path = doccom_markdown_paht
    else:
        messagebox.showwarning("Fehler", "Keine passende Markdown-Datei gefunden.")
        return

    try:
        pycharm_path = r'C:/Program Files/JetBrains/PyCharm Community Edition 2022.3.2/bin/pycharm64.exe'
        print(file_path)
        command = [pycharm_path, file_path]
        print(command)
        subprocess.Popen(command)
        # ToDo: 116-20250124-00108-0007
    except Exception as e:
        messagebox.showerror("Fehler", f"Es gab ein Problem beim Öffnen der Datei: {e}")


def copy_to_clipboard(text):
    pyperclip.copy(text)
    messagebox.showinfo("Erfolg", f"Kommentar '{text}' wurde in die Zwischenablage kopiert und in der Markdown-Datei eingefügt.")


def save_comment_to_file(comment):
    global todo_markdown_paht, bugdoc_markdown_paht, doccom_markdown_paht

    if comment_type.get() == "TD" and todo_markdown_paht:
        file_path = todo_markdown_paht
    elif comment_type.get() == "BD" and bugdoc_markdown_paht:
        file_path = bugdoc_markdown_paht
    elif comment_type.get() == "DC" and doccom_markdown_paht:
        file_path = doccom_markdown_paht
    else:
        messagebox.showwarning("Fehler", "Bitte wählen Sie zuerst eine Markdown-Datei für diesen Kommentar-Typ aus.")
        return

    try:
        with open(file_path, "a") as file:
            file.write(f"{comment}\n")
    except Exception as e:
        messagebox.showerror("Fehler", f"Es gab ein Problem beim Speichern: {e}")


def on_generate_comment():
    flag = comment_type.get()

    if flag == "TD":
        doctype = generate_docToDO()
        save_comment_to_file(doctype)
        copy_to_clipboard(doctype)
        open_markdown_file()

    elif flag == "BD":
        doctype = generate_docBugDoc()
        save_comment_to_file(doctype)
        copy_to_clipboard(doctype)
        open_markdown_file()

    elif flag == "DC":
        doctype = generate_docCOM()
        save_comment_to_file(doctype)
        copy_to_clipboard(doctype)
        open_markdown_file()

    else:
        messagebox.showwarning("Ungültige Eingabe", "Bitte einen gültigen Kommentar-Typ auswählen.")

    # ToDo: 116-20250124-00117-0007


def on_set_config_file():
    global config_paht
    config_paht = filedialog.askopenfilename(
        title="Wählen Sie die Konfigurationsdatei aus",
        filetypes=[("INI Dateien", "*.ini"), ("Alle Dateien", "*.*")]
    )
    if config_paht:  # Wenn der Benutzer eine Datei auswählt
        config_entry.delete(0, tk.END)
        config_entry.insert(0, config_paht)
        messagebox.showinfo("Konfigurationsdatei gesetzt", f"Das Konfigurationsdateipfad wurde auf {config_paht} gesetzt.")
    else:
        messagebox.showwarning("Kein Pfad gewählt", "Es wurde keine Datei ausgewählt.")


def on_set_markdown_file(comment_type):
    global todo_markdown_paht, bugdoc_markdown_paht, doccom_markdown_paht

    file_path = filedialog.asksaveasfilename(
        title=f"Wählen Sie die {comment_type} Markdown-Datei aus",
        defaultextension=".md",
        filetypes=[("Markdown Dateien", "*.md"), ("Alle Dateien", "*.*")]
    )

    if file_path:  # Wenn der Benutzer eine Datei auswählt
        if comment_type == "TD":
            todo_markdown_paht = file_path
        elif comment_type == "BD":
            bugdoc_markdown_paht = file_path
        elif comment_type == "DC":
            doccom_markdown_paht = file_path
        messagebox.showinfo("Markdown-Datei gesetzt", f"Die {comment_type} Markdown-Datei wurde auf {file_path} gesetzt.")
    else:
        messagebox.showwarning("Kein Pfad gewählt", "Es wurde keine Datei ausgewählt.")


def on_show_help():
    help_message = (
        "Usage: Setze den Zähler und die IDs in der config.ini\n"
        "TD = ToDo-Kommentar\n"
        "BD = BugDoc-Kommentar\n"
        "DC = DocCOM-Kommentar\n"
    )
    messagebox.showinfo("Hilfe", help_message)


def load_comments(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except Exception as e:
        messagebox.showerror("Fehler", f"Es gab ein Problem beim Laden der Datei: {e}")
        return []


def update_comments_list(file_path, listbox):
    comments = load_comments(file_path)
    listbox.delete(0, tk.END)
    for comment in comments:
        listbox.insert(tk.END, comment.strip())


def delete_selected_comments(listbox):
    global todo_markdown_paht, bugdoc_markdown_paht, doccom_markdown_paht, config_paht

    # Bestimmen Sie, welche Datei verwendet wird und den entsprechenden Zähler
    if comment_type.get() == "TD" and todo_markdown_paht:
        file_path = todo_markdown_paht
        section = "ToDOs"
        header = "# ToDo:"
    elif comment_type.get() == "BD" and bugdoc_markdown_paht:
        file_path = bugdoc_markdown_paht
        section = "BugDoc"
        header = "# BugDoc:"
    elif comment_type.get() == "DC" and doccom_markdown_paht:
        file_path = doccom_markdown_paht
        section = "DocCOM"
        header = "# DocCOM:"
    else:
        messagebox.showwarning("Fehler", "Keine passende Markdown-Datei zum Löschen gefunden.")
        return

    # Lade die Datei und finde die Kommentare
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Finden der Indizes der Kommentare, die gelöscht werden sollen
        selected_indices = [index for index in listbox.curselection()]
        delete_start_index = selected_indices[0]  # Der erste ausgewählte Kommentar bestimmt den Startpunkt
        delete_end_index = None

        # Finde den nächsten Kommentar, der nach dem Startpunkt kommt
        for i in range(delete_start_index + 1, len(lines)):
            if lines[i].startswith(header):
                delete_end_index = i
                break

        # Wenn kein nächster Kommentar gefunden wurde, lösche bis zum Ende der Datei
        if delete_end_index is None:
            delete_end_index = len(lines)

        # Lösche die Zeilen zwischen dem Start- und Endpunkt
        comments_to_delete = []
        for i in range(delete_start_index, delete_end_index):
            if lines[i].startswith(header):
                comments_to_delete.append(lines[i])  # Nur die Header zählen als Kommentar

        remaining_lines = lines[:delete_start_index] + lines[delete_end_index:]

        # Schreibe die verbleibenden Zeilen zurück in die Datei
        with open(file_path, "w") as file:
            file.writelines(remaining_lines)

        # Zähler für den entsprechenden Kommentar-Typ aktualisieren
        config = configparser.ConfigParser()
        config.read(config_paht)
        counter = config.getint(section, 'counter')

        # Reduziere den Zähler um die Anzahl der **gelöschten Kommentare** (nicht Zeilen)
        counter -= len(comments_to_delete)

        # Setze den neuen Zähler in der config.ini
        config.set(section, 'counter', str(counter))

        with open(config_paht, 'w') as configfile:
            config.write(configfile)

        messagebox.showinfo("Erfolg",
                            f"{len(comments_to_delete)} Kommentar(e) wurden gelöscht und der Zähler angepasst!")

        # Aktualisiere die Anzeige der Kommentare in der Listbox
        update_comments_list(file_path, listbox)

    except Exception as e:
        messagebox.showerror("Fehler", f"Es gab ein Problem beim Löschen der Kommentare: {e}")





def show_comments_window():
    # Bestimmen Sie, welche Datei verwendet wird
    if comment_type.get() == "TD" and todo_markdown_paht:
        file_path = todo_markdown_paht
    elif comment_type.get() == "BD" and bugdoc_markdown_paht:
        file_path = bugdoc_markdown_paht
    elif comment_type.get() == "DC" and doccom_markdown_paht:
        file_path = doccom_markdown_paht
    else:
        messagebox.showwarning("Fehler", "Keine passende Markdown-Datei gefunden.")
        return

    comments = load_comments(file_path)

    comments_window = tk.Toplevel(root)
    comments_window.title(f"Kommentare - {file_path}")

    listbox = tk.Listbox(comments_window, selectmode=tk.MULTIPLE, height=30, width=150)
    listbox.pack(padx=100, pady=100)

    for comment in comments:
        listbox.insert(tk.END, comment.strip())

    delete_button = tk.Button(comments_window, text="Kommentare löschen", command=lambda: delete_selected_comments(listbox))
    delete_button.pack(padx=100, pady=100)

    comments_window.mainloop()


# Beispielaufruf der Funktion
config_path = load_and_save_config()

# GUI Setup
root = tk.Tk()
root.title(f"Comment Generator - {config_path}")

# Setze die Fenstergröße
root.geometry("1080x250")

# Verhindere, dass das Fenster in der Größe verändert wird
root.resizable(False, False)


# Menüleiste erstellen
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menü "Datei"
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Datei", menu=file_menu)
file_menu.add_command(label="Konfigurationsdatei wählen", command=on_set_config_file)
file_menu.add_command(label="ToDo Markdown-Datei wählen", command=lambda: on_set_markdown_file("TD"))
file_menu.add_command(label="BugDoc Markdown-Datei wählen", command=lambda: on_set_markdown_file("BD"))
file_menu.add_command(label="DocCOM Markdown-Datei wählen", command=lambda: on_set_markdown_file("DC"))
file_menu.add_separator()
file_menu.add_command(label="Beenden", command=root.quit)

# Menü "Kommentare"
comments_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Kommentare", menu=comments_menu)
comments_menu.add_command(label="Markdown-Datei öffnen", command=open_markdown_file)  # Hinzugefügter Menüpunkt
comments_menu.add_command(label="Kommentare anzeigen", command=show_comments_window)  # Fehler behoben

# Hilfe-Menüpunkt direkt als eigenes Menü
menu_bar.add_command(label="Hilfe", command=on_show_help)

# Setze GUI-Elemente
comment_type_label = tk.Label(root, text="Wählen Sie den Kommentar-Typ:")
comment_type_label.pack(pady=5, padx=10, anchor="w")

comment_type = tk.StringVar()
comment_type.set("TD")  # Standardmäßig "TD"
dropdown = tk.OptionMenu(root, comment_type, "TD", "BD", "DC")
dropdown.pack(pady=5, padx=10, anchor="w")

generate_button = tk.Button(root, text="Kommentar Generieren und Speichern", command=on_generate_comment)
generate_button.pack(pady=5, padx=10, anchor="w")

root.mainloop()

