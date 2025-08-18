import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

import pandas as pd 
import numpy as np

def configGridDim(frame,col,rw):
    for i in range(col):
        frame.grid_columnconfigure(i, weight=1, uniform="foo")
    for i in range(rw):
        frame.grid_rowconfigure(i, weight=1, uniform="foo")
        
def browseFiles(Master):
    return filedialog.askopenfilename(parent=Master,initialdir = "/home/zheying/Downloads/testtauc", title = "Select a File", filetypes = (("CSV files","*.csv*"), ("all files", "*.*")))




raw_files = []

def import_raw(destroy,Master,filename,legend,delim,skip):
    global raw_files
    if legend == '':
        legend = filename
    raw_files.append({'path':filename,'legend':legend,'delimiter':delim,'row skips':int(skip)})
    plot_raws(Master)
    destroy.destroy()

def plot_raws(Master):
    global raw_files
    fig = Figure(figsize = (5, 5), dpi = 100)
    plot = fig.add_subplot(1,1,1)

    for file in raw_files:
        if file['delimiter'] == 'comma':
            delim = ','
        elif file['delimiter'] == 'whitespace':
            delim = '\s+'
        df  = pd.read_csv(file['path'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])
        plot.plot(df['x'], df['y'],label=file['legend'])

    plot.legend()

    canvas = FigureCanvasTkAgg(fig, master = Master)  
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew',columnspan=10,rowspan=15)
    toolbarframe = Frame(master=Master)
    toolbar = NavigationToolbar2Tk(canvas, toolbarframe)
    toolbar.update()
    toolbarframe.grid(row=16, column=0, sticky='nsew',columnspan=10)

def open_import_raw_trend_window(Master):
    top= Toplevel(Master)
    top.geometry("800x300")
    top.title("Import Trend")

    spectrum_legend = StringVar()
    spectrum_legend_label = Label(master=top,text='Legend')
    spectrum_legend_label.grid(column=0,row=0,columnspan=1,rowspan=1,sticky='nsew')
    spectrum_legend_entry = Entry(master=top,textvariable=spectrum_legend)
    spectrum_legend_entry.grid(column=1,row=0,columnspan=3,rowspan=1,sticky='nsew')

    spectrum_file_path = StringVar()
    spectrum_path_label = Label(master=top,text='Path')
    spectrum_path_label.grid(column=0,row=1,columnspan=1,rowspan=1,sticky='nsew')
    spectrum_path_entry = Entry(master=top,textvariable=spectrum_file_path)
    spectrum_path_entry.grid(column=1,row=1,columnspan=3,rowspan=1,sticky='nsew')
    spectrum_explore_btn = Button(master=top,text = "Browse Files",command = lambda: spectrum_file_path.set(browseFiles(top)))
    spectrum_explore_btn.grid(column=4,row=1,columnspan=1,rowspan=1,sticky='nsew')

    delimiter = StringVar()
    delimiter_label = Label(master=top,text='Delimiter:')
    delimiter_label.grid(column=0,row=3,columnspan=1,rowspan=1,sticky='w')
    delimiter_combo = ttk.Combobox(master=top,textvariable=delimiter)
    delimiter_combo['values'] = ('comma','whitespace')
    delimiter_combo.grid(column=1,row=3,columnspan=1,rowspan=1,sticky='w')

    rowskip = StringVar()
    rowskip_label = Label(master=top,text='Row skips:')
    rowskip_label.grid(column=2,row=3,columnspan=1,rowspan=1,sticky='E')
    rowskip_entry = Entry(master=top,textvariable=rowskip)
    rowskip_entry.grid(column=3,row=3,columnspan=1,rowspan=1,sticky='w')

    cancel_btn = Button(master=top,text = "Cancel",command = lambda:top.destroy())
    cancel_btn.grid(column=3,row=8,columnspan=1,rowspan=1,sticky='nsew')
    import_btn = Button(master=top,text = "Import",command = lambda: import_raw(top,Master,spectrum_file_path.get(),spectrum_legend.get(),delimiter.get(),rowskip.get()))
    import_btn.grid(column=4,row=8,columnspan=1,rowspan=1,sticky='nsew')


    configGridDim(top,5,8)






trans_files = []
ext_files = []
def import_trans(destroy,Master,legend,spectrum,spectrumbg,ref,refbg,specint,refint,delim,skip):
    global trans_files
    if legend == '':
        legend = spectrum
    trans_files.append({'spectrum':spectrum,'spectrum bg':spectrumbg,'ref':ref,'ref bg':refbg,'spectrum int':int(specint),'ref int':int(refint),'legend':legend,'delimiter':delim,'row skips':int(skip)})
    plot_trans(Master)
    destroy.destroy()

def plot_trans(Master):
    global trans_files
    fig = Figure(figsize = (5, 5), dpi = 100)
    plot = fig.add_subplot(1,1,1)
    delim = ','
    
    for file in trans_files:
        if file['delimiter'] == 'comma':
            delim = ','
        elif file['delimiter'] == 'whitespace':
            delim = '\s+'
        df_spec  = pd.read_csv(file['spectrum'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])
        df_spec_bg  = pd.read_csv(file['spectrum bg'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])
        df_ref  = pd.read_csv(file['ref'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])
        df_ref_bg  = pd.read_csv(file['ref bg'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])

            # return (spectra - bg) / ((ref - bg) * spectraOverRefFactor)
        T = ((df_spec - df_spec_bg) / (df_ref - df_ref_bg)) * (file['spectrum int']/file['ref int'])

        plot.plot(df_spec['x'], T['y'],label=file['legend'])

    plot.legend()

    canvas = FigureCanvasTkAgg(fig, master = Master)  
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew',columnspan=10,rowspan=15)
    toolbarframe = Frame(master=Master)
    toolbar = NavigationToolbar2Tk(canvas, toolbarframe)
    toolbar.update()
    toolbarframe.grid(row=16, column=0, sticky='nsew',columnspan=10)

def import_ext(destroy,Master,legend,spectrum,spectrumbg,ref,refbg,specint,refint,delim,skip):
    global ext_files
    if legend == '':
        legend = spectrum
    ext_files.append({'spectrum':spectrum,'spectrum bg':spectrumbg,'ref':ref,'ref bg':refbg,'spectrum int':int(specint),'ref int':int(refint),'legend':legend,'delimiter':delim,'row skips':int(skip)})
    plot_ext(Master)
    destroy.destroy()

def plot_ext(Master):
    global ext_files
    fig = Figure(figsize = (5, 5), dpi = 100)
    plot = fig.add_subplot(1,1,1)
    delim = ','
    for file in ext_files:
        if file['delimiter'] == 'comma':
            delim = ','
        elif file['delimiter'] == 'whitespace':
            delim = '\s+'
        df_spec  = pd.read_csv(file['spectrum'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])
        df_spec_bg  = pd.read_csv(file['spectrum bg'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])
        df_ref  = pd.read_csv(file['ref'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])
        df_ref_bg  = pd.read_csv(file['ref bg'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])

        alpha = -np.log10(((df_spec - df_spec_bg) / (df_ref - df_ref_bg)) * (file['spectrum int']/file['ref int']))
        plot.plot(df_spec['x'], alpha['y'],label=file['legend'])

    plot.legend()
    # handles, labels = plot.gca().get_legend_handles_labels()
    # by_label = dict(zip(labels, handles))
    # plot.legend(by_label.values(), by_label.keys())

    canvas = FigureCanvasTkAgg(fig, master = Master)  
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew',columnspan=10,rowspan=15)
    toolbarframe = Frame(master=Master)
    toolbar = NavigationToolbar2Tk(canvas, toolbarframe)
    toolbar.update()
    toolbarframe.grid(row=16, column=0, sticky='nsew',columnspan=10)


def open_import_trans_trend_window(Master,mode):
    top= Toplevel(Master)
    top.geometry("800x300")
    top.title("Import Trend")

    spectrum_legend = StringVar()
    spectrum_legend_label = Label(master=top,text='Legend')
    spectrum_legend_label.grid(column=0,row=0,columnspan=1,rowspan=1,sticky='w')
    spectrum_legend_entry = Entry(master=top,textvariable=spectrum_legend)
    spectrum_legend_entry.grid(column=1,row=0,columnspan=3,rowspan=1,sticky='nsew')

    spectrum_file_path = StringVar()
    spectrum_path_label = Label(master=top,text='Spectrum Path')
    spectrum_path_label.grid(column=0,row=1,columnspan=1,rowspan=1,sticky='w')
    spectrum_path_entry = Entry(master=top,textvariable=spectrum_file_path)
    spectrum_path_entry.grid(column=1,row=1,columnspan=3,rowspan=1,sticky='nsew')
    spectrum_explore_btn = Button(master=top,text = "Browse Files",command = lambda: spectrum_file_path.set(browseFiles(top)))
    spectrum_explore_btn.grid(column=4,row=1,columnspan=1,rowspan=1,sticky='nsew')
    spectrum_intTime = StringVar()
    spectrum_intTime_label = Label(master=top,text='Int Time:')
    spectrum_intTime_label.grid(column=5,row=1,columnspan=1,rowspan=1,sticky='nsew')
    spectrum_intTime_entry = Entry(master=top,textvariable=spectrum_intTime)
    spectrum_intTime_entry.grid(column=6,row=1,columnspan=1,rowspan=1,sticky='w')
    
    spectrum_bg_file_path = StringVar()
    spectrum_bg_path_label = Label(master=top,text='Spectrum Bg Path')
    spectrum_bg_path_label.grid(column=0,row=2,columnspan=1,rowspan=1,sticky='w')
    spectrum_bg_path_entry = Entry(master=top,textvariable=spectrum_bg_file_path)
    spectrum_bg_path_entry.grid(column=1,row=2,columnspan=3,rowspan=1,sticky='nsew')
    spectrum_bg_explore_btn = Button(master=top,text = "Browse Files",command = lambda: spectrum_bg_file_path.set(browseFiles(top)))
    spectrum_bg_explore_btn.grid(column=4,row=2,columnspan=1,rowspan=1,sticky='nsew')

    ref_file_path = StringVar()
    ref_path_label = Label(master=top,text='Reference Path')
    ref_path_label.grid(column=0,row=3,columnspan=1,rowspan=1,sticky='w')
    ref_path_entry = Entry(master=top,textvariable=ref_file_path)
    ref_path_entry.grid(column=1,row=3,columnspan=3,rowspan=1,sticky='nsew')
    ref_explore_btn = Button(master=top,text = "Browse Files",command = lambda: ref_file_path.set(browseFiles(top)))
    ref_explore_btn.grid(column=4,row=3,columnspan=1,rowspan=1,sticky='nsew')
    ref_intTime = StringVar()
    ref_intTime_label = Label(master=top,text='Int Time:')
    ref_intTime_label.grid(column=5,row=3,columnspan=1,rowspan=1,sticky='nsew')
    ref_intTime_entry = Entry(master=top,textvariable=ref_intTime)
    ref_intTime_entry.grid(column=6,row=3,columnspan=1,rowspan=1,sticky='w')

    ref_bg_file_path = StringVar()
    ref_bg_path_label = Label(master=top,text='Reference Bg Path')
    ref_bg_path_label.grid(column=0,row=4,columnspan=1,rowspan=1,sticky='w')
    ref_bg_path_entry = Entry(master=top,textvariable=ref_bg_file_path)
    ref_bg_path_entry.grid(column=1,row=4,columnspan=3,rowspan=1,sticky='nsew')
    ref_bg_explore_btn = Button(master=top,text = "Browse Files",command = lambda: ref_bg_file_path.set(browseFiles(top)))
    ref_bg_explore_btn.grid(column=4,row=4,columnspan=1,rowspan=1,sticky='nsew')


    delimiter = StringVar()
    delimiter_label = Label(master=top,text='Delimiter:')
    delimiter_label.grid(column=0,row=6,columnspan=1,rowspan=1,sticky='w')
    delimiter_combo = ttk.Combobox(master=top,textvariable=delimiter)
    delimiter_combo['values'] = ('comma','whitespace')
    delimiter_combo.grid(column=1,row=6,columnspan=1,rowspan=1,sticky='w')

    rowskip = StringVar()
    rowskip_label = Label(master=top,text='Row skips:')
    rowskip_label.grid(column=2,row=6,columnspan=1,rowspan=1,sticky='E')
    rowskip_entry = Entry(master=top,textvariable=rowskip)
    rowskip_entry.grid(column=3,row=6,columnspan=1,rowspan=1,sticky='w')


    cancel_btn = Button(master=top,text = "Cancel",command = lambda:top.destroy())
    cancel_btn.grid(column=3,row=8,columnspan=1,rowspan=1,sticky='nsew')
    if mode == 'trans':
        import_btn = Button(master=top,text = "Import",command = lambda: import_trans(top,Master,spectrum_legend.get(),spectrum_file_path.get(),spectrum_bg_file_path.get(),ref_file_path.get(),ref_bg_file_path.get(),spectrum_intTime.get(),ref_intTime.get(),delimiter.get(),rowskip.get()))
    elif mode == 'ext':
        import_btn = Button(master=top,text = "Import",command = lambda: import_ext(top,Master,spectrum_legend.get(),spectrum_file_path.get(),spectrum_bg_file_path.get(),ref_file_path.get(),ref_bg_file_path.get(),spectrum_intTime.get(),ref_intTime.get(),delimiter.get(),rowskip.get()))
    import_btn.grid(column=4,row=8,columnspan=1,rowspan=1,sticky='nsew')

    configGridDim(top,7,8)


# Function called when a checkbox is clicked
def on_checkbox_change(checkbox_value, checkbox_var):
#    print(f"Checkbox {checkbox_value} is {'checked' if checkbox_var.get() else 'unchecked'}")
    pass
   
# Function to create multiple checkboxes using a loop
def create_checkboxes(root, files):
   checkboxes = []  # List to store BooleanVar objects for each checkbox

   # Loop to create checkboxes dynamically
   for i in range(len(files)):
      checkbox_var = tk.BooleanVar()  # Variable to track the state of the checkbox
      checkbox = tk.Checkbutton(
         root,
         text=files[i]['legend'],
         variable=checkbox_var,
         command=lambda i=i, var=checkbox_var: on_checkbox_change(i+1, var)
      )
      checkbox.pack()  # Place the checkbox in the window
      checkboxes.append(checkbox_var)  # Add the variable to the list

   return checkboxes  # Return the list of checkbox variables

def remove_files(destroy,checkboxes,mode):
    global raw_files
    global trans_files
    global ext_files
    files_from_mode = {'raw': raw_files,'trans':trans_files,'ext':ext_files}

    list_of_state = [i.get() for i in checkboxes]
    idx_to_del = []
    for i in range(len(list_of_state)):
        if list_of_state[i] == True:
            idx_to_del.append(i)

    new_files = [e for i, e in enumerate(files_from_mode[mode]) if i not in idx_to_del]

    if mode == 'raw':
        raw_files = new_files
        plot_raws(raw_tab)
    elif mode == 'trans':
        trans_files = new_files
        plot_trans(trans_tab)
    elif mode == 'ext':
        ext_files = new_files
        plot_ext(ext_tab)

    destroy.destroy()

    
def open_remove_trend_window(Master,mode):
    global raw_files
    global trans_files
    global ext_files
    files_from_mode = {'raw': raw_files,'trans':trans_files,'ext':ext_files}

    top= Toplevel(Master)
    top.geometry("800x300")
    top.title("Remove Trend")

    checkboxes = create_checkboxes(top,files_from_mode[mode])
    remove_btn = Button(top,text='Remove',command=lambda: remove_files(top,checkboxes,mode),width=13)
    remove_btn.pack()
   



# Variables
windowWidth = 1080
windowHeight = 720


window = tk.Tk()
window.title("Spectrum Toolkit")
window.geometry('{}x{}'.format(windowWidth,windowHeight))   
tabControl = ttk.Notebook(window)

raw_tab = ttk.Frame(tabControl)
trans_tab = ttk.Frame(tabControl)
ext_tab = ttk.Frame(tabControl)

tabControl.add(raw_tab, text ='Raw')
tabControl.add(trans_tab, text ='Transmittance')
tabControl.add(ext_tab, text ='Extinction')
tabControl.pack(expand = 1, fill ="both")


# Raw Tab
raw_menubar = ttk.Frame(raw_tab)
raw_import_btn = Button(raw_menubar,text='Import',command=lambda: open_import_raw_trend_window(raw_tab),width=13)
raw_import_btn.pack(side = LEFT,padx=2)
raw_remove_btn = Button(raw_menubar,text='Remove',command=lambda: open_remove_trend_window(raw_tab,'raw'),width=13)
raw_remove_btn.pack(side = LEFT,padx=2)
raw_menubar.grid(row=0, column=0, sticky='nsew',columnspan=10)
configGridDim(raw_tab,10,17)


# Trans Tab
trans_menubar = ttk.Frame(trans_tab)
trans_import_btn = Button(trans_menubar,text='Import',command=lambda: open_import_trans_trend_window(trans_tab,'trans'),width=13)
trans_import_btn.pack(side = LEFT,padx=2)
trans_remove_btn = Button(trans_menubar,text='Remove',command=lambda: open_remove_trend_window(trans_tab,'trans'),width=13)
trans_remove_btn.pack(side = LEFT,padx=2)
trans_menubar.grid(row=0, column=0, sticky='nsew',columnspan=10)
configGridDim(trans_tab,10,17)

# Extinction Tab
ext_menubar = ttk.Frame(ext_tab)
ext_import_btn = Button(ext_menubar,text='Import',command=lambda: open_import_trans_trend_window(ext_tab,'ext'),width=13)
ext_import_btn.pack(side = LEFT,padx=2)
ext_remove_btn = Button(ext_menubar,text='Remove',command=lambda: open_remove_trend_window(ext_tab,'ext'),width=13)
ext_remove_btn.pack(side = LEFT,padx=2)
ext_menubar.grid(row=0, column=0, sticky='nsew',columnspan=10)
configGridDim(ext_tab,10,17)


window.mainloop()  