import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import StringVar

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

prospect_ascii = """
                                     _   
                                    | |  
 _ __  _ __ ___  ___ _ __   ___  ___| |_ 
| '_ \| '__/ _ \/ __| '_ \ / _ \/ __| __|
| |_) | | | (_) \__ \ |_) |  __/ (__| |_ 
| .__/|_|  \___/|___/ .__/ \___|\___|\__|
| |                 | |                  
|_|                 |_|                  
"""

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("PROSPECT")
        self.geometry(f"{600}x{400}")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Title
        self.title_label = tkinter.Text(self, bg=self.cget('bg'), height=9, width=180, bd=0, highlightthickness=0, fg="white")
        self.title_label.tag_configure("center", justify='center')
        self.title_label.insert('10.0', prospect_ascii)
        self.title_label.tag_add("center", "1.0", "end")
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.title_label.config(state=tkinter.DISABLED)  # This will disable user interaction

        # Switch
        self.slide_var = StringVar(value="Leading")
        self.slide_switch = customtkinter.CTkSwitch(
            self, variable=self.slide_var, text='', onvalue="Leading", offvalue="Trailing"
        )
        self.slide_switch.grid(row=1, column=0)  # You may need to adjust the position

        # Switch Labels
        self.leading_label = customtkinter.CTkLabel(self, text="LEADING")
        self.leading_label.grid(row=1, column=0, sticky="e")  # You may need to adjust the position
        self.trailing_label = customtkinter.CTkLabel(self, text="TRAILING")
        self.trailing_label.grid(row=1, column=0, sticky="w")  # You may need to adjust the position

        # Search String Input
        self.search_entry_label = customtkinter.CTkLabel(self, text="Search String:", anchor="w")
        self.search_entry_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.search_entry = customtkinter.CTkEntry(self, placeholder_text="1a2b3c")
        self.search_entry.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.search_entry.bind("<Key>", self.enable_search_button)

        # Search Button
        self.search_button = customtkinter.CTkButton(master=self, text="SEARCH", state="disabled", bg_color="gray")
        self.search_button.grid(row=4, column=0, padx=20, pady=(10, 30), sticky="ew")

    def enable_search_button(self, event):
        self.search_button.configure(state="normal", bg_color="blue")


if __name__ == "__main__":
    app = App()
    app.mainloop()
