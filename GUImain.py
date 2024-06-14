import pyperclip
import random
import time
import pyautogui
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class AutoMessageSender:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Message Sender")

        # Styles definieren
        style = ttk.Style(root)
        root.configure(background='#1f1f2e')  # Dunkles Blau-Schwarz für das Hauptfenster-Hintergrund
        style.configure('TFrame', background='#282a36')  # Dunkles Lila für Frame-Hintergrund
        style.configure('TLabel', background='#282a36', foreground='#f8f8f2', font=('Arial', 10))  # Label-Stil
        style.configure('TButton', background='#bd93f9', foreground='#44475a', font=('Arial', 10, 'bold'))  # Button-Stil
        style.map('TButton', background=[('active', '#ff79c6')])  # Aktive Hintergrundfarbe für Button
        style.configure('TEntry', fieldbackground='#44475a', foreground='#bd93f9', font=('Arial', 10))  # Entry-Stil

        # Frame für Widgets
        self.frame = ttk.Frame(root, padding="10 10 10 10")
        self.frame.pack(padx=10, pady=10)

        # Labels und Eingabefelder für Zeitintervalle
        ttk.Label(self.frame, text="Minimale Zeit (Sekunden):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_min = ttk.Entry(self.frame)
        self.entry_min.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Maximale Zeit (Sekunden):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_max = ttk.Entry(self.frame)
        self.entry_max.grid(row=1, column=1, padx=5, pady=5)

        # Starten und Stoppen Buttons
        ttk.Button(self.frame, text="Starten", command=self.start_script).grid(row=2, columnspan=2, pady=10, sticky='we')
        self.stop_button = ttk.Button(self.frame, text="Stoppen", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.grid(row=3, columnspan=2, pady=10, sticky='we')

        # Timer Label
        self.label_timer = ttk.Label(root, text="")
        self.label_timer.pack(pady=5)

        # Info Button
        info_text = "ℹ"
        info_label = ttk.Label(root, text=info_text, cursor="hand2")
        info_label.configure(background='#1f1f2e', foreground='#bd93f9', font=('Arial', 16, 'bold'))
        info_label.pack(side=tk.TOP, padx=10, pady=10)
        info_label.bind("<Button-1>", lambda e: self.show_info())

        # Standardnachrichten-Datei prüfen oder erstellen
        self.message_file = "messages.txt"
        self.check_message_file()

        # Variablen für den Timer und den zuletzt gesendeten Index
        self.timer_job = None
        self.last_index = None

    def check_message_file(self):
        if not os.path.exists(self.message_file):
            with open(self.message_file, 'w', encoding='utf-8') as file:
                file.write(
                    "Pfirsich oder Eistee?\nWas mögt ihr mehr, Kaffee oder Tee?\nPizza oder Burger?\nNetflix oder Disney+?\n"
                    "Früh aufstehen oder lange schlafen?\nMarvel oder DC?\nZocken oder Sport machen?\nSnapchat oder Instagram?\n"
                    "Sommer oder Winter?\nLieblingssong aktuell?\nMac oder Windows?\nStädtetrip oder Strandurlaub?\n"
                    "Online shoppen oder im Laden?\nWelche Serie suchtet ihr gerade?\nTikTok oder YouTube?\nLieblingsessen ever?\n"
                    "Kino oder Couch?\nActionfilm oder Rom-Com?\nHunde oder Katzen?\nLieblingsgame?\nWhatsApp oder Telegram?\n"
                    "Sneakers oder Boots?\nBuch lesen oder Hörbuch?\nParty machen oder chillen?\nWelche Apps nutzt ihr am meisten?\n")

            messagebox.showinfo("Info",
                                f"Die Datei 'messages.txt' wurde erstellt.\nStandardnachrichten wurden hinzugefügt.")

    def start_script(self):
        try:
            cooldown_min = float(self.entry_min.get())
            cooldown_max = float(self.entry_max.get())
            if cooldown_min > cooldown_max:
                messagebox.showerror("Fehler", "Die minimale Zeit darf nicht größer als die maximale Zeit sein.")
                return
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlen ein.")
            return

        # Wenn ein Timer bereits läuft, stoppen wir ihn zuerst
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.stop_button.config(state=tk.NORMAL)
        self.start_sending(cooldown_min, cooldown_max)

    def start_sending(self, cooldown_min, cooldown_max):
        with open(self.message_file, 'r', encoding='utf-8') as file:
            string_array = file.readlines()
        string_array = [message.strip() for message in string_array]

        if not string_array:
            messagebox.showerror("Fehler", "Die Datei enthält keine Nachrichten.")
            return

        random.seed()

        def send_message():
            self.stop_button.config(state=tk.NORMAL)  # Den Stop-Button aktivieren
            index = random.randint(0, len(string_array) - 1)
            while index == self.last_index:
                index = random.randint(0, len(string_array) - 1)

            selected_string = string_array[index]
            pyperclip.copy(selected_string)  # Text in die Zwischenablage kopieren
            pyautogui.hotkey('ctrl', 'v')  # Einfügen des Textes

            pyautogui.press('enter')
            self.last_index = index

            cooldown = random.uniform(cooldown_min, cooldown_max)
            self.update_timer(cooldown)
            self.timer_job = self.root.after(int(cooldown * 1000), send_message)

        send_message()

    def stop_script(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
            self.stop_button.config(state=tk.DISABLED)
            self.label_timer.config(text="Nachrichtenversand gestoppt.")

    def update_timer(self, cooldown):
        if cooldown > 0:
            self.label_timer.config(text=f"Nächste Nachricht in: {cooldown:.2f} Sekunden")
            self.timer_job = self.root.after(100, lambda: self.update_timer(cooldown - 0.1))
        else:
            self.label_timer.config(text="Nachricht wird jetzt gesendet...")

    def show_info(self):
        info_text = "Dieses Tool sendet zufällige Nachrichten aus einer Datei in regelmäßigen Abständen.\n\n" \
                    "Geben Sie die minimale und maximale Zeit in Sekunden ein, zwischen denen die Nachrichten gesendet werden sollen.\n\n" \
                    "Die Nachrichten werden aus der Datei 'messages.txt' gelesen. Stellen Sie sicher, dass die Datei existiert und Nachrichten enthält.\n\n" \
                    "made by hskys on discord || wenn du dafür gezahlt hast wurdest du gescammed"

        messagebox.showinfo("Info", info_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoMessageSender(root)
    root.mainloop()
