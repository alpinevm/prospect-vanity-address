import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import StringVar

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("PROSPECT")
        self.geometry(f"{500}x{300}")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Title
        self.title_label = customtkinter.CTkLabel(self, text="PROSPECT", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Slide Selector
        self.slide_var = StringVar(value="Leading")
        self.slide_switch = customtkinter.CTkSwitch(
            self, variable=self.slide_var, onvalue="Leading", offvalue="Trailing"
        )
        self.slide_switch.grid(row=1, column=0)  # You may need to adjust the position


        # Add labels for the switch
        self.leading_label = customtkinter.CTkLabel(self, text="LEADING")
        self.leading_label.grid(row=1, column=0, sticky="e")  # You may need to adjust the position
        self.trailing_label = customtkinter.CTkLabel(self, text="TRAILING")
        self.trailing_label.grid(row=1, column=0, sticky="w")  # You may need to adjust the position

        # Search String Entry
        self.search_entry_label = customtkinter.CTkLabel(self, text="Search String:", anchor="w")
        self.search_entry_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.search_entry = customtkinter.CTkEntry(self, placeholder_text="1a2b3c")
        self.search_entry.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.search_entry.bind("<Key>", self.enable_search_button)

        # Search Button
        self.search_button = customtkinter.CTkButton(master=self, text="SEARCH", state="disabled", bg_color="gray")
        self.search_button.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="ew")

    def enable_search_button(self, event):
        self.search_button.configure(state="normal", bg_color="blue")


if __name__ == "__main__":
    app = App()
    app.mainloop()
