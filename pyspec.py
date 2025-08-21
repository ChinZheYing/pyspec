import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import pandas as pd 
import numpy as np

def configGridDim(frame,col,rw):
    for i in range(col):
        frame.grid_columnconfigure(i, weight=1, uniform="foo")
    for i in range(rw):
        frame.grid_rowconfigure(i, weight=1, uniform="foo")
        
def browseFiles(Master):
    # return filedialog.askopenfilename(parent=Master,initialdir = "/home/zheying/Downloads/genta_vis_sensing", title = "Select a File", filetypes = (("all files", "*.*"),("CSV files","*.csv*"),("Text files","*.txt")))
    return filedialog.askopenfilename(parent=Master,initialdir = "/", title = "Select a File", filetypes = (("CSV files","*.csv*"),("Text files","*.txt"),("Data point","*.dpt"), ("all files", "*.*")))

graph_settings = {'raw':{'title':'','x axis title':'Wavelength(nm)','y axis title':'Counts'},'trans':{'title':'','x axis title':'Wavelength(nm)','y axis title':'Transmittance'},'ext':{'title':'','x axis title':'Wavelength(nm)','y axis title':'Extinction'},'tauc':{'title':'','x axis title':'Photon Energy(eV)','y axis title':'(αE)²'}}
files = {'raw':[],'trans':[],'ext':[],'tauc':[]}

def import_trend(destroy,Master,legend,spectrum,spectrumbg,ref,refbg,specint,refint,delim,skip,mode):
    global files

    if legend == '':
        legend = spectrum
    files[mode].append({'spectrum':spectrum,'spectrum bg':spectrumbg,'ref':ref,'ref bg':refbg,'spectrum int':int(specint),'ref int':int(refint),'legend':legend,'delimiter':delim,'row skips':int(skip),'has fit range':False,'fit max':0,'fit min':0})
    plot_trend(Master,mode)
    destroy.destroy()


def plot_trend(Master,mode):
    global files

    fig = Figure(figsize = (5, 5), dpi = 100)
    plot = fig.add_subplot(1,1,1)
    delim = ','
    
    for file in files[mode]:
        if file['delimiter'] == 'comma':
            delim = ','
        elif file['delimiter'] == 'whitespace':
            delim = '\s+'
        df_spec  = pd.read_csv(file['spectrum'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])

        if mode != 'raw':
            df_spec_bg  = pd.read_csv(file['spectrum bg'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])
            df_ref  = pd.read_csv(file['ref'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])
            df_ref_bg  = pd.read_csv(file['ref bg'],delimiter=delim,skiprows=file['row skips'],header=None,names=['x', 'y'])

        if mode == 'raw':
            plot.plot(df_spec['x'], df_spec['y'],label=file['legend'])
        elif mode == 'trans':
            T = ((df_spec - df_spec_bg) / (df_ref - df_ref_bg)) * (file['ref int']/file['spectrum int'])
            plot.plot(df_spec['x'], T['y'],label=file['legend'])
        elif mode == 'ext':
            alpha = -np.log10(((df_spec - df_spec_bg) / (df_ref - df_ref_bg)) * (file['ref int']/file['spectrum int']))
            plot.plot(df_spec['x'], alpha['y'],label=file['legend'])
        elif mode == 'tauc':
            energy = 1240/df_spec['x']
            alpha = -np.log10(((df_spec - df_spec_bg) / (df_ref - df_ref_bg)) * (file['ref int']/file['spectrum int']))
            tauc = (alpha['y']*(energy))**2
            # print(tauc)
            plot.plot(energy, tauc,label=file['legend'])

            if (file['has fit range'] == True):
                minindex = 0
                maxindex = -1
                print(df_spec['x'][0])
                for i in range(len(df_spec['x'])):
                    if df_spec['x'][i] < file['fit min']:
                        minindex = i
                    if df_spec['x'][i] > file['fit max']:
                        maxindex = i
                        break
                slope, yintercept = np.polyfit(energy[minindex:maxindex], tauc[minindex:maxindex], 1) 
                xintercept = -yintercept/slope
                # print(xintercept)
                fit = np.poly1d([slope, yintercept])
                line = np.linspace(3, 4, 100)
                plot.plot(line, fit(line))#,label='Linear fit of steepest section'


    plot.legend()
    plot.set_title(graph_settings[mode]['title'])
    plot.set_xlabel(graph_settings[mode]['x axis title'])
    plot.set_ylabel(graph_settings[mode]['y axis title'])

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
    spectrum_file_path = StringVar()
    spectrum_intTime = StringVar()
    spectrum_bg_file_path = StringVar()
    ref_file_path = StringVar()
    ref_intTime = StringVar()
    delimiter = StringVar()
    ref_bg_file_path = StringVar()
    rowskip = StringVar()

    if mode == 'raw':
        spectrum_intTime.set('1')
        spectrum_bg_file_path.set('')
        ref_file_path.set('')
        ref_intTime.set('1')

    spectrum_legend_label = Label(master=top,text='Legend')
    spectrum_legend_label.grid(column=0,row=0,columnspan=1,rowspan=1,sticky='w')
    spectrum_legend_entry = Entry(master=top,textvariable=spectrum_legend)
    spectrum_legend_entry.grid(column=1,row=0,columnspan=3,rowspan=1,sticky='nsew')

    spectrum_path_label = Label(master=top,text='Spectrum Path')
    spectrum_path_label.grid(column=0,row=1,columnspan=1,rowspan=1,sticky='w')
    spectrum_path_entry = Entry(master=top,textvariable=spectrum_file_path)
    spectrum_path_entry.grid(column=1,row=1,columnspan=3,rowspan=1,sticky='nsew')
    spectrum_explore_btn = Button(master=top,text = "Browse Files",command = lambda: spectrum_file_path.set(browseFiles(top)))
    spectrum_explore_btn.grid(column=4,row=1,columnspan=1,rowspan=1,sticky='nsew')
    
    if mode != 'raw':
        spectrum_intTime_label = Label(master=top,text='Int Time:')
        spectrum_intTime_label.grid(column=5,row=1,columnspan=1,rowspan=1,sticky='nsew')
        spectrum_intTime_entry = Entry(master=top,textvariable=spectrum_intTime)
        spectrum_intTime_entry.grid(column=6,row=1,columnspan=1,rowspan=1,sticky='w')
        
        spectrum_bg_path_label = Label(master=top,text='Spectrum Bg Path')
        spectrum_bg_path_label.grid(column=0,row=2,columnspan=1,rowspan=1,sticky='w')
        spectrum_bg_path_entry = Entry(master=top,textvariable=spectrum_bg_file_path)
        spectrum_bg_path_entry.grid(column=1,row=2,columnspan=3,rowspan=1,sticky='nsew')
        spectrum_bg_explore_btn = Button(master=top,text = "Browse Files",command = lambda: spectrum_bg_file_path.set(browseFiles(top)))
        spectrum_bg_explore_btn.grid(column=4,row=2,columnspan=1,rowspan=1,sticky='nsew')

        ref_path_label = Label(master=top,text='Reference Path')
        ref_path_label.grid(column=0,row=3,columnspan=1,rowspan=1,sticky='w')
        ref_path_entry = Entry(master=top,textvariable=ref_file_path)
        ref_path_entry.grid(column=1,row=3,columnspan=3,rowspan=1,sticky='nsew')
        ref_explore_btn = Button(master=top,text = "Browse Files",command = lambda: ref_file_path.set(browseFiles(top)))
        ref_explore_btn.grid(column=4,row=3,columnspan=1,rowspan=1,sticky='nsew')
        
        ref_intTime_label = Label(master=top,text='Int Time:')
        ref_intTime_label.grid(column=5,row=3,columnspan=1,rowspan=1,sticky='nsew')
        ref_intTime_entry = Entry(master=top,textvariable=ref_intTime)
        ref_intTime_entry.grid(column=6,row=3,columnspan=1,rowspan=1,sticky='w')

        ref_bg_path_label = Label(master=top,text='Reference Bg Path')
        ref_bg_path_label.grid(column=0,row=4,columnspan=1,rowspan=1,sticky='w')
        ref_bg_path_entry = Entry(master=top,textvariable=ref_bg_file_path)
        ref_bg_path_entry.grid(column=1,row=4,columnspan=3,rowspan=1,sticky='nsew')
        ref_bg_explore_btn = Button(master=top,text = "Browse Files",command = lambda: ref_bg_file_path.set(browseFiles(top)))
        ref_bg_explore_btn.grid(column=4,row=4,columnspan=1,rowspan=1,sticky='nsew')
    
    delimiter.set('comma')
    delimiter_label = Label(master=top,text='Delimiter:')
    delimiter_label.grid(column=0,row=6,columnspan=1,rowspan=1,sticky='w')
    delimiter_combo = ttk.Combobox(master=top,textvariable=delimiter)
    delimiter_combo['values'] = ('comma','whitespace')
    delimiter_combo.grid(column=1,row=6,columnspan=1,rowspan=1,sticky='w')

    rowskip.set('1')
    rowskip_label = Label(master=top,text='Row skips:')
    rowskip_label.grid(column=2,row=6,columnspan=1,rowspan=1,sticky='E')
    rowskip_entry = Entry(master=top,textvariable=rowskip)
    rowskip_entry.grid(column=3,row=6,columnspan=1,rowspan=1,sticky='w')

    cancel_btn = Button(master=top,text = "Cancel",command = lambda:top.destroy())
    cancel_btn.grid(column=5,row=8,columnspan=1,rowspan=1,sticky='nsew')
    import_btn = Button(master=top,text = "Import",command = lambda: import_trend(top,Master,spectrum_legend.get(),spectrum_file_path.get(),spectrum_bg_file_path.get(),ref_file_path.get(),ref_bg_file_path.get(),spectrum_intTime.get(),ref_intTime.get(),delimiter.get(),rowskip.get(),mode))
    import_btn.grid(column=6,row=8,columnspan=1,rowspan=1,sticky='nsew')

    configGridDim(top,7,9)


def on_checkbox_change(checkbox_value, checkbox_var):
    pass
   
def create_checkboxes(root, files):
   checkboxes = []  # List to store BooleanVar objects for each checkbox

   for i in range(len(files)):
      checkbox_var = tk.BooleanVar()  # Variable to track the state of the checkbox
      checkbox = tk.Checkbutton(
         root,
         text=files[i]['legend'],
         variable=checkbox_var,
         command=lambda i=i, var=checkbox_var: on_checkbox_change(i+1, var)
      )
      checkbox.pack()
      checkboxes.append(checkbox_var)

   return checkboxes 

def remove_files(destroy,checkboxes,mode,Master):
    global files

    list_of_state = [i.get() for i in checkboxes]
    idx_to_del = []
    for i in range(len(list_of_state)):
        if list_of_state[i] == True:
            idx_to_del.append(i)

    new_files = [e for i, e in enumerate(files[mode]) if i not in idx_to_del]
    files[mode] = new_files
    plot_trend(Master,mode)

    destroy.destroy()

    
def open_remove_trend_window(Master,mode):
    global files

    top= Toplevel(Master)
    top.geometry("800x300")
    top.title("Remove Trend")

    checkboxes = create_checkboxes(top,files[mode])
    remove_btn = Button(top,text='Remove',command=lambda: remove_files(top,checkboxes,mode,Master),width=13)
    remove_btn.pack()

def fit_trend(destroy,Master,mode,trend_index_dict,minwave,maxwave,legend):
    global files

    files['tauc'][trend_index_dict[legend]]['has fit range'] = True
    files['tauc'][trend_index_dict[legend]]['fit min'] = float(minwave)
    files['tauc'][trend_index_dict[legend]]['fit max'] = float(maxwave)

    plot_trend(Master,mode)
    destroy.destroy()

def open_new_fit_window(Master,mode):
    global files

    trend_index_dict = {}

    top= Toplevel(Master)
    top.geometry("800x300")
    top.title("New Fit")

    spec = StringVar()
    spec_label = Label(master=top,text='Pick a spectrum:')
    spec_label.grid(column=0,row=0,columnspan=1,rowspan=1,sticky='E')
    spec_combo = ttk.Combobox(master=top,textvariable=spec)
    labels = []
    for i in range(len(files['tauc'])):
        trend_index_dict[files['tauc'][i]['legend']] = i
        labels.append(files['tauc'][i]['legend'])
    spec_combo['values'] = tuple(labels)
    spec_combo.grid(column=1,row=0,columnspan=1,rowspan=1,sticky='w')

    minwave = StringVar()
    minmave_label = Label(master=top,text='Min Wavelength:')
    minmave_label.grid(column=0,row=1,columnspan=1,rowspan=1,sticky='E')
    minwave_entry = Entry(master=top,textvariable=minwave)
    minwave_entry.grid(column=1,row=1,columnspan=1,rowspan=1,sticky='w')

    maxwave = StringVar()
    maxmave_label = Label(master=top,text='Max Wavelength:')
    maxmave_label.grid(column=0,row=2,columnspan=1,rowspan=1,sticky='E')
    maxwave_entry = Entry(master=top,textvariable=maxwave)
    maxwave_entry.grid(column=1,row=2,columnspan=1,rowspan=1,sticky='w')

    fit_btn = Button(master=top,text = "Fit",command = lambda:fit_trend(top,Master,mode,trend_index_dict,minwave.get(),maxwave.get(),spec.get()))
    fit_btn.grid(column=6,row=8,columnspan=1,rowspan=1,sticky='nsew')

    configGridDim(top,7,9)




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
tauc_tab = ttk.Frame(tabControl)

tabControl.add(raw_tab, text ='Raw')
tabControl.add(trans_tab, text ='Transmittance')
tabControl.add(ext_tab, text ='Extinction')
tabControl.add(tauc_tab, text ='Tauc')
tabControl.pack(expand = 1, fill ="both")


# Raw Tab
raw_menubar = ttk.Frame(raw_tab)
raw_import_btn = Button(raw_menubar,text='Import',command=lambda: open_import_trans_trend_window(raw_tab,'raw'),width=13)
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

# Tauc Tab
tauc_menubar = ttk.Frame(tauc_tab)
tauc_import_btn = Button(tauc_menubar,text='Import',command=lambda: open_import_trans_trend_window(tauc_tab,'tauc'),width=13)
tauc_import_btn.pack(side = LEFT,padx=2)
tauc_remove_btn = Button(tauc_menubar,text='Remove',command=lambda: open_remove_trend_window(tauc_tab,'tauc'),width=13)
tauc_remove_btn.pack(side = LEFT,padx=2)
tauc_add_fit_btn = Button(tauc_menubar,text='New Fit',command=lambda: open_new_fit_window(tauc_tab,'tauc'),width=13)
tauc_add_fit_btn.pack(side = LEFT,padx=2)
tauc_edit_fit_btn = Button(tauc_menubar,text='Edit Fit',command=None,width=13)
tauc_edit_fit_btn.pack(side = LEFT,padx=2)
tauc_menubar.grid(row=0, column=0, sticky='nsew',columnspan=10)
configGridDim(tauc_tab,10,17)


window.mainloop()  