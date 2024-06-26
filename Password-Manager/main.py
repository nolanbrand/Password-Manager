from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for letter in range(randint(8, 10))]
    password_list += [choice(symbols) for symbol in range(randint(2, 4))]
    password_list += [choice(numbers) for number in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(first=0, last=END)
    password_entry.insert(index=0, string=password)
    pyperclip.copy(password)


# ---------------------------- SAVE / FIND PASSWORD ------------------------------- #
def save():
    new_website = website_entry.get()
    new_email_username = email_user_entry.get()
    new_password = password_entry.get()
    new_data = {
        new_website: {
            "email": new_email_username,
            "password": new_password
        }
    }

    if len(new_website) == 0 or len(new_password) == 0 or len(new_email_username) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(first=0, last=END)
            password_entry.delete(first=0, last=END)


def find_password():
    existing_website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="File Does Not Exist", message="No data file found.")
    else:
        is_there = existing_website in data
        if is_there:
            messagebox.showinfo(title=existing_website, message=f"Email/Username: {data[existing_website]['email']} "
                                                                f"\nPassword: {data[existing_website]['password']}")
        else:
            messagebox.showinfo(title="No Website Found", message="No details for the website exists.")



# ---------------------------- UI SETUP ------------------------------- #
#main window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=30, bg="white")

#MyPass image
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
MyPass_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=MyPass_img)
canvas.grid(column=1, row=0)

#text labels
website_label = Label(text="Website:", bg="white")
website_label.grid(column=0, row=1)
email_user_label = Label(text="Email/Username:", bg="white")
email_user_label.grid(column=0, row=2)
password_label = Label(text="Password:", bg="white")
password_label.grid(column=0, row=3)

#User entries
website_entry = Entry(width=31)
website_entry.grid(column=1, row=1, columnspan=2, sticky="w")
website_entry.focus()
email_user_entry = Entry(width=48)
email_user_entry.grid(column=1, row=2, columnspan=2, sticky="w")
email_user_entry.insert(index=0, string="nolanpbrand@gmail.com")
password_entry = Entry(width=31)
password_entry.grid(column=1, row=3, sticky="w")

#buttons
generate_button = Button(text="Generate Password", font=("Arial", 7), command=generate_password)
generate_button.grid(column=2, row=3, sticky="w")
add_button = Button(text="Add", width=40, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="w", pady=5)
search_button = Button(text="Search", width=11, command=find_password)
search_button.grid(column=2, row=1, columnspan=2, pady=5)

window.mainloop()
