from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
BG = "#e73f1a"
YELLOW = "#FDFD96"
LITE_ORANGE = "#fbc680"
FONT = ("Bebas", 15, "normal")
ENTRY_FONT = ("Impact", 15, "normal")


# ----------------------------------------------- PASSWORD GENERATOR ------------------------------------------------- #
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for letter in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for symbol in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for number in range(random.randint(2, 4))]

    random.shuffle(password_list)

    random_password = "".join(password_list)

    password_entry.delete(0, END)

    password_entry.insert(END, string=random_password)

    pyperclip.copy(random_password)


# ---------------------------------------------- SAVE PASSWORD ------------------------------------------------------- #
def save():
    website = site_entry.get()
    email_username = email_entry.get()
    password = password_entry.get()
    new_data_dict = {
        website: {
            "Username: ": email_username,
            "Password: ": password
        }
    }

    if len(website) == 0 or len(email_username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please don't leave the fields empty.")
        return
    is_data_ok = messagebox.askokcancel(title=f"Details of {website}",
                                        message=f"Email/Username: {email_username}"
                                                f"\nPassword: {password}\n\nIs it okay to save?")
    if is_data_ok:
        try:
            with open(file="data.json", mode="r") as data:
                # Reading json
                json_data = json.load(data)

        except FileNotFoundError:
            with open(file="data.json", mode="w") as data:
                json.dump(new_data_dict, data, indent=4)
        else:
            # Updating json
            json_data.update(new_data_dict)

            with open(file="data.json", mode="w") as data:
                # Saving updated json
                json.dump(json_data, data, indent=4)

        finally:
            site_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


# --------------------------------------------- SEARCH PASSWORD ------------------------------------------------------ #
def search_data():
    # TODO 1 loading json file
    website = site_entry.get()
    try:
        with open(file="data.json", mode="r") as data:
            search_json = json.load(data)
    except FileNotFoundError:
        messagebox.showerror(title="File Error", message="No data file found.")
    else:
        if website in search_json:
            email_address = search_json[website]["Username: "]
            the_password = search_json[website]["Password: "]
            messagebox.showinfo(title=website, message=f"Email/Username: {email_address}\n"
                                                       f"Password: {the_password}")
        else:
            messagebox.showerror(title="Search Error", message=f"No details for {website} found.")


# ----------------------------------------------- UI SETUP ----------------------------------------------------------- #
# Window
window = Tk()
window.title("VamZ Password Manager")
window.config(padx=50, pady=50, bg=BG)

# Logo image
canvas = Canvas(height=200, width=300, bg=BG, highlightthickness=0)
logo = PhotoImage(file="./logo.png")
canvas.create_image(150, 100, image=logo)
canvas.grid(column=1, row=0)
# -------------------------------------------------- WIDGETS --------------------------------------------------------- #
# Labels
site = Label(text="Website: ")
site.config(font=FONT, bg=BG, fg=LITE_ORANGE)
site.grid(column=0, row=1)

email = Label(text="Email/Username: ")
email.config(font=FONT, bg=BG, fg=LITE_ORANGE)
email.grid(column=0, row=2)

password_text = Label(text="Password: ")
password_text.config(font=FONT, bg=BG, fg=LITE_ORANGE)
password_text.grid(column=0, row=3)

# Entry
site_entry = Entry()
site_entry.config(bg=YELLOW, font=ENTRY_FONT)
site_entry.grid(column=1, row=1, sticky="EW")

email_entry = Entry()
email_entry.config(bg=YELLOW, font=ENTRY_FONT)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

password_entry = Entry()
password_entry.config(bg=YELLOW, font=ENTRY_FONT)
password_entry.grid(column=1, row=3, sticky="EW")

# Buttons
search = Button(text="Search", command=search_data)
search.config(bg=BG, font=("Impact", 10, "normal"), fg=LITE_ORANGE)
search.grid(column=2, row=1, sticky="EW")

generate_password = Button(text="Generate Password", command=generate_pass)
generate_password.config(bg=BG, font=("Impact", 10, "normal"), fg=LITE_ORANGE)
generate_password.grid(column=2, row=3)

add_entry = Button(text="ADD", command=save)
add_entry.config(bg=BG, font=("Impact", 12, "normal"), fg=LITE_ORANGE)
add_entry.grid(column=1, row=4, columnspan=2, sticky="EW")
# ------------------------------------------------END OF WIDGETS------------------------------------------------------ #
window.mainloop()
