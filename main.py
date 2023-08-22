import json
import pyotp
import customtkinter
import time
import pyperclip
import tkinter
from PIL import Image

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x400")
app.title("HHTNQ AUTHY")
app.columnconfigure((0, 1), weight=1)
app.iconbitmap('ico.ico')


def gui():

    def copy_event():
        pyperclip.copy(generated_code.cget("text"))

    def processing_data(event):
        if radio_var.get() == 0:
            global warning_label
            output_label.configure(text="Choose your platform")
        else:
            output_label.configure(text="")
            output_search_input = search_input.get().lower()
            found_items = []
            for dictionary in original_data:
                if "name" in dictionary and dictionary["name"].lower() == output_search_input:
                    found_items.append(dictionary)
            if found_items == []:
                output_label.configure(
                    text="Current key is not found!", fg_color="#3b1516")
            else:
                output_label.configure(
                    text=f"{found_items[0]['name']}", fg_color="#325937")
                old_radio = radio_var.get()
                update_otp_time(found_items[0], output_search_input, old_radio)

    def update_otp_time(found_items, output_search_input, old_radio):
        new_search_input = search_input.get().lower()
        if output_search_input == new_search_input:
            key = found_items
            secret_code = key['key']
            totp = pyotp.TOTP(secret_code)
            authy_code = totp.now()
            remaining_code = round(
                totp.interval - (time.time() % totp.interval))
            generated_code.configure(text=f"{authy_code}")
            timer_left.configure(text=f"{remaining_code}")
            app.after(1000, update_otp_time, found_items,
                      output_search_input, old_radio)

    def bitmart_event():
        try:
            with open('pairs_bitmart.json', 'r') as json_file:
                global original_data
                original_data = ""
                original_data = json.load(json_file)
                return (original_data)
        except FileNotFoundError:
            warning_label = customtkinter.CTkLabel(
                master=app, text=f"File pairs_bitmart.json is not found!!!", fg_color="red")
            warning_label.grid(pady=10, padx=10, row=6,
                               columnspan=2, sticky="n")

    def superx_event():
        try:
            with open('pairs_superx.json', 'r') as json_file:
                global original_data
                original_data = ""
                original_data = json.load(json_file)
                return (original_data)
        except FileNotFoundError:
            warning_label = customtkinter.CTkLabel(
                master=app, text=f"File pairs_superx.json is not found!!!", fg_color="red")
            warning_label.grid(pady=10, padx=10, row=6,
                               columnspan=2, sticky="n")

    search_label = customtkinter.CTkLabel(
        master=app, text="Search by email", font=("TkTextFont", 20))
    search_label.grid(row=0, columnspan=2, pady=10, padx=10, sticky="n")
    search_input = customtkinter.CTkEntry(
        master=app, border_width=1, border_color="#4b4e6e", width=200)
    search_input.grid(pady=10, padx=10, row=1, columnspan=2, sticky="n")
    search_input.bind('<KeyRelease>', lambda event: processing_data(event))
    update_image = customtkinter.CTkImage(light_image=Image.open(
        "update.ico"), dark_image=Image.open("update.ico"), size=(30, 30))
    image_label = customtkinter.CTkButton(
        app, image=update_image, text="", width=30, height=30, fg_color="#4b4e6e")
    image_label.bind('<ButtonPress-1>', lambda event: processing_data(event))
    image_label.grid(padx=40, row=1, column=1, sticky="e")
    frame = customtkinter.CTkFrame(master=app, height=30)
    frame.grid(pady=10, padx=10, row=2, columnspan=2, sticky="n")
    output_label = customtkinter.CTkLabel(
        master=frame, text="", font=("TkTextFont", 15), width=200, height=30, corner_radius=45)
    output_label.grid(pady=10, padx=10, sticky="n")
    generated_code_label = customtkinter.CTkLabel(
        master=app, text="Code: ", font=("TkTextFont", 20))
    generated_code_label.grid(pady=10, padx=10, row=3,
                              columnspan=2, sticky="w")
    generated_code = customtkinter.CTkLabel(
        master=app, text=f"", font=("TkTextFont", 20))
    generated_code.grid(pady=10, padx=10, row=3, columnspan=2, sticky="n")
    timer_left = customtkinter.CTkLabel(
        master=app, text=f"", font=("TkTextFont", 20))
    timer_left.grid(pady=10, padx=10, row=3, columnspan=2, sticky="e")
    copy_btn = customtkinter.CTkButton(
        master=app, text="Copy to clipboard", fg_color="#4b4e6e", command=copy_event, font=("TkTextFont", 15))
    copy_btn.grid(pady=10, padx=10, row=4, columnspan=2, sticky="n")
    radio_var = tkinter.IntVar(value=0)
    bitmart = customtkinter.CTkRadioButton(app, text="Bitmart",
                                           command=bitmart_event, variable=radio_var, value=1)
    bitmart.bind('<ButtonPress-1>', lambda event: processing_data(event))
    bitmart.grid(pady=10, padx=10, row=5, column=0, sticky="n")
    superx = customtkinter.CTkRadioButton(app, text="superx",
                                          command=superx_event, variable=radio_var, value=2)
    superx.bind('<ButtonPress-1>', lambda event: processing_data(event))
    superx.grid(pady=10, padx=10, row=5, column=1, sticky="n")


if __name__ == "__main__":
    key_first = None
    gui()
    app.mainloop()
