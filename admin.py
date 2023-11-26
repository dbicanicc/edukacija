import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, Scrollbar
from database import add_user, edit_user, delete_user, Session, Osoba

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Sučelje")
        self.root.geometry("400x400")

        #kreiranje glavnog okvira
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        #dodavanje gumba
        self.btn_add_user = tk.Button(self.frame, text="Dodaj korisnika", command=self.add_user)
        self.btn_edit_user = tk.Button(self.frame, text="Uredi korisnika", command=self.edit_user)
        self.btn_delete_user = tk.Button(self.frame, text="Obriši korisnika", command=self.delete_user)

        #postavljanje gumba u okvir
        self.btn_add_user.grid(row=0, column=1, padx=5, pady=5)
        self.btn_edit_user.grid(row=0, column=2, padx=5, pady=5)
        self.btn_delete_user.grid(row=0, column=3, padx=5, pady=5)

        #kreiranje liste osoba koje se nalaze u bazi sa mogućnosti odabira
        self.users_listbox = Listbox(self.frame, selectmode=tk.SINGLE)
        self.users_listbox.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky=tk.NSEW)

        #klizač
        scrollbar = Scrollbar(self.frame, orient=tk.VERTICAL, command=self.users_listbox.yview)
        scrollbar.grid(row=1, column=4, padx=5, pady=5, sticky=tk.NS)
        self.users_listbox.config(yscrollcommand=scrollbar.set)

        self.load_users()

    # Dohvaćanje osoba iz baze i prikaz u listi
    def load_users(self):
        session = Session()
        users = session.query(Osoba).all()
        session.close()

        self.users_listbox.delete(0, tk.END)
        for user in users:
            user_info = f"{user.ime} {user.prezime} ({user.pin}){' (Aktivan)' if user.aktivna else ''}"
            self.users_listbox.insert(tk.END, user_info)

    #dodavanje nove osobe
    def add_user(self):
        user_dialog = tk.Toplevel(self.root)
        user_dialog.title("Dodaj korisnika")

        user_frame = tk.Frame(user_dialog)
        user_frame.grid(row=0, column=0, padx=10, pady=10)

        first_name = simpledialog.askstring("Dodaj korisnika", "Ime:")
        last_name = simpledialog.askstring("Dodaj korisnika", "Prezime:")
        pin = simpledialog.askstring("Dodaj korisnika", "PIN:")

        if first_name and last_name and pin:
            add_user(first_name, last_name, pin)
            messagebox.showinfo("Korisnik dodan", "Korisnik je uspješno dodan.")
            user_dialog.destroy()
            self.load_users()
        else:
            messagebox.showerror("Greška", "Morate unijeti ime, prezime i PIN korisnika.")
            
    #uređivanje osoba u bazi
    def edit_user(self):
        selected_user = self.users_listbox.get(tk.ACTIVE)
        if selected_user:
            parts = selected_user.split()
            if len(parts) >= 3:
                pin = parts[2]
                response = messagebox.askyesno("Potvrda", "Jeste li sigurni da želite uređivati ovog korisnika?")
                if response:
                    user_dialog = tk.Toplevel(self.root)
                    user_dialog.title("Uredi korisnika")

                    user_frame = tk.Frame(user_dialog)
                    user_frame.grid(row=0, column=0, padx=10, pady=10)

                    first_name = simpledialog.askstring("Uredi korisnika", "Ime:")
                    last_name = simpledialog.askstring("Uredi korisnika", "Prezime:")
                    new_pin = simpledialog.askstring("Uredi korisnika", "Novi PIN:")

                    if first_name and last_name and new_pin:
                        edit_user(pin, first_name, last_name, new_pin)
                        messagebox.showinfo("Korisnik uređen", "Podaci korisnika su ažurirani.")
                        user_dialog.destroy()
                        self.load_users()
                    else:
                        messagebox.showerror("Greška", "Morate unijeti ime, prezime i novi PIN korisnika.")
        else:
            messagebox.showerror("Greška", "Niste odabrali korisnika za uređivanje.")

    def delete_user(self):
        selected_user = self.users_listbox.get(tk.ACTIVE)
        if selected_user:
            parts = selected_user.split()
            if len(parts) >= 3:
                pin = parts[2]
                response = messagebox.askyesno("Potvrda", "Jeste li sigurni da želite obrisati ovog korisnika?")
                if response:
                    delete_user(pin)
                    self.load_users()
        else:
            messagebox.showerror("Greška", "Niste odabrali korisnika za brisanje.")

if __name__ == "__main__":
    root = tk.Tk()
    admin_app = AdminApp(root)
    root.mainloop()
