from tkinter import *
from tkinter import messagebox
import random
from pyperclip import *
import json

BGCOLOR = "#FFFFFF"


def allowed_user():

    # ---------------------------- SEARCH PASSWORD ------------------------------- #
    def find_password():
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="File Not Found", message="No data file found")
        else:
            if website_input.get() in data:
                search_email = data[website_input.get()]["email"]
                search_pswd = data[website_input.get()]["password"]
                messagebox.showinfo(title="details",
                                    message=f"The saved details for {website_input.get()} is :\nEmail: {search_email}\nPassword: {search_pswd}")
            else:
                messagebox.showerror(title="Data not found", message="No details for the website exists")

    # ---------------------------- PASSWORD GENERATOR ------------------------------- #
    def generate_password():
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                   'P',
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = random.randint(6, 9)
        nr_symbols = random.randint(1, 3)
        nr_numbers = random.randint(2, 4)

        password_list = []

        password_list += [random.choice(letters) for _ in range(nr_letters)]

        password_list += [random.choice(symbols) for _ in range(nr_symbols)]

        password_list += [random.choice(numbers) for _ in range(nr_numbers)]

        random.shuffle(password_list)

        password = "".join(password_list)
        password_text.insert(0, password)
        copy(password)

    # ---------------------------- SAVE PASSWORD ------------------------------- #
    def save():
        website = website_input.get()
        password = password_text.get()
        email = username_input.get()
        new_data = {website:
            {
                "email": email,
                "password": password
            }
        }
        if len(website) == 0 or len(password) == 0:
            messagebox.showwarning(title='Oops!', message="Please don't leave any boxes empty.")
        else:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
                    if website in data:
                        is_agree = messagebox.askyesno(title="This website already exists",
                                                       message="This website already exists\nDo you want to change the save password?")
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
                    messagebox.showinfo(title="Success", message="Your password has been saved successfully.")
            else:
                if not is_agree:
                    pass
                else:
                    # updating old data with new data
                    data.update(new_data)
                    with open("data.json", "w") as data_file:
                        # loading the updated data to the file
                        json.dump(data, data_file, indent=4)
                        messagebox.showinfo(title="Success", message="Your password has been saved successfully.")

            finally:
                website_input.delete(0, 'end')
                password_text.delete(0, 'end')

    # ---------------------------- SECOND SCREEN ------------------------------- #

    website_label = Label(text="Website", bg=BGCOLOR)
    website_label.config(pady=5, padx=5)
    website_label.grid(column=0, row=1)

    username_label = Label(text="Email/Username", bg=BGCOLOR)
    username_label.config(pady=5, padx=5)
    username_label.grid(column=0, row=2)

    pswd_label = Label(text="Password", bg=BGCOLOR)
    pswd_label.grid(column=0, row=3)
    pswd_label.config(pady=8, padx=5)

    # Entry widgets
    website_input = Entry(width=14, highlightthickness=0, borderwidth=2)
    website_input.grid(column=1, row=1, sticky="w")
    website_input.focus()

    username_input = Entry(width=30, highlightthickness=0, borderwidth=2)
    username_input.grid(column=1, row=2, columnspan=2)
    username_input.insert(0, "yourname@gmail.com")

    password_text = Entry(width=14, highlightthickness=0, borderwidth=2)
    password_text.grid(column=1, row=3, sticky="w")

    # buttons
    generate_pswd_btn = Button(text="Generate Password", highlightthickness=0, border=0, bd=0, bg=BGCOLOR,
                               activebackground="white", width=11,
                               command=generate_password)
    generate_pswd_btn.config(pady=3)
    generate_pswd_btn.grid(column=2, row=3, sticky="e")

    add_btn = Button(width=28, text="Add", highlightthickness=0, border=0, bd=0, bg=BGCOLOR, activebackground="white",
                     command=save)
    add_btn.config(pady=3)
    add_btn.grid(column=1, row=4, columnspan=2, sticky="w")

    search_btn = Button(text="Search", highlightthickness=0, border=0, bd=0, bg=BGCOLOR, width=11,
                        command=find_password)
    search_btn.config(pady=3)
    search_btn.grid(column=2, row=1, sticky="e")

    def status():
        if checked_state.get() == 0:
            password_text.config(show="•")
        else:
            password_text.config(show="")

    # checkbox
    checked_state = IntVar()
    checked_state.set(1)
    show_password = Checkbutton(text="Show Password", highlightthickness=0, onvalue=1, offvalue=0,
                                variable=checked_state,
                                command=status)
    show_password.grid(column=2, row=5, sticky="e")


# ---------------------------- MASTER LOGIN SCREEN ------------------------------- #
window = Tk()
window.config(pady=100, padx=60, bg=BGCOLOR)
window.title("Password Manager")

canvas = Canvas(width=100, height=100, bg=BGCOLOR, highlightthickness=0)
logo_image = PhotoImage(file="img.png")
canvas.create_image(50, 40, image=logo_image)
canvas.grid(column=1, row=0)

master_label = Label(text="Enter your master password", bg=BGCOLOR)
master_label.grid(column=1, row=1)
master_label.config(pady=7, padx=110)

master_password_entry = Entry(width=20, highlightthickness=0, borderwidth=2)
master_password_entry.grid(column=1, row=2)
master_password_entry.focus()

space = Label(text="", bg=BGCOLOR)
space.grid(column=1, row=3)


def verify_user():
    if master_password_entry.get() == "password":
        allowed_user()
        master_label.grid_remove()
        master_password_entry.grid_remove()
        master_login_btn.grid_remove()
    else:
        messagebox.showerror(title="Error", message="Invalid Login Credential, Try again!")
        master_password_entry.delete(0, END)


master_login_btn = Button(text="Log In", highlightthickness=0, bd=0, command=verify_user)
master_login_btn.config(pady=5, padx=3)
master_login_btn.grid(column=1, row=4)
window.mainloop()
