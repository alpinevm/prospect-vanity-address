import tkinter
import tkinter.messagebox
from lib.main import MinerOutputState, dummy_miner
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

# Data
is_mining = False
current_mining_speed = 0
GPUs = ''
addresses_found = ''
is_errored = False
error_message = ''

# Colors
primary_blue = "#307BF4"
secondary_blue = "#232A37"
tertiary_blue = '#213f72'
mid_blue = '#37669D'
dark_gray = "#282828"

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
        self.title_label.grid(row=0, column=0, padx=20, pady=(0, 0))
        self.title_label.config(state=tkinter.DISABLED)  # This will disable user interaction

        # Search String Input
        self.search_entry_label = customtkinter.CTkLabel(self, text="Enter a Search String:", anchor="e")
        self.search_entry_label.grid(row=1, column=0, padx=20, pady=(0, 0))
        self.search_entry = customtkinter.CTkEntry(self, placeholder_text="C0FFEE")
        self.search_entry.grid(row=1, column=0, padx=20, pady=(60, 0), sticky="ew")
        self.search_entry.bind("<Key>", self.enable_search_button)

        # Button Frame
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, pady=(20, 10))

        # Buttons
        self.start_button = customtkinter.CTkButton(self.button_frame, text="STARTS WITH", fg_color=("white", primary_blue), hover_color=(mid_blue))
        self.start_button.bind("<Button-1>", self.toggle_ends_button)
        self.start_button.pack(side="left", padx=2)

        self.end_button = customtkinter.CTkButton(self.button_frame, text="ENDS WITH", fg_color=("white", dark_gray), hover_color=(mid_blue))
        self.end_button.bind("<Button-1>", self.toggle_starts_button)
        self.end_button.pack(side="left", padx=2)

        # Search Button
        self.search_button = customtkinter.CTkButton(master=self, command=self.start_mining, text="START SEARCH", state="disabled", bg_color=self.cget('bg'))
        self.search_button.grid(row=6, column=0, padx=200, pady=(10, 30), sticky="ew")

        # Store the original UI state
        self.original_ui_state = self.state()

    def start_mining(self):
        # INSERT UI SWITCHING HERE
        pass

    def toggle_ends_button(self, event):
        self.start_button.configure(fg_color=("white", primary_blue))
        self.end_button.configure(fg_color=("white", dark_gray))

    def toggle_starts_button(self, event):
        self.end_button.configure(fg_color=("white", primary_blue))
        self.start_button.configure(fg_color=("white", dark_gray))


    def enable_search_button(self, event):
        self.search_button.configure(state="normal", fg_color=(primary_blue), hover_color=(tertiary_blue), bg_color=self.cget('bg'))


if __name__ == "__main__":
    app = App()
    app.mainloop()
