
import tkinter as tk
from tkinter import messagebox, simpledialog
from database import Session, Osoba


class SmartKeyApp:
    def __init__(self, root):
        # Inicijalizacija glavnog OKVIRA
        self.root = root
        self.root.title("SmartKey App")
        self.root.geometry("400x500")  # Postavljanje dimenzija sučelja na 400x500 piksela

        # Kreiranje glavnog okvira
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, padx=5, pady=5)

        # Dodavanje gumba za pozivanje i otključavanje vrata
        self.btn_call = tk.Button(self.frame, text="Pozovi", command=self.animate_call)
        self.btn_unlock = tk.Button(self.frame, text="Otključaj", command=self.enter_unlock_pin)

        # Postavljanje gumba na okvir
        self.btn_call.grid(row=0, column=0, padx=5, pady=5)
        self.btn_unlock.grid(row=0, column=1, padx=5, pady=5)

        # Kreiranje brojčanih tipki
        self.create_number_buttons()

        # Unos za prikaz rezultata
        self.result_entry = tk.Entry(self.frame, font=("Arial", 24), state="readonly")
        self.result_entry.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.result_entry.configure(justify="center")  # Centrirajte tekst unutar Entry widgeta

        # Inicijalizacija varijabli za unesene brojeve i PIN za otključavanje
        self.entered_numbers = ""
        self.unlock_pin = ""

        # Gumb za brisanje posljednjeg unesenog broja
        self.btn_back = tk.Button(self.frame, text="Back", command=self.delete_last_number)
        self.btn_back.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        # Unos za PIN
        self.pin_entry = tk.Entry(self.frame, show="", font=("Arial", 24))
        self.pin_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")  # Dodajte sticky="ew" kako biste postavili širinu na fill

    def number_clicked(self, number):
        self.pin_entry.insert(tk.END, number)

    def animate_call(self):
        # Animacija gumba za pozivanje, nepotrebno al se činilo zgodno
        self.btn_call.config(state="disabled")
        self.btn_call.update()

        for _ in range(5):
            self.btn_call.config(bg="red")
            self.btn_call.update()
            self.root.after(300)
            self.btn_call.config(bg="light gray")
            self.btn_call.update()
            self.root.after(300)

        self.btn_call.config(state="active")

    def enter_unlock_pin(self):
        # Unos PIN-a za otključavanje
        self.unlock_pin = self.pin_entry.get()
        if self.unlock_pin:
            self.unlock()

    def unlock(self):
        # Provjera unesenog PIN-a u bazi podataka
        entered_pin = self.unlock_pin
        session = Session()
        user = session.query(Osoba).filter_by(pin=entered_pin).first()

        if user:
            self.result_entry.config(state="normal")  # Omogući unos u Entry widget za prikaz rezultata
            self.result_entry.delete(0, tk.END)  # Obrišite prethodni rezultat
            self.result_entry.insert(tk.END, "WELCOME HOME" +" "+ user.ime)  # Ispis poruke i imena osobe
            self.result_entry.config(state="readonly")  # Ponovno onemogući unos u Entry widget
        else:
            self.result_entry.config(state="normal")
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(tk.END, "Pogrešan unos")
            self.result_entry.config(state="readonly")

        session.close()

    def create_number_buttons(self):
        # Kreiranje brojčanih tipki
        number_frame = tk.Frame(self.frame)
        number_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        number_buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            '*', '0', '#'
        ]

        for i in range(4):
            for j in range(3):
                num = number_buttons[i * 3 + j]
                number_label = tk.Label(number_frame, text=num, width=6, height=3, relief="groove", borderwidth=3)
                number_label.grid(row=i, column=j)
                number_label.bind("<Button-1>", lambda event, n=num: self.number_clicked(n))

    def delete_last_number(self):
        # Brisanje posljednjeg unesenog broja iz PIN-a
        pin = self.pin_entry.get()
        if pin:
            new_pin = pin[:-1]
            self.pin_entry.delete(0, tk.END)
            self.pin_entry.insert(0, new_pin)

    def update_display(self):
        self.result_entry.config(text=self.entered_numbers)

# Pokretanje glavnog programa
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartKeyApp(root)
    root.mainloop()
