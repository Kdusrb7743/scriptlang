from calendar import c
from msilib.schema import ComboBox
from tarfile import PAX_FIELDS
from tkinter import *
from tkinter import font
from tkinter import ttk
from numpy import pad
from xml.etree import ElementTree

import requests


#from http.client import HTTPSConnection


window = Tk()                      # 주제 : 편의시설: 카페, 편의점, 약국
window.geometry("550x700-350+100") # 앞에는 크기 , 뒤에는 좌표


CityStr = StringVar()

Url = None
conn = None
SIGUN_CD = None
data_code = None
#server = "openapi.gg.go.kr"      # https://data.gg.go.kr/  https://openapi.gg.go.kr

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
    
    # 1. 타이틀
    MainText = Label(frameTitle, font = fontTitle, text='편의시설 - 카페 편의점 약국')
    MainText.pack(anchor="center",fill="both")

    # 2.L 시군구 
    data = ["수원시", "성남시", "용인시", "안양시", "안산시", "과천시", "광명시", "광주시", "군포시", "부천시", "시흥시", "김포시", "안성시"\
        , "오산시", "의왕시", "이천시", "평택시", "하남시", "화성시", "여주시", "고양시", "구리시", "남양주시", "동두천시", "양주시", "의정부시"
        , "파주시", "포천시", "양평군", "연천군", "포천군"]

    cityCombo = ttk.Combobox(frameCombo, values=data, font=fontNormal, textvariable=CityStr, width=20)
    cityCombo.set("경기도 시군구")
    cityCombo.bind('<<ComboboxSelected>>', getstr)             #콤보박스 선택시 이벤트 해주는 바인드 부분
    cityCombo.pack(side='left', padx=20)
    
    # 2.R 이메일
    emailbutton = Button(frameCombo, text="이메일", padx=15, pady=15, command=email)
    emailbutton.pack(side='right', padx=20)
    
    # 3. 카페, 편의점, 약국 버튼
    #CaftUrl = "https://openapi.gg.go.kr/Resrestrtcvnstr?KEY=9dff4350fafe400db05270b8161c46d3"      #카페
    #ConvenienceUrl = "https://openapi.gg.go.kr/Genrestrtcate?KEY=9dff4350fafe400db05270b8161c46d3" #편의점
    #PharmacyUrl = "https://openapi.gg.go.kr/Parmacy?KEY=9dff4350fafe400db05270b8161c46d3"          #약국
    
    # 사업자명 BIZPLC_NM 에 해당하는걸 출력할것임----------------------------------- 하는 중

    Cafebutton = Button(frameselect, text="카페", padx=30, pady=20, command=CaftUrl)     # 카페 버튼 누르면 밑에 리스트 박스에 정보 송출
    Cafebutton.grid(row=0, column=0, padx=65)
    Conveniencebutton = Button(frameselect, text="편의점", padx=30, pady=20, command=ConvenienceUrl)
    Conveniencebutton.grid(row=0, column=1)
    Pharmacybutton = Button(frameselect, text="약국", padx=30, pady=20, command=PharmacyUrl)
    Pharmacybutton.grid(row=0, column=2, padx=65)


    # 4. 리스트 및 상세정보
    global left_listbox, right_listbox                #좌측 리스트박스
    LBscrollbar = Scrollbar(framelist)
    left_listbox = Listbox(framelist, font=fontNormal, width = 20, yscrollcommand=LBscrollbar.set)
    left_listbox.pack(side='left')
    LBscrollbar.pack(side='left', fill='y')
    LBscrollbar.config(command=left_listbox.yview)

    # Center 검색
    searchebutton = Button(framelist, text="검색", padx=10, pady=10, command=Print)
    searchebutton.pack(side='left')
    
    RBscrollbar = Scrollbar(framelist)  #우측 리스트박스
    right_listbox = Listbox(framelist,font=fontNormal, width = 20, yscrollcommand=RBscrollbar.set)
    right_listbox.pack(side='right')
    RBscrollbar.pack(side='right', fill='y')
    RBscrollbar.config(command=right_listbox.yview)


    # 5. 지도 및 그래프 부분
    # 추가

    # 이후 이메일 처리, 리스트 스크롤 처리 xml api들여오기, 지도, 그래프

def Print():     #검색버튼 누르면 리스트박스에 selection된 것의 상세정보 우측에 표시
    global right_listbox
    from bs4 import BeautifulSoup

    selection = left_listbox.curselection()
    if (len(selection) > 0):

        conn = openAPIserver(Complete_Url)
        tree = ElementTree.fromstring(conn)

        right_listbox.delete(0, left_listbox.size())      # 입력된거 리셋
        i = 1
        value = left_listbox.get(selection[0])

        print(value)
        itemele = tree.iter("row")
        for item in itemele:
            name = item.find("BIZPLC_NM")
            operation = item.find("BSN_STATE_NM") #REFINE_LOTNO_ADDR
            road_name_add = item.find("REFINE_LOTNO_ADDR")                  #------------ 막 로직 완성--------

            if (name.text == value):
                right_listbox.insert(i - 1, "지점명 :" + name.text)
                right_listbox.insert(i, "운영여부 :" + operation.text)
                right_listbox.insert(i + 1, "도로명주소 :" + road_name_add.text)
                print(1)
                break
        
        # itemElements = tree.iter("row") # item 엘리먼트 리스트 추출
        # for item in itemElements:
        #     BIZPLC_NM = item.find("BIZPLC_NM")
        #     if len(BIZPLC_NM.text) > 0:
        #         left_listbox.insert(i - 1, BIZPLC_NM.text)

def email():     # 이메일 보내는 부분
    pass

def CaftUrl():
    global Url
    Url = "Genrestrtcate?KEY=9dff4350fafe400db05270b8161c46d3"
    listbox_print()

def ConvenienceUrl():
    global Url
    Url = "Resrestrtcvnstr?KEY=9dff4350fafe400db05270b8161c46d3"
    listbox_print()
    
def PharmacyUrl():
    global Url
    Url = "Parmacy?KEY=9dff4350fafe400db05270b8161c46d3"
    listbox_print()

def listbox_print():
    global Url
    global SIGUN_CD
    global Complete_Url
    global conn

    Complete_Url = 0
    Complete_Url = "https://openapi.gg.go.kr/" + Url + "&Type=xml" + "&pIndex=1" + "&pSize=100" + SIGUN_CD
    #Complete_Url = "https://openapi.gg.go.kr/Resrestrtcvnstr?KEY=9dff4350fafe400db05270b8161c46d3&Type=xml&pIndex=1&pSize=50&SIGUN_CD=41270"
    #print(Url)
    #print(SIGUN_CD)            # 3개 디버깅용
    #print(Complete_Url)

    conn = openAPIserver(Complete_Url)
    extractData(conn)

    # req = conn.getresponse()
    # print(req.status)
    # if int(req.status) == 200:                 # 417오류 해결필요 -> 안씀
    #     print("data downloading complete!")
    # else :
    #     print ("OpenAPI request has been failed!! please retry")
    #     return None

def openAPIserver(Complete_Url):
    return requests.get(Complete_Url).text.encode('utf-8')

def extractData(strXml): #strXml은 OpenAPI 검색 결과 XML 문자열

    tree = ElementTree.fromstring(strXml)
    #print (parseString(strXml.decode('utf-8')).toprettyxml()) #내용 확인용     디버깅

    global left_listbox
    left_listbox.delete(0,left_listbox.size())      # 입력된거 리셋
    i = 1
    itemElements = tree.iter("row") # item 엘리먼트 리스트 추출
    for item in itemElements:
        BIZPLC_NM = item.find("BIZPLC_NM")
        if len(BIZPLC_NM.text) > 0:
            left_listbox.insert(i - 1, BIZPLC_NM.text)    #----리스트박스 출력완료 -> 리스트 클릭하면 오른쪽 상세알려줌 할 차례

# def connectOpenAPIServer():
#     global conn, server
#     conn = HTTPSConnection(server)
#     conn.set_debuglevel(1)

def getstr(event):
    global SIGUN_CD, data_code
    data_code = { "가평군" : 41820, "고양시":  41280, "과천시": 41290, "광명시":  41210, "광주시" : 41610, "구리시" : 41310, "군포시" : 41410,\
        "김포시" : 41570, "남양주시": 41360, "동두천시" :  41250, "부천시": 41190, "성남시" : 41130, "수원시" :  41110, "시흥시" : 41390,\
        "안산시" : 41270, "안성시" :  41550, "안양시" : 41170, "양주시" : 41630, "양평군" : 41830, "여주시" :  41670, "연천군" :  41800,\
        "오산시" : 41370, "용인시" :  41460, "의왕시" :  41430, "의정부시" :  41150, "이천시"    :  41500, "파주시" :  41480, "평택시" : 41220,\
        "포천시" : 41650, "하남시" :  41450, "화성시" :  41590}
    City = data_code[CityStr.get()]
    SIGUN_CD = '&SIGUN_CD='+ str(City)      # 시군구 요청인자 &SIGUN_NM=땡땡시
    print(SIGUN_CD)

InitScreen() # 화면 전체 구성


window.mainloop()
