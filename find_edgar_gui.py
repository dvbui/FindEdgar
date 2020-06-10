import tkinter as tk
from find_edgar import *

oo = 1e9
companies = []


def update_companies(file_name, label_var):
    global companies
    try:
        companies = from_cik_to_company(cik_file=file_name, verbose=False, no_of_companies=oo)
    except FileNotFoundError:
        pass
    label_var.set("{} companies found".format(len(companies)))


main_window = tk.Tk()
input_frame = tk.Frame(main_window)
input_frame.grid(row=0)


def generate_input_form():
    main_window.title("Find Edgar")
    tk.Label(input_frame, text='CIK File').grid(row=0)
    cik_info_var = tk.StringVar()
    cik_info_label = tk.Label(input_frame, textvariable=cik_info_var)
    cik_file_var = tk.StringVar()
    cik_file_entry = tk.Entry(input_frame, textvariable=cik_file_var)
    cik_file_var.trace("w", lambda name, index, mode, sv=cik_file_var: update_companies(cik_file_entry.get(),
                                                                                        cik_info_var))
    cik_file_entry.grid(row=0, column=1)
    cik_info_label.grid(row=0, column=2)
    tk.Label(input_frame, text='Words File').grid(row=1)
    word_file_entry = tk.Entry(input_frame)
    word_file_entry.grid(row=1, column=1)
    tk.Label(input_frame, text='Output File').grid(row=2)
    output_file_entry = tk.Entry(input_frame)
    output_file_entry.grid(row=2, column=1)


generate_input_form()
main_window.mainloop()
