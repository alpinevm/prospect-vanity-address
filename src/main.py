# used imports
import sys
import statistics
import math
import tkinter
import tkinter.messagebox
from lib import MinerOutputState, init_miner 
import customtkinter
from tkinter import StringVar
import pyperclip
from multiprocessing import Process, Queue
import time

# This function runs in a separate process
def data_collector(queue, search_str, prefix):
    datafeed = init_miner(search_str, prefix) 
    for data in datafeed:
        queue.put(data)
    print("Exiting miner process")

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

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

# colors (スペースゴッド)
primary_blue = "#307BF4"
secondary_blue = "#232A37"
tertiary_blue = '#213f72'
mid_blue = '#37669D'
dark_gray = "#282828"
redFaded= '#AD2B2B'
redLight= '#fa4142'
redDark= '#af2d2e'
errorRed= '#D50000'
successGreen= '#2ABA75'
successGreenDark= '#307755'
yellow= '#FFDC00'
yellowDark= '#FFC400'

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("PROSPECT")
        self.geometry(f"{600}x{335}")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.prefix = True 

        # ASCII
        self.title_label = tkinter.Text(self, bg=self.cget('bg'), height=9, width=180, bd=0, highlightthickness=0, fg="white")
        self.title_label.tag_configure("center", justify='center')
        self.title_label.insert('1.0', prospect_ascii)
        self.title_label.tag_add("center", "1.0", "end")
        self.title_label.grid(row=0, column=0, padx=20, pady=(0, 0))
        self.title_label.config(state=tkinter.DISABLED)  # This will disable user interaction

        # enter search string 
        self.search_entry_label = customtkinter.CTkLabel(self, text="Enter a Search String:", anchor="e")
        self.search_entry_label.grid(row=1, column=0, padx=20, pady=(0, 0))
        # search string input form
        self.search_entry = customtkinter.CTkEntry(self, placeholder_text="'C0FFEE'")
        self.search_entry.grid(row=1, column=0, padx=20, pady=(60, 0), sticky="ew")
        # update search button on type
        self.search_entry.bind("<Key>", self.enable_search_button)

        # button frames
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, pady=(20, 10))
        # start button
        self.start_button = customtkinter.CTkButton(self.button_frame, width=45, height=28, text="START", font=("Arial", 13, 'bold'), fg_color=("white", primary_blue), hover_color=(mid_blue))
        self.start_button.bind("<Button-1>", self.toggle_ends_button)
        self.start_button.pack(side="left", padx=2)
        #end button
        self.end_button = customtkinter.CTkButton(self.button_frame, text="END", width=45, height=28, font=("Arial", 12, 'bold'), fg_color=("white", dark_gray), hover_color=(mid_blue))
        self.end_button.bind("<Button-1>", self.toggle_starts_button)
        self.end_button.pack(side="left", padx=2)

        # Start Search Button
        self.search_button = customtkinter.CTkButton(master=self, command=self.start_search, height=40, text="START SEARCH", font=("Helvetica", 15, "bold"), state="disabled", bg_color=self.cget('bg'))
        self.search_button.grid(row=6, column=0, padx=200, pady=(12, 20), sticky="ew")

    def toggle_ends_button(self, event):
        self.prefix = True 
        self.start_button.configure(fg_color=("white", primary_blue))
        self.end_button.configure(fg_color=("white", dark_gray))

    def toggle_starts_button(self, event):
        self.prefix = False
        self.end_button.configure(fg_color=("white", primary_blue))
        self.start_button.configure(fg_color=("white", dark_gray))

    def enable_search_button(self, event):
        # Enable Search Entry
        self.search_entry.configure(state='normal')
        # Stop search if typing
        # try:
        #     self.stop_search()
        # except:
        #     pass
        # Enable Search Button
        self.search_button.configure(state="normal", fg_color=(primary_blue), hover_color=(tertiary_blue), bg_color=self.cget('bg'))

    def start_search(self):        
        # Create Search Screen
        self.search_screen = SearchScreen(
                master=self,
                width=600,
                search_str=(self.search_entry.get().lower()),
                prefix=self.prefix,
                height=400,
                corner_radius=10,
                bg_color=self.cget('bg')
            )
        self.search_screen.grid(row=10, rowspan=10, pady=(0, 5), column=0)
        # Resize Window
        self.geometry(f"{600}x{600}")
        # Stop Search Button
        self.search_button.configure(state="normal", fg_color=('#333333'), hover_color=('#555555'), text="STOP SEARCH", command=self.stop_search, bg_color=self.cget('bg'))
        # Disable Search Entry
        self.search_entry.configure(state='disabled')

    def stop_search(self):
        # Resize Window
        self.geometry(f"{600}x{335}")
        # Destroy Search Screen
        self.search_screen.destroy()
        # Enable Search Button
        self.search_button.configure(state="normal", fg_color=(primary_blue), hover_color=(tertiary_blue), text="START SEARCH", command=self.start_search, bg_color=self.cget('bg'))        
        # Enable Search Entry
        self.search_entry.configure(state='normal')

class SearchScreen(customtkinter.CTkFrame):
    def __init__(self, master, search_str, prefix: bool, **kwargs):
        super().__init__(master, **kwargs)
        # DATA
        self.search_str = search_str
        self.master = master
        self.kwargs = kwargs

        self.calculated_sim = False
        self.last_ten_mining_steps = []

        self.miner_data_queue = Queue()
        self.data_collector_process = Process(target=data_collector, args=(self.miner_data_queue, search_str,prefix,))
        self.data_collector_process.start()

        self.is_loading = True
        self.is_searching = False 
        self.is_errored = False 
        self.is_found = False
        self.current_search_speed = 189.905
        self.device_data = ' No device data found'
        self.error_message = 'You messed up big time ligma balls fr'
        self.found_address = '0xaaa2323a1fbec2e7e418eae55afcb0d2854b9436'
        self.found_pky = '0xa671038e0a59e034cd2868de98b52f67107219614b94a694b2173868155163a7'
        self.estimated_time = '13.43 seconds 50% - 2.43 mins 90% - 5.43 mins 99%'
        self.start_time = 0 # this should also be the time elapsed so just have this counting upwards when search starts


        if self.is_loading:
            # loading
            self.loading = customtkinter.CTkLabel(self, text=('Initializing...'), anchor="center", text_color=successGreen, font=('Sans', 50), justify='center')
            self.loading.grid(row=11, column=0, padx=165, pady=(85, 30), sticky='ew')
            # device data
            self.loading_2 = customtkinter.CTkLabel(self, text=("Collecting GPU device data..."), anchor="center", font=('Sans', 12), text_color='#777777', justify='center')
            self.loading_2.grid(row=15, column=0, padx=30, pady=(40, 10))
        if self.is_errored:
            # search failed
            self.current_search_speed_label = customtkinter.CTkLabel(self, text=("Search Failed"), anchor="center", font=('Sans', 14), justify='center')
            self.current_search_speed_label.grid(row=10, column=0, padx=10, pady=(10, 0), sticky='ew')  
            # error text
            self.current_search_err_label = customtkinter.CTkLabel(self, text="FATAL ERROR", anchor="center", text_color=errorRed, font=('Sans', 70), justify='center')
            self.current_search_err_label.grid(row=11, column=0, padx=10, pady=(20, 0), sticky='ew')
            # error msg
            self.current_search_err_label_text = customtkinter.CTkLabel(self, text=self.error_message, anchor="center", text_color=redLight, font=('Sans', 15), justify='center')
            self.current_search_err_label_text.grid(row=12, column=0, padx=10, pady=(0, 0), sticky='ew')
            # device data
            self.device_data_value = customtkinter.CTkLabel(self, text=(self.device_data), anchor="center", font=('Sans', 12), text_color='#777777', justify='center')
            self.device_data_value.grid(row=15, column=0, padx=30, pady=(45, 5))
            
        self.first_time_loading = True # this is just to make sure the loading screen only shows once
        self.update_gui()

    def esimate_time(self, z_targetprob, v_attemptspersecond):
        # Calculate z_targetprobability
        # Calculate p_guess
        p_guess = 16 ** (40 - len(self.search_str)) / 16 ** 40 
        # Calculate x
        x = abs((-math.log(1 - z_targetprob / 100)) / (math.log(1 - p_guess) * v_attemptspersecond))
        return x

    def update_gui(self):
        def format_time(seconds):
            if seconds > 1000000000:
                return "< 0.01 seconds"
            if seconds < 60:
                return f"{seconds:.2f} seconds"
            elif seconds < 3600:
                return f"{seconds / 60:.2f} minutes"
            elif seconds < 86400:
                return f"{seconds / 3600:.2f} hours"
            else:
                return f"{seconds / 86400:.2f} days"
        # Here you would update the labels in your GUI
        if not self.miner_data_queue.empty():
            data = self.miner_data_queue.get()
            if data['state'] == MinerOutputState.DEVICE_DATA:
                try:
                    self.loading_2.configure(text=data['data'])
                    self.device_data = data['data']
                except:
                    pass
            
            # SEARCHING SCREEN
            if data['state'] == MinerOutputState.MINING_SPEED:
                if not self.calculated_sim:
                    current_search_speed = data['data']['speed']
                    units: str = data['data']['units']
                    if units.lower().startswith('h'):
                        pass 
                    elif units.lower().startswith('kh'):
                        current_search_speed = current_search_speed * 1000
                    elif units.lower().startswith('mh'):
                        current_search_speed = current_search_speed * 1000000
                    elif units.lower().startswith('gh'):
                        current_search_speed = current_search_speed * 1000000000
                    elif units.lower().startswith('th'):
                        current_search_speed = current_search_speed * 1000000000000
                    self.last_ten_mining_steps.append(current_search_speed)

                # calculate time elapsed
                self.end_time = time.time()
                self.time_elapsed = self.end_time - self.start_time
                # destroy loading screen
                try:
                    self.loading.destroy()
                    self.loading_2.destroy()
                except:
                    pass
                if not self.calculated_sim and len(self.last_ten_mining_steps) == 10:
                    # if you got access to something higher, well then you've got higher priorities than this 
                    # calculate median 
                    self.calculated_sim = True
                    current_search_speed = statistics.median(self.last_ten_mining_steps)
                    p50 = self.esimate_time(50, current_search_speed)
                    p90 = self.esimate_time(90, current_search_speed)
                    p99 = self.esimate_time(99, current_search_speed)

                    esimated_time_str = "Estimated Time: " + format_time(p50) + " (50%) " + format_time(p90) + " (90%) " + format_time(p99) + " (99%)"

                    self.device_data_value = customtkinter.CTkLabel(self, text=(esimated_time_str + ("\n") + self.device_data), anchor="center", font=('Sans', 12), text_color='#777777', justify='center')
                    self.device_data_value.grid(row=15, column=0, padx=30, pady=(30, 10))

                    print("Median Search Speed (10 steps): " + str(current_search_speed))
                    print("p50: " + str(p50))
                    print("p90: " + str(p90))
                    print("p99: " + str(p99))

                if self.first_time_loading:
                    # calculate search speed
                    

                    # time elapsed
                    self.start_time = time.time()
                    self.current_search_speed_label = customtkinter.CTkLabel(self, text=("Time Elapsed: " + str(time.time() - self.start_time)), anchor="center", font=('Sans', 14), justify='center')
                    self.current_search_speed_label.grid(row=10, column=0, padx=10, pady=(10, 0), sticky='ew')  
                    # speed
                    self.current_search_speed_value = customtkinter.CTkLabel(self, text=str(self.current_search_speed), anchor="center", text_color=successGreen, font=('Sans', 90), justify='center')
                    self.current_search_speed_value.grid(row=11, column=0, padx=10, pady=(5, 0), sticky='ew')
                    # MH/s
                    self.current_search_speed_mhs = customtkinter.CTkLabel(self, text="MH/s", anchor="center", text_color=successGreen, font=('Sans', 18), justify='center')
                    self.current_search_speed_mhs.grid(row=12, column=0, padx=10, pady=(0, 0), sticky='ew')
                    self.device_data_value = customtkinter.CTkLabel(self, text=(self.device_data), anchor="center", font=('Sans', 12), text_color='#777777', justify='center')
                    self.device_data_value.grid(row=15, column=0, padx=30, pady=(30, 10))
                    # to not rerender entire screen
                    self.first_time_loading = False
                # update speed
                if self.current_search_speed_value.cget("text") != data['data']['speed']:
                    self.current_search_speed_value.configure(text=str(data['data']['speed']))
                # update MH/s
                if self.current_search_speed_mhs.cget("text") != (str(data['data']['units']) + "/s"):
                    self.current_search_speed_mhs.configure(text=(str(data['data']['units']) + "/s"))
                # update time elapsed
                if self.current_search_speed_label.cget("text") != ("Time Elapsed: " + str(format_time(time.time() - self.start_time))):
                    self.current_search_speed_label.configure(text=("Time Elapsed: " + str(format_time(time.time() - self.start_time))))

            # ADDRESS FOUND
            if data['state'] == MinerOutputState.FOUND:
                # calculate time elapsed
                self.end_time = time.time()
                self.time_elapsed = self.end_time - self.start_time
                # destroy components
                try:
                    self.loading.destroy()
                    self.loading_2.destroy()
                except:
                    pass
                try:
                    self.current_search_speed_label.destroy()
                except:
                    pass
                try:
                    self.current_search_speed_value.destroy()
                except:
                    pass
                try:
                    self.current_search_speed_mhs.destroy()
                except:
                    pass
                try:
                    self.current_search_err_label.destroy()
                except:
                    pass
                try:
                    self.current_search_err_label_text.destroy()
                except:
                    pass
                try:
                    self.device_data_value.destroy()
                except:
                    pass
                self.value_found = customtkinter.CTkLabel(self, text="ADDRESS MATCH FOUND!", anchor="center", text_color=successGreen, font=('Sans', 26, 'bold'), justify='center')
                self.value_found.grid(row=11, column=0, padx=10, pady=(10, 5), sticky='ew')
                # address
                self.address_label = customtkinter.CTkLabel(self, text=(self.found_address), anchor="center", font=('Sans', 13), text_color=successGreenDark, justify='center')
                self.address_label.grid(row=13, column=0, padx=30, pady=(10, 5))
                # copy address button
                self.copy_address_button = customtkinter.CTkButton(master=self, command=self.copy_address, fg_color=successGreenDark, hover_color=successGreenDark, text="Copy Address")
                self.copy_address_button.grid(row=14, column=0, padx=180, pady=(0, 0), sticky="ew")
                # pkey
                self.pkey_label = customtkinter.CTkLabel(self, text=(self.found_pky), anchor="center", font=('Sans', 13), text_color=redFaded, justify='center')
                self.pkey_label.grid(row=15, column=0, padx=30, pady=(10, 5))
                # copy pkey button
                self.copy_pkey_button = customtkinter.CTkButton(master=self, command=self.copy_pkey, fg_color=redDark, hover_color=redFaded, text="Copy Private Key")
                self.copy_pkey_button.grid(row=16, column=0, padx=180, pady=(0, 10), sticky="ew")
                # time elapsed & device data
                self.device_data_value = customtkinter.CTkLabel(self, text=("Time Elapsed - " + (str(format_time(time.time() - self.start_time))) + ("\n") + self.device_data), anchor="center", font=('Sans', 12), text_color='#777777', justify='center')
                self.device_data_value.grid(row=17, column=0, padx=30, pady=(20, 5))

                if self.address_label.cget("text") != data['data']['address']:
                    self.address_label.configure(text=str(data['data']['address']))
                if self.pkey_label.cget("text") != data['data']['private_key']:
                    self.pkey_label.configure(text=str(data['data']['private_key']))

            # ERROR
            if data['state'] == MinerOutputState.ERROR:
                # destroy loading screen
                try:
                    self.loading.destroy()
                    self.loading_2.destroy()
                except:
                    pass
                # search failed
                self.current_search_speed_label = customtkinter.CTkLabel(self, text=("Search Failed"), anchor="center", font=('Sans', 14), justify='center')
                self.current_search_speed_label.grid(row=10, column=0, padx=10, pady=(10, 0), sticky='ew')  
                # error text
                self.current_search_err_label = customtkinter.CTkLabel(self, text="FATAL ERROR", anchor="center", text_color=errorRed, font=('Sans', 70), justify='center')
                self.current_search_err_label.grid(row=11, column=0, padx=70, pady=(22, 0), sticky='ew')
                # error msg
                self.current_search_err_label_text = customtkinter.CTkLabel(self, text=data['message'], anchor="center", text_color=redDark, font=('Sans', 15), justify='center')
                self.current_search_err_label_text.grid(row=12, column=0, padx=10, pady=(0, 0), sticky='ew')
                # device data
                self.device_data_value = customtkinter.CTkLabel(self, text=(self.device_data), anchor="center", font=('Sans', 12), text_color='#777777', justify='center')
                self.device_data_value.grid(row=15, column=0, padx=30, pady=(45, 5))




        # self.update()
        # Schedule next GUI update
        self.after(10, self.update_gui)  # updates every 100 ms

    def destroy(self):
        # Override the destroy method to terminate the process when the GUI is closed
        self.data_collector_process.terminate()
        self.data_collector_process.join()
        super().destroy()

    def copy_address(self):
        address = self.address_label.cget("text")
        pyperclip.copy(address)
        self.copy_address_button.configure(text='Address Copied!')

    def copy_pkey(self):
        pkey = self.pkey_label.cget("text")
        pyperclip.copy(pkey)
        self.copy_pkey_button.configure(text='Private Key Copied!')


if __name__ == "__main__":
    app = App()
    app.mainloop()
