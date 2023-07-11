import tkinter as tk
import os
import json
from PdfAPI import PdfApi

class UI():
    def __init__(self) -> None:
        self.pdfapi = PdfApi()
    
    def process_start(self, key_entry, dir_entry):
        key = key_entry.get() # key input data
        dir = dir_entry.get() # dir input data
        print(f"Key: {key}, Dir: {dir}")
        
        files = self.file_list_maker(dir)
        
        for i in range(len(files)):
            result_list = self.pdfapi_process(f'{dir}/{files[i]}')
            if result_list[0] and result_list[1] is not None:
                print("find successfully")
            
            else : print("fail")
            # TODO : 제목 저자 중 하나 이상 에러 -> 재혁이 태스크로
        
        return dir
    
    def pdfapi_process(self, dir):
        s_id = self.pdfapi.add_adf_via_url(dir)
        result = self.pdfapi.ask_of_pdf(s_id)
        result_list = self.pdfapi.extract_result(result)
        
        return result_list
    
    def file_list_maker(self, dir):
        files = os.listdir(dir) # 디렉토리의 모든 파일과 폴더를 가져옴
        pdf_files = [file for file in files if file.endswith('.pdf')] # .pdf 확장자를 가진 파일들만 선택
        return pdf_files

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

        tk.Button(frame, text='Print', command=lambda: self.process_start(key_entry, dir_entry)).grid(row=2, column=1, pady=4)
        
        root.mainloop()

