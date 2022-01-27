# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:10:40 2021

@author: Computer
"""
from numpy import sqrt, linspace, exp, tan
from math import pi, atan, degrees
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure, imread, imshow
from smithplot import SmithAxes
from tkinter import Label, Frame, Tk, messagebox
from tkinter.ttk import Notebook, Combobox, Entry, Button
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

root = Tk()
root.title("Диаграмма Вольперта")
root.geometry("1300x700") 
root.resizable(False, False)

def validation(input): 
    try: 
        if input == '':
            return True
        elif input == "-":
            return True
        else:
            x = float(input)
            return True
    except ValueError:
        return False

SmithAxes.update_scParams({"symbol.infinity.correction": 10})
SmithAxes.update_scParams({"axes.xlabel.rotation": float(0)})
SmithAxes.update_scParams({"axes.xlabel.fancybox": {"boxstyle": "round4,pad=0.1,rounding_size=0.8",
                                           "facecolor": 'w',
                                           "edgecolor": "w",
                                           "mutation_aspect": 0.90,
                                           "alpha": 1},
                           "symbol.ohm": "Ом",
                           "grid.major.color": "0.05",
                           "grid.minor.color": "0.1",
                           })
tab_control = Notebook(root)  

#ПЕРВАЯ ВКЛАДКА
tab1 = Frame(tab_control, bg ='white')  
tab_control.add(tab1, text='Расчет режима работы')  
tab_control.grid(ipadx = 190 , ipady = 295)

def get_values_tab1():
    R = tab1_vvod131.get()
    X = tab1_vvod132.get()
    Zv = tab1_vvod12.get()
    L = tab1_vvod133.get()
    
    if (R == '' and X == '') or Zv == '' or L == '':
        messagebox.showinfo('Ошибка ввода данных', 'Проверьте, все ли поля заполнены!')
        return False
    elif float(Zv) == 0:
        messagebox.showinfo('Ошибка ввода данных', 'Волновое сопротивление не должно быть нулевым!')
        return False
    elif float(L) <= 0:
        messagebox.showinfo('Ошибка ввода данных', 'Длина волны должна быть больше нуля!')
        return False
    else: 
        Zv = float(Zv)
        L = float(L)
        if R == '':
            R = 0
            X = float(X)
        elif X == '':
            X = 0
            R = float(R)
        else:
            R = float(R)
            X = float(X)
        
        graph_tab1(R, X, Zv, L)
                        
            
def graph_tab1(R, X, Zv, L):
    Z = R+1j*X
    ro = (Z/Zv - 1)/(Z/Zv + 1)
    z = linspace(0, 2*pi, 100)
    Up = exp(-1j*z)
    Uo = ro*exp(1j*z)
    U=Up+Uo
    I = (exp(-1j*(z+pi/2)) + ro*exp(1j*(z+pi/2)))/Z
    try:
        KSV = round((1+abs(ro))/(1-abs(ro)), 2)
    except ZeroDivisionError:
        KSV = 'бесконечность'
    Pot = round(abs((Uo*Uo/Up*Up))[0], 2)
    abs_ro = abs(ro)
    if ro.real != 0:
        phase_ro = atan(ro.imag/ro.real)
        phase = degrees(phase_ro%(2*pi))
        if phase > 180: 
            phase -= 360
    
    
    #Smith строим
    SmithAxes.update_scParams(axes_impedance = Zv)
    SmithAxes.update_scParams({"axes.radius": float(0.53)})
    tab1_figure = Figure(figsize=(5,5))
    tab1_figure.set_figheight(5.6)
    tab1_figure.set_figwidth(12.8)
    ax = tab1_figure.add_subplot(1, 2, 1, projection='smith')
    Z = R+1j*X
    canvas = FigureCanvasTkAgg(tab1_figure, tab1_frame_canvas)
     
    #строим графики тока и напряжения
    ax1 = tab1_figure.add_subplot(3, 2, 4)
    ax2 = ax1.twinx()
    ax1.grid()
    ax3 = tab1_figure.add_subplot(3, 2, 2)
    ax3.patch.set_visible(False)
    ax3.axis('off')
    if ro.real != 0:
        text1 = f'     КСВ = {KSV} \n\n      Pот\n   ——— = {Pot}\n     Pпад \n\nρ = {round(abs_ro, 2)}×exp({round(phase, 2)}j)'
    elif ro.real == 0:
        text1 = f'     КСВ = {KSV} \n\n      Pот\n   ——— = {Pot}\n     Pпад \n\n      ρ = 0'
        
    ax3.text(0.37, 0.1, text1, font='Times New Roman', size = 14)
    ax.plot(Z, datatype='Z', markersize="10", color="#FF0000")
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax1.plot(z*L/20*pi, abs(U), label= '|U|', color = '#00005c')
    ax1.plot(z*L/20*pi, abs(I*Z), '--',label = '|J|', color='#660e00')
    ax1.set_ylabel('|Un|, |Jn|', size = 10)
    ax1.set_xlabel('Z, мм', size = 10)
    ax1.text(0.9*L, -0.7, 'НАГРУЗКА', font='Times New Roman', size = 13)
    ax1.legend(prop={"size":12, 'family':'Times New Roman'})
    ax1.set_xlim(0, L)
    ax2.set_xlim(0, L)
    ax1.set_ylim(-0.0000001, 2.01)
    ax2.set_ylim(-0.0000001, 2.01)
    ax2.axis('off')
    ax1.tick_params(axis='both', which='major', labelsize=11)
    canvas = FigureCanvasTkAgg(tab1_figure, tab1_frame_canvas)
    canvas.get_tk_widget().grid(row=5)
    canvas.draw()
   
#создаю рамку в первой вкладке
frame_top1 = Frame(tab1, bg ='white')
frame_top1.grid()

#создаю метки(текст) в рамке frame_top
tab1_txt1 = Label(frame_top1, bg ='white', text="Расчет режима работы линии", font=('Times New Roman', 16))  
tab1_txt1.grid(row = 0, padx = 515, pady = 5)

#новая рамка для ввода данных:
tab1_frame_data = Frame(tab1, bg ='white')
tab1_frame_data.grid()
tab1_txt12 = Label(tab1_frame_data, text="Введите волновое сопротивление, Ом:", font=('Times New Roman', 13), bg ='white')
tab1_vvod12 = Entry(tab1_frame_data, width=6, font=('Times New Roman', 12), validate="key")
tab1_vvod12['validatecommand'] = (tab1_vvod12.register(validation), '%P')


tab1_txt12.grid(row = 1, column = 0)
tab1_vvod12.grid(row = 1, column = 1)

#создаем пустые виджеты
ghost1 = Label(tab1_frame_data, text="SALA", font=('Times New Roman', 11), bg ='white', fg='white')
ghost2 = Label(tab1_frame_data, text="SALA", font=('Times New Roman', 11), bg ='white', fg='white')

#ввод сопротивления нагрузки
tab1_text131 = Label(tab1_frame_data, text="Введите сопротивление нагрузки, Ом:", font=('Times New Roman', 13), bg ='white')
tab1_vvod131 = Entry(tab1_frame_data,width=6, font=('Times New Roman', 12), validate="key") 
tab1_vvod131['validatecommand'] = (tab1_vvod131.register(validation), '%P')
 
tab1_text132 = Label(tab1_frame_data, text="+j", font=('Times New Roman', 11), bg ='white')
tab1_vvod132 = Entry(tab1_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab1_vvod132['validatecommand'] = (tab1_vvod132.register(validation), '%P')


tab1_text133 = Label(tab1_frame_data, text="Введите длину волны, мм:", font=('Times New Roman', 13), bg ='white')
tab1_vvod133 = Entry(tab1_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab1_vvod133['validatecommand'] = (tab1_vvod133.register(validation), '%P')


ghost1.grid(row = 1, column = 2)
tab1_text131.grid(row = 1, column = 3)
tab1_vvod131.grid(row = 1, column = 4, pady = 10)
tab1_text132.grid(row = 1, column = 5)
tab1_vvod132.grid(row = 1, column = 6) 
ghost2.grid(row = 1, column = 7)

tab1_text133.grid(row = 1, column = 8)
tab1_vvod133.grid(row = 1, column = 9, pady = 10)

#рамка для вывода изображения
tab1_frame_canvas = Frame(tab1, bg = 'white')
tab1_frame_canvas.grid()

#кнопка для вывода изображения
button_tab1 = Button(tab1_frame_data, text="Построить", command = lambda: get_values_tab1())
button_tab1.grid(row = 2, column = 0, columnspan=10) 

#ВТОРАЯ ВКЛАДКА

tab2 = Frame(tab_control, bg ='white')  
tab_control.add(tab2, text='Расчет соединений')  
tab_control.grid(ipadx = 190 , ipady = 295)


def graph_tab2(Zv, Z, L):       
    Z_title = f'{round(Z.real, 2)} + ({round(Z.imag, 2)})j'
    ro = (Z/Zv - 1)/(Z/Zv + 1)
    z = linspace(0, 2*pi, 100)
    Up = exp(-1j*z)
    Uo = ro*exp(1j*z)
    U=Up+Uo
    abs_ro = abs(ro)
    phase_ro = atan(ro.imag/ro.real)
    phase = degrees(phase_ro%(2*pi))
    if phase > 180: 
        phase -= 360

    try:
        KSV = round((1+abs(ro))/(1-abs(ro)), 2)
    except ZeroDivisionError:
        KSV = 'бесконечность'
    Pot = round(abs((Uo*Uo/Up*Up))[0], 2)
    
    #Smith строим
    SmithAxes.update_scParams(axes_impedance = Zv)
    SmithAxes.update_scParams({"axes.radius": float(0.52)})
    tab2_figure = Figure(figsize=(6,6))
    tab2_figure.set_figheight(5.2)
    tab2_figure.set_figwidth(12.5)
    ax3 = tab2_figure.add_subplot(3, 2, 2)
    ax3.patch.set_visible(False)
    ax3.axis('off')
    text1 = f'     КСВ = {KSV} \n\n      Pот\n   ——— = {Pot}\n     Pпад \n\nρ = {round(abs_ro, 2)}×exp({round(phase, 2)}j)'
    ax3.text(0.37, 0.1, text1, font='Times New Roman', size = 14)
    ax = tab2_figure.add_subplot(1, 2, 1, projection='smith')
    ax.plot(Z, datatype='Z', markersize="10", color="#FF0000")
    ax.tick_params(axis='both', which='major', labelsize=14)
    canvas = FigureCanvasTkAgg(tab2_figure, tab2_frame_canvas)
        
    #строим графики тока и напряжения
    ax1 = tab2_figure.add_subplot(3, 2, 4)
    ax1.grid()
    ax1.plot(z*L/20*pi, abs(U), label= '|U|', color = '#00005c')
    ax1.set_ylabel('Напряжение в линии, В', size = 12)
    ax1.set_xlabel('Z, мм', size = 12)
    ax1.set_xlim(0, L)
    ax1.set_ylim(-0.0000000000001, 2.01)
    ax1.text(0.9*L, -0.7, 'НАГРУЗКА', font='Times New Roman', size = 13)
    ax1.tick_params(axis='both', which='major', labelsize=12)
    canvas = FigureCanvasTkAgg(tab2_figure, tab2_frame_canvas)
    canvas.get_tk_widget().grid(row=2)
    canvas.draw()
            

def get_values_tab2(x, tab2_entries):
    
    if x == "Через отрезок линии":
        Zv = tab2_vvod121.get() #волновое сопротивление
        R1 = tab2_vvod131.get() #сопр 1 нагрузки
        X1 = tab2_vvod132.get() #сопр 1 нагрузки
        L = tab2_vvod135.get() #длина волны 
        L0 = tab2_entries[tab2_vvod136].get() #длина отрезка
        Zv2 = tab2_entries[tab2_vvod122].get() #волновое сопротивление подключаемого отрезка
        
        if (R1 == '' and X1 == '') or Zv == '' or L == '' or L0 == '' or Zv2 == '':
            messagebox.showinfo('Ошибка ввода данных', 'Проверьте, все ли поля заполнены!')
            return False
        elif float(Zv) == 0:
            messagebox.showinfo('Ошибка ввода данных', 'Волновое сопротивление не должно быть нулевым!')
            return False
        elif float(L) <= 0:
            messagebox.showinfo('Ошибка ввода данных', 'Длина волны должна быть больше нуля!')
            return False
        else:
            Zv = float(Zv)
            L = float(L)
            L0 = float(L0)
            Zv2 = float(Zv2)
            if R1 == '':
                R1 = 0
                X1 = float(X1)
            elif X1 == '':
                X1 = 0
                R1 = float(R1)
            else:
                X1 = float(X1)
                R1 = float(R1)
            Z1 = R1 + 1j*X1
            Z = Zv2*((Z1+1j*Zv2*tan(2*pi*L0/L))/((Zv2+1j*Z1*tan(2*pi*L0/L))))
            graph_tab2(Zv, Z, L)
        
    else: 
        Zv = tab2_vvod121.get() #волновое сопротивление
        R1 = tab2_vvod131.get() #сопр 1 нагрузки
        X1 = tab2_vvod132.get() #сопр 1 нагрузки
        R2 = tab2_entries[tab2_vvod133].get() #сопр 2 нагрузки
        X2 = tab2_entries[tab2_vvod134].get() #сопр 2 нагрузки
        L = tab2_vvod135.get() #длина волны 
        if (R1 == '' and X1 == '') or (R2 == '' and X2 == '') or Zv == '' or L == '':
            messagebox.showinfo('Ошибка ввода данных', 'Проверьте, все ли поля заполнены!')
            return False
        elif float(Zv) == 0:
            messagebox.showinfo('Ошибка ввода данных', 'Волновое сопротивление не должно быть нулевым!')
            return False
        else:
            Zv = float(Zv)
            L = float(L)                
            if R1 == '':
                R1 = 0
                X1 = float(X1)
                Z1 = R1 + 1j*X1                  
            elif X1 == '':
                X1 = 0
                R1 = float(R1)
                Z1 = R1 + 1j*X1
            else:
                R1 = float(R1)
                X1 = float(X1)
                Z1 = R1 + 1j*X1
                
            if R2 == '':
                R2 = 0
                X2 = float(X2)
                Z2 = R2 + 1j*X2
            elif X2 == '':
                X2 = 0
                R2 = float(R2)   
                Z2 = R2 + 1j*X2
            else:
                R2 = float(R2)
                X2 = float(X2)
                Z2 = R2 + 1j*X2                  
                    
            if x == "Последовательное":          
                Z = Z1 + Z2
            elif x == "Параллельное":
                Z = Z1*Z2/(Z1+Z2)
            
            
            graph_tab2(Zv, Z, L)


   
#создаю рамку в первой вкладке
frame_top2 = Frame(tab2, bg ='white')
frame_top2.grid(row = 0)

#создаю метки(текст) в рамке frame_top
tab2_txt1 = Label(frame_top2, bg ='white', text="Расчет соединений", font=('Times New Roman', 16))  
tab2_txt1.grid(row = 0, padx = 560, pady = 7, columnspan = 40)
#новая рамка для ввода данных:
tab2_frame_data = Frame(tab2, bg ='white')
tab2_frame_data.grid(row = 1, padx = 10)

tab2_txt11 = Label(frame_top2, text="Тип соединения:", font=('Times New Roman', 13), bg ='white')
tab2_txt11.grid(row = 1, column = 20)

combo = Combobox(frame_top2, width = 19, state='readonly')
combo['values'] = ("Последовательное", "Параллельное", "Через отрезок линии")
combo.current(0)
combo.grid(row = 1, column = 21, pady = 7)

#ввод волновых сопротивлений
tab2_txt121 = Label(tab2_frame_data, text="Волновое сопротивление, Ом: линии", font=('Times New Roman', 13), bg ='white')
tab2_vvod121 = Entry(tab2_frame_data, width=7, font=('Times New Roman', 12), validate="key") 
tab2_vvod121['validatecommand'] = (tab2_vvod121.register(validation), '%P')

 
tab2_txt121.grid(row = 2, column = 0)
tab2_vvod121.grid(row = 2, column = 1)

tab2_txt122 = Label(tab2_frame_data, text="отрезка", font=('Times New Roman', 13), bg ='white')
tab2_vvod122 = Entry(tab2_frame_data, width=7, state='readonly', font=('Times New Roman', 12), validate="key")  
tab2_vvod122['validatecommand'] = (tab2_vvod122.register(validation), '%P')


tab2_txt122.grid(row = 2, column = 2)
tab2_vvod122.grid(row = 2, column = 3)

#ввод сопротивления нагрузки 1
tab2_text131 = Label(tab2_frame_data, text="            Введите сопротивление 1ой нагрузки, Ом:", font=('Times New Roman', 13), bg ='white')
tab2_vvod131 = Entry(tab2_frame_data,width=7, font=('Times New Roman', 12), validate="key")  
tab2_vvod131['validatecommand'] = (tab2_vvod131.register(validation), '%P')


tab2_text132 = Label(tab2_frame_data, text="+j", font=('Times New Roman', 13), bg ='white')
tab2_vvod132 = Entry(tab2_frame_data,width=7, font=('Times New Roman', 12), validate="key")
tab2_vvod132['validatecommand'] = (tab2_vvod132.register(validation), '%P')



tab2_text131.grid(row = 2, column = 5, pady = 3)
tab2_vvod131.grid(row = 2, column = 6)
tab2_text132.grid(row = 2, column = 7)
tab2_vvod132.grid(row = 2, column = 8)

#Ввод длины волны и длины отреезка
tab2_text135 = Label(tab2_frame_data, text="Введите длину, мм: волны", font=('Times New Roman', 13), bg ='white')
tab2_vvod135 = Entry(tab2_frame_data,width=7, font=('Times New Roman', 12), validate="key")
tab2_vvod135['validatecommand'] = (tab2_vvod135.register(validation), '%P')


tab2_text135.grid(row = 3, column = 0)
tab2_vvod135.grid(row = 3, column = 1)

tab2_text136 = Label(tab2_frame_data, text="отрезка", font=('Times New Roman', 13), bg ='white')
tab2_vvod136 = Entry(tab2_frame_data, width=7, state='readonly', font=('Times New Roman', 12), validate="key")  
tab2_vvod136['validatecommand'] = (tab2_vvod136.register(validation), '%P')


tab2_text136.grid(row = 3, column = 2)
tab2_vvod136.grid(row = 3, column = 3)

#ввод сопротивления нагрузки 2
tab2_text133 = Label(tab2_frame_data, text="            Введите сопротивление 2ой нагрузки, Ом:", font=('Times New Roman', 13), bg ='white')
tab2_text133.grid(row = 3, column = 5)
tab2_vvod133 = Entry(tab2_frame_data, width=7, state="normal", font=('Times New Roman', 12), validate="key")
tab2_vvod133['validatecommand'] = (tab2_vvod133.register(validation), '%P')


tab2_vvod133.grid(row = 3, column = 6)

tab2_text134 = Label(tab2_frame_data, text="+j", font=('Times New Roman', 13), bg ='white')
tab2_text134.grid(row = 3, column = 7)
tab2_vvod134 = Entry(tab2_frame_data, width=7, state="normal", font=('Times New Roman', 12), validate="key")
tab2_vvod134['validatecommand'] = (tab2_vvod134.register(validation), '%P')


tab2_vvod134.grid(row = 3, column = 8)


tab2_entries = {
    tab2_vvod136: tab2_vvod136,
    tab2_vvod122: tab2_vvod122,
    tab2_vvod133: tab2_vvod133,
    tab2_vvod134: tab2_vvod134,
}             
  

#рамка для вывода изображения
tab2_frame_canvas = Frame(tab2, bg ='white')
tab2_frame_canvas.grid(row = 2)#(fill='both', expand = 1, padx=20)

#кнопка для вывода изображения
button_tab2 = Button(tab2_frame_canvas, text="Построить", command = lambda: get_values_tab2(combo.get(), tab2_entries))
button_tab2.grid(row = 0, pady = 5)   

def callbackFunc(event):
    if combo.get() != 'Через отрезок линии':
        tab2_entries[tab2_vvod136] = Entry(tab2_frame_data, width=7, state="readonly", font=('Times New Roman', 12))  
        tab2_entries[tab2_vvod136].grid(row = 3, column = 3)
        
        tab2_entries[tab2_vvod122] = Entry(tab2_frame_data, width=7, state="readonly", font=('Times New Roman', 12))
        tab2_entries[tab2_vvod122].grid(row = 2, column = 3)
                
        tab2_entries[tab2_vvod133] = Entry(tab2_frame_data, width=7, state="normal", font=('Times New Roman', 12), validate="key")
        tab2_entries[tab2_vvod133]['validatecommand'] = (tab2_entries[tab2_vvod133].register(validation), '%P')
        tab2_entries[tab2_vvod133].grid(row = 3, column = 6)
        
        tab2_entries[tab2_vvod134] = Entry(tab2_frame_data, width=7, state="normal", font=('Times New Roman', 12), validate="key")
        tab2_entries[tab2_vvod134]['validatecommand'] = (tab2_entries[tab2_vvod134].register(validation), '%P')
        tab2_entries[tab2_vvod134].grid(row = 3, column = 8)
          
    else:

        tab2_entries[tab2_vvod136] = Entry(tab2_frame_data, width=7, state="normal", font=('Times New Roman', 12), validate="key")  
        tab2_entries[tab2_vvod136]['validatecommand'] = (tab2_entries[tab2_vvod136].register(validation), '%P')
        tab2_entries[tab2_vvod136].grid(row = 3, column = 3)
        
        tab2_entries[tab2_vvod122] = Entry(tab2_frame_data, width=7, state="normal", font=('Times New Roman', 12), validate="key")  
        tab2_entries[tab2_vvod122]['validatecommand'] = (tab2_entries[tab2_vvod122].register(validation), '%P')
        tab2_entries[tab2_vvod122].grid(row = 2, column = 3)
        
        tab2_entries[tab2_vvod133] = Entry(tab2_frame_data, width=7, state="readonly", font=('Times New Roman', 12))
        tab2_entries[tab2_vvod133].grid(row = 3, column = 6)
        
       
        tab2_entries[tab2_vvod134] = Entry(tab2_frame_data, width=7, state="readonly", font=('Times New Roman', 12))
        tab2_entries[tab2_vvod134].grid(row = 3, column = 8)
      
combo.bind("<<ComboboxSelected>>", lambda event: callbackFunc(event))

#ТРЕТЬЯ ВКЛАДКА
tab3 = Frame(tab_control, bg ='white')  
tab_control.add(tab3, text='Расчёт сопротивления нагрузки')  
tab_control.grid(ipadx = 190 , ipady = 295)

def get_values_tab3():
    Zv = tab3_vvod12.get()
    KSV = tab3_vvod131.get()
    LU = tab3_vvod132.get()
    L = tab3_vvod133.get()
    
    if Zv == '' or KSV == '' or LU == '' or L == '':
        messagebox.showinfo('Ошибка ввода данных', 'Проверьте, все ли поля заполнены!')
        return False
    elif float(Zv) == 0:
        messagebox.showinfo('Ошибка ввода данных', 'Волновое сопротивление не должно быть нулевым!')
        return False    
    elif float(L) <= 0:
        messagebox.showinfo('Ошибка ввода данных', 'Длина волны должна быть больше нуля!')
        return False
    else: 
        Zv = float(Zv)
        L = float(L)
        LU = float(LU)
        KSV = float(KSV)
        if KSV < 1: 
            messagebox.showinfo('Ошибка ввода данных', 'КСВ не может быть меньше единицы!')
            return False

        else:        
            graph_tab3(Zv, KSV, LU, L)

def graph_tab3(Zv, KSV, LU, L):
 
    #свдиг фазы вычисляем
    fi = 4*pi*LU/L - pi
    phase = degrees(fi%(2*pi))
    if phase > 180: 
        phase -= 360

    
    #находим модуль коэф. отражения из КСВ
    abs_ro = (KSV-1)/(KSV+1)
    
    #находим коэф. отражения через модуль и фазу
    ro = abs_ro*exp(-1j*fi)
    
    #выведенная мной формула для сопротивления нагрузки
    Zn = Zv*(-ro-1)/(ro-1)  
    z = linspace(0, 2*pi, 100)
    Up = exp(-1j*z)
    Uo = ro*exp(1j*z)
    U=Up+Uo  
    #напряжение при КЗ
    U2 = Up+Uo/ro
    Pot = round(abs((Uo*Uo/Up*Up))[0], 2)   
    #Smith строим
    SmithAxes.update_scParams(axes_impedance = Zv)
    SmithAxes.update_scParams({"axes.radius": float(0.53)})
    tab3_figure = Figure(figsize=(5,5))
    tab3_figure.set_figheight(5.6)
    tab3_figure.set_figwidth(12.9)
    ax = tab3_figure.add_subplot(1, 2, 1, projection='smith')
    ax.plot(Zn, datatype='Z', markersize="10", color="#FF0000")
    ax.tick_params(axis='both', which='major', labelsize=12)
    canvas = FigureCanvasTkAgg(tab3_figure, tab3_frame_canvas)

    #строим графики тока и напряжения
    ax1 = tab3_figure.add_subplot(3, 2, 4)
    ax1.grid()
    ax3 = tab3_figure.add_subplot(3, 2, 2)
    ax3.patch.set_visible(False)
    ax3.axis('off')
    text1 = f'        Pот\n     ——— = {Pot}\n       Pпад \n\nZн = {round(Zn.real, 2)} + {round(Zn.imag, 2)}j Ом \n\nρ = {round(abs_ro, 2)}×exp({round(phase, 2)}j)'
    ax3.text(0.33, 0.1, text1, font='Times New Roman', size = 14)
    ax1.plot(z*L/20*pi, abs(U), label= '|U|', color = '#00005c')
    ax1.plot(z*L/20*pi, abs(U2), '--',label = '|Uкз|', color='#660e00')
    ax1.set_ylabel('Напряжение в линии, В', size = 12)
    ax1.set_xlabel('Z, мм', size = 12)
    ax1.set_yticks([0.0, 0.5, 1.0, 1.5, 2.0])
    ax1.tick_params(axis='both', which='major', labelsize=12)
    ax1.set_xlim(0, L)
    ax1.set_ylim(-0.00000001, 2.01)
    ax1.text(0.9*L, -0.7, 'НАГРУЗКА', font='Times New Roman', size = 13)
    ax1.legend(prop={"size":12, 'family':'Times New Roman'})
    canvas = FigureCanvasTkAgg(tab3_figure, tab3_frame_canvas)
    canvas.get_tk_widget().grid(row=5)
    canvas.draw()

#создаю рамку в первой вкладке
frame_top3 = Frame(tab3, bg ='white')
frame_top3.grid()

#создаю метки(текст) в рамке frame_top
tab3_txt1 = Label(frame_top3, bg ='white', text="Расчет сопротивления нагрузки по данным измерений", font=('Times New Roman', 16))  
tab3_txt1.grid(row = 0, padx = 405, pady = 5)

#новая рамка для ввода данных:
tab3_frame_data = Frame(tab3, bg ='white')
tab3_frame_data.grid()
tab3_txt12 = Label(tab3_frame_data, text="Введите волновое сопротивление, Ом:", font=('Times New Roman', 13), bg ='white')
tab3_vvod12 = Entry(tab3_frame_data, width=6, font=('Times New Roman', 12), validate="key")
tab3_vvod12['validatecommand'] = (tab3_vvod12.register(validation), '%P')
  
tab3_txt12.grid(row = 1, column = 0)
tab3_vvod12.grid(row = 1, column = 1)

#создаем пустые виджеты
tab3_ghost1 = Label(tab3_frame_data, text="SA", font=('Times New Roman', 12), bg ='white', fg='white')
tab3_ghost2 = Label(tab3_frame_data, text="SA", font=('Times New Roman', 12), bg ='white', fg='white')

#ввод сопротивления нагрузки
tab3_text131 = Label(tab3_frame_data, text="Введите КСВ:", font=('Times New Roman', 13), bg ='white')
tab3_vvod131 = Entry(tab3_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab3_vvod131['validatecommand'] = (tab3_vvod131.register(validation), '%P') 

tab3_ghost3 = Label(tab3_frame_data, text="SA", font=('Times New Roman', 12), bg ='white', fg='white')

tab3_text132 = Label(tab3_frame_data, text="Введите расстояние от min до min при КЗ, мм:", font=('Times New Roman', 13), bg ='white')
tab3_vvod132 = Entry(tab3_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab3_vvod132['validatecommand'] = (tab3_vvod132.register(validation), '%P')

tab3_text133 = Label(tab3_frame_data, text="Введите длину волны, мм:", font=('Times New Roman', 13), bg ='white')
tab3_vvod133 = Entry(tab3_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab3_vvod133['validatecommand'] = (tab3_vvod133.register(validation), '%P')

tab3_ghost1.grid(row = 1, column = 2)
tab3_text131.grid(row = 1, column = 3)
tab3_vvod131.grid(row = 1, column = 4, pady = 10)
tab3_ghost3.grid(row = 1, column = 5)
tab3_text132.grid(row = 1, column = 6)
tab3_vvod132.grid(row = 1, column = 7) 
tab3_ghost2.grid(row = 1, column = 8)

tab3_text133.grid(row = 1, column = 9)
tab3_vvod133.grid(row = 1, column = 10, pady = 15)

#рамка для вывода изображения
tab3_frame_canvas = Frame(tab3, bg = 'white')
tab3_frame_canvas.grid()

#кнопка для вывода изображения
button_tab3 = Button(tab3_frame_data, text="Построить", command = lambda: get_values_tab3())
button_tab3.grid(row = 2, column = 0, columnspan=11) 





#ЧЕТВЕРТАЯ ВКЛАДКА
tab4 = Frame(tab_control, bg ='white')  
tab_control.add(tab4, text='Согласование четвертьволновым трансформатором')  
tab_control.grid(ipadx = 170 , ipady = 295)


def get_values_tab4():
    R = tab4_vvod131.get()
    X = tab4_vvod132.get()
    Zv = tab4_vvod12.get()
    L = tab4_vvod133.get()
   
    if Zv == '' or (R == '' and X == '') or L == '':
        messagebox.showinfo('Ошибка ввода данных', 'Проверьте, все ли поля заполнены!')
        return False
    elif float(Zv) == 0:
        messagebox.showinfo('Ошибка ввода данных', 'Волновое сопротивление не должно быть нулевым!')
        return False
    elif float(L) <= 0:
        messagebox.showinfo('Ошибка ввода данных', 'Длина волны должна быть больше нуля!')
        return False
    else: 
        Zv = float(Zv)
        L = float(L)
        if R == '' or float(R) == 0:
            messagebox.showinfo('Информация', 'Согласование невозможно! \nЛиния работает в режиме КБВ = 0.')
            return False
        elif X == '' or float(X) == 0:
            messagebox.showinfo('Информация', 'В согласовании нет необходимости!')
            return False
        else:
            R = float(R)
            X = float(X)
                 
    graph_tab4(R, X, Zv, L)

def graph_tab4(R, X, Zv, L):
    Z = R+1j*X
    a = (R-Zv)*(R+Zv)+X**2
    b = X*(R+Zv)-X*R-Zv
  
    if (a > 0) & (b > 0): 
        c = atan((2*Zv*X)/(R**2+X**2-Zv**2))
    elif (a < 0):
        c = atan((2*Zv*X)/(R**2+X**2-Zv**2)) + pi
    elif (a > 0) & (b < 0): 
        c = atan((2*Zv*X)/(R**2+X**2-Zv**2)) + 2*pi
    
    Lu = round((c*L/(4*pi)), 2)
    Ltr = round((L/4), 2)
    
    KBW1 = sqrt((R+Zv)**2+X**2)
    KBW2 = sqrt((R-Zv)**2+X**2)
    KBW = (KBW1-KBW2)/(KBW1+KBW2)
    Ztr = round(Zv/sqrt(KBW), 2)
    
    #Smith строим
    SmithAxes.update_scParams(axes_impedance = Zv)
    SmithAxes.update_scParams({"axes.radius": float(0.54)})
    tab4_figure = Figure(figsize=(5,5))
    tab4_figure.set_figheight(5.6)
    tab4_figure.set_figwidth(12.8)
    ax = tab4_figure.add_subplot(1, 2, 1, projection='smith')
    Z = R+1j*X
    canvas = FigureCanvasTkAgg(tab4_figure, tab4_frame_canvas)
   
    #выводим текст на пустой график
    ax.plot(Z, datatype='Z', markersize="10", color="#FF0000")
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax1 = tab4_figure.add_subplot(2, 2, 4)
    ax1.patch.set_visible(False)
    ax1.axis('off')
    text1 = f'Расстояние от нагрузки до места включения трансформатора: \nL1 = {Lu} мм \n\nДлина трансформирующего отрезка: \nL2 = {Ltr} мм \n\nВолновое сопротивление трансформатора: \nZтр = {Ztr} Ом'
    ax1.text(0.05, 0.15, text1, font='Times New Roman', size = 14)
    
    
    
    ax2 = tab4_figure.add_subplot(2, 2, 2)
    ax2.grid(False)
    ax2.patch.set_visible(False)
    ax2.axis('off')
    image1 = imread(resource_path('image1.jpg'))
    ax2.imshow(image1)
    
    
    
    canvas = FigureCanvasTkAgg(tab4_figure, tab4_frame_canvas)
    canvas.get_tk_widget().grid(row=5)
    canvas.draw()
   
#создаю рамку в четвертой вкладке
frame_top4 = Frame(tab4, bg ='white')
frame_top4.grid()

#создаю метки(текст) в рамке frame_top
tab4_txt1 = Label(frame_top4, bg ='white', text="Согласование четвертьволновым трансформатором", font=('Times New Roman', 16))  
tab4_txt1.grid(row = 0, padx = 415, pady = 5)

#новая рамка для ввода данных:
tab4_frame_data = Frame(tab4, bg ='white')
tab4_frame_data.grid()
tab4_txt12 = Label(tab4_frame_data, text="Введите волновое сопротивление, Ом:", font=('Times New Roman', 13), bg ='white')
tab4_vvod12 = Entry(tab4_frame_data, width=6, font=('Times New Roman', 12), validate="key")
tab4_vvod12['validatecommand'] = (tab4_vvod12.register(validation), '%P')
  
tab4_txt12.grid(row = 1, column = 0)
tab4_vvod12.grid(row = 1, column = 1)

#создаем пустые виджеты
tab4_ghost1 = Label(tab4_frame_data, text="SALA", font=('Times New Roman', 11), bg ='white', fg='white')
tab4_ghost2 = Label(tab4_frame_data, text="SALA", font=('Times New Roman', 11), bg ='white', fg='white')

#ввод сопротивления нагрузки
tab4_text131 = Label(tab4_frame_data, text="Введите сопротивление нагрузки, Ом:", font=('Times New Roman', 13), bg ='white')
tab4_vvod131 = Entry(tab4_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab4_vvod131['validatecommand'] = (tab4_vvod131.register(validation), '%P')
  
tab4_text132 = Label(tab4_frame_data, text="+j", font=('Times New Roman', 11), bg ='white')
tab4_vvod132 = Entry(tab4_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab4_vvod132['validatecommand'] = (tab4_vvod132.register(validation), '%P')

tab4_text133 = Label(tab4_frame_data, text="Введите длину волны, мм:", font=('Times New Roman', 13), bg ='white')
tab4_vvod133 = Entry(tab4_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab4_vvod133['validatecommand'] = (tab4_vvod133.register(validation), '%P')

tab4_ghost1.grid(row = 1, column = 2)
tab4_text131.grid(row = 1, column = 3)
tab4_vvod131.grid(row = 1, column = 4, pady = 10)
tab4_text132.grid(row = 1, column = 5)
tab4_vvod132.grid(row = 1, column = 6) 
tab4_ghost2.grid(row = 1, column = 7)

tab4_text133.grid(row = 1, column = 8)
tab4_vvod133.grid(row = 1, column = 9, pady = 10)

#рамка для вывода изображения
tab4_frame_canvas = Frame(tab4, bg = 'white')
tab4_frame_canvas.grid()

#кнопка для вывода изображения
button_tab4 = Button(tab4_frame_data, text="Построить", command = lambda: get_values_tab4())
button_tab4.grid(row = 2, column = 0, columnspan=10) 




#ПЯТАЯ ВКЛАДКА
tab5 = Frame(tab_control, bg ='white')  
tab_control.add(tab5, text='Согласование короткозамкнутым шлейфом')  
tab_control.grid(ipadx = 190 , ipady = 295)


def get_values_tab5():
    Zv1 = tab5_vvod12.get()
    Zv2 = tab5_vvod131.get()
    R = tab5_vvod132.get()
    X = tab5_vvod133.get()
    L = tab5_vvod134.get()
   
    if Zv1 == '' or Zv2 == '' or (R == '' and X == '') or L == '':
        messagebox.showinfo('Ошибка ввода данных', 'Проверьте, все ли поля заполнены!')
        return False
    elif float(Zv1) == 0 or float(Zv2) == 0:
        messagebox.showinfo('Ошибка ввода данных', 'Волновое сопротивление не должно быть нулевым!')
        return False
    elif float(L) <= 0:
        messagebox.showinfo('Ошибка ввода данных', 'Длина волны должна быть больше нуля!')
        return False
    else: 
        Zv1 = float(Zv1)
        Zv2 = float(Zv2)
        L = float(L)
        if R == '' or float(R) == 0:
            messagebox.showinfo('Информация', 'Согласование невозможно! \nЛиния работает в режиме КБВ = 0.')
            return False
        elif X == '' or float(X) == 0:
            messagebox.showinfo('Информация', 'В согласовании нет необходимости!')
            return False
        else:
            R = float(R)
            X = float(X)
                 
        graph_tab5(R, X, Zv1, Zv2, L)

def graph_tab5(R, X, Zv1, Zv2, L):
    Z = R+1j*X

    a = (R-Zv1)*(R+Zv1)+X**2
    b = X*(R+Zv1)-X*R-Zv1

    if (a > 0) & (b > 0): 
        c = atan((2*Zv1*X)/(R**2+X**2-Zv1**2))
    elif (a < 0):
        c = atan((2*Zv1*X)/(R**2+X**2-Zv1**2)) + pi
    elif (a > 0) & (b < 0): 
        c = atan((2*Zv1*X)/(R**2+X**2-Zv1**2)) + 2*pi
        
    Lu = round((c*L/(4*pi)), 2)
    
    KBW1 = sqrt((R+Zv1)**2+X**2)
    KBW2 = sqrt((R-Zv1)**2+X**2)
    KBW = (KBW1-KBW2)/(KBW1+KBW2)
    
    beta = 2*pi/L
    Lsh = round(((atan((Zv1*sqrt(KBW))/(Zv2*(1-KBW))))/beta), 2)
    Lcon = round((((atan(1/(sqrt(KBW))))/beta) + Lu), 2)
    
    #Smith строим
    SmithAxes.update_scParams(axes_impedance = Zv1)
    SmithAxes.update_scParams({"axes.radius": float(0.54)})
    tab5_figure = Figure(figsize=(5,5))
    tab5_figure.set_figheight(5.6)
    tab5_figure.set_figwidth(12.8)
    ax = tab5_figure.add_subplot(1, 2, 1, projection='smith')
    canvas = FigureCanvasTkAgg(tab5_figure, tab5_frame_canvas)
      
    #выводим текст на пустой график
    ax.plot(Z, datatype='Z', markersize="10", color="#FF0000")
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax1 = tab5_figure.add_subplot(2, 2, 4)
    ax1.patch.set_visible(False)
    ax1.axis('off')
    text1 = f'Расстояние от нагрузки до места включения шлейфа: \nL1 = {Lcon} мм \n\nДлина шлейфа: \nL2 = {Lsh} мм'
    ax1.text(0.05, 0.5, text1, font='Times New Roman', size = 14)
            
    ax2 = tab5_figure.add_subplot(2, 2, 2)
    ax2.grid(False)
    ax2.patch.set_visible(False)
    ax2.axis('off')
    image2 = imread(resource_path('image2.jpg'))
    ax2.imshow(image2)
    
    canvas = FigureCanvasTkAgg(tab5_figure, tab5_frame_canvas)
    canvas.get_tk_widget().grid(row=5)
    canvas.draw()

#создаю рамку в первой вкладке
frame_top5 = Frame(tab5, bg ='white')
frame_top5.grid()


#создаю метки(текст) в рамке frame_top
tab5_txt1 = Label(frame_top5, bg ='white', text="Согласование короткозамкнутым шлейфом", font=('Times New Roman', 16))  
tab5_txt1.grid(row = 0, padx = 452, pady = 5)

#новая рамка для ввода данных:
tab5_frame_data = Frame(tab5, bg ='white')
tab5_frame_data.grid()
tab5_txt12 = Label(tab5_frame_data, text="Волновое сопротивление линии, Ом:", font=('Times New Roman', 13), bg ='white')
tab5_vvod12 = Entry(tab5_frame_data, width=6, font=('Times New Roman', 12), validate="key")
tab5_vvod12['validatecommand'] = (tab5_vvod12.register(validation), '%P')
 
tab5_txt12.grid(row = 1, column = 0)
tab5_vvod12.grid(row = 1, column = 1)

#создаем пустые виджеты
tab5_ghost1 = Label(tab5_frame_data, text="SA", font=('Times New Roman', 12), bg ='white', fg='white')
tab5_ghost2 = Label(tab5_frame_data, text="SA", font=('Times New Roman', 12), bg ='white', fg='white')

#ввод сопротивления нагрузки
tab5_text131 = Label(tab5_frame_data, text="Волновое сопротивление шлейфа, Ом:", font=('Times New Roman', 13), bg ='white')
tab5_vvod131 = Entry(tab5_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab5_vvod131['validatecommand'] = (tab5_vvod131.register(validation), '%P') 

tab5_ghost3 = Label(tab5_frame_data, text="SA", font=('Times New Roman', 12), bg ='white', fg='white')

tab5_text132 = Label(tab5_frame_data, text="Сопротивление нагрузки, Ом:", font=('Times New Roman', 13), bg ='white')
tab5_vvod132 = Entry(tab5_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab5_vvod132['validatecommand'] = (tab5_vvod132.register(validation), '%P')

tab5_text133 = Label(tab5_frame_data, text="+j", font=('Times New Roman', 11), bg ='white')
tab5_vvod133 = Entry(tab5_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab5_vvod133['validatecommand'] = (tab5_vvod133.register(validation), '%P')

tab5_text134 = Label(tab5_frame_data, text="Длина волны, мм:", font=('Times New Roman', 13), bg ='white')
tab5_vvod134 = Entry(tab5_frame_data,width=6, font=('Times New Roman', 12), validate="key")
tab5_vvod134['validatecommand'] = (tab5_vvod134.register(validation), '%P')

tab5_ghost1.grid(row = 1, column = 2)
tab5_text131.grid(row = 1, column = 3)
tab5_vvod131.grid(row = 1, column = 4, pady = 10)
tab5_ghost3.grid(row = 1, column = 5)
tab5_text132.grid(row = 1, column = 6)
tab5_vvod132.grid(row = 1, column = 7) 
tab5_text133.grid(row = 1, column = 8)
tab5_vvod133.grid(row = 1, column = 9, pady = 15)
tab5_ghost2.grid(row = 1, column = 10)
tab5_text134.grid(row = 1, column = 11)
tab5_vvod134.grid(row = 1, column = 12)

#рамка для вывода изображения
tab5_frame_canvas = Frame(tab5, bg = 'white')
tab5_frame_canvas.grid()

#кнопка для вывода изображения
button_tab5 = Button(tab5_frame_data, text="Построить", command = lambda: get_values_tab5())
button_tab5.grid(row = 2, column = 0, columnspan=14) 


root.mainloop()

