from calendar import c
from msilib.schema import ComboBox
from tarfile import PAX_FIELDS
from tkinter import *
from tkinter import font
from tkinter import ttk

from numpy import pad


window = Tk()
window.geometry("400x600-350+100") # 앞에는 크기 , 뒤에는 좌표

def InitScreen():
    fontTitle = font.Font(window, size=18, weight='bold',family='돋움체')
    fontNormal = font.Font(window, size=15, weight='bold')

    frameTitle = Frame(window, padx=10, pady=10)
    frameTitle.pack(side="top", fill="x")
    frameCombo = Frame(window, pady=10)
    frameCombo.pack(side="top", fill="x")
    frameselect = Frame(window, pady=10)
    frameselect.pack(side="top", fill="x")
    framelist = Frame(window)
    framelist.pack(side="top", fill="x")
    framemap = Frame(window)
    framemap.pack(side="top", fill="x")
    
    # 타이틀
    MainText = Label(frameTitle, font = fontTitle, text='편의시설 - 카페 편의점 약국')
    MainText.pack(anchor="center",fill="both")

    data = ["임시 저장", "1", "2"]
    cityCombo = ttk.Combobox(frameCombo, values=data, font=fontNormal)
    cityCombo.set("시군구")
    cityCombo.pack(side='left', padx=30)

    emailbutton = Button(frameCombo, text="이메일", padx=10, pady=10)
    emailbutton.pack(side='right', padx=20)
    
    Cafebutton = Button(frameselect, text="카페", padx=10, pady=10)
    Cafebutton.grid(row=0, column=0, padx=60)
    Conveniencebutton = Button(frameselect, text="편의점", padx=10, pady=10)
    Conveniencebutton.grid(row=0, column=1)
    Pharmacybutton = Button(frameselect, text="약국", padx=10, pady=10)
    Pharmacybutton.grid(row=0, column=2, padx=60)


    # 시(군) 선택 및 검색창
    #global Searchcity
    #controlbar = Searchcity(frameCombo)
    

# 주제 : 편의시설: 카페, 편의점, 약국

InitScreen() # 화면 전체 구성

window.mainloop()