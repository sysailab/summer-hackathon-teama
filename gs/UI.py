import tkinter as tk
import json

class UI():
    def print_data(self, key_entry, dir_entry):
        key = key_entry.get() # key input data
        dir = dir_entry.get() # dir input data
        print(f"Key: {key}, Dir: {dir}")
        return dir

    def start(self, config):
        root = tk.Tk()
        
        root.geometry(config["size"])
        
        frame = tk.Frame(root)
        frame.pack(anchor='center')
        
        key_config = config["key_config"]
        dir_config = config["dir_config"]
        
        tk.Label(frame, text="Key").grid(row=0, column=0, padx=key_config["label_padx"], pady=key_config["label_pady"])
        tk.Label(frame, text="Dir").grid(row=1, column=0, padx=dir_config["label_padx"], pady=dir_config["label_pady"])

        key_entry = tk.Entry(frame, width=key_config["input_width"])
        dir_entry = tk.Entry(frame, width=dir_config["input_width"])

        key_entry.grid(row=0, column=1, padx=key_config["label_padx"], pady=key_config["label_pady"])
        dir_entry.grid(row=1, column=1, padx=dir_config["label_padx"], pady=dir_config["label_pady"])

        tk.Button(frame, text='Print', command=self.print_data(key_entry, dir_entry)).grid(row=2, column=1, pady=4)

        root.mainloop()

