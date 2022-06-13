from tkinter import *
from tkinter import font
from tkinter import ttk
from xml.etree import ElementTree

import requests
import folium
import webbrowser

window = Tk()                      # 주제 : 편의시설: 카페, 편의점, 약국
window.geometry("800x700-350+100") # 앞에는 크기 , 뒤에는 좌표

CityStr = StringVar()

Url = None
conn = None
SIGUN_CD = None
data_code = None
Latitude = None
longitude = None
#server = "openapi.gg.go.kr"      # https://data.gg.go.kr/  https://openapi.gg.go.kr

breakshop_cnt = conveniencestore_cnt = pharmacy_cnt = 0

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
    MainText = Label(frameTitle, font = fontTitle, text='편의시설 - 휴게음식점 편의점 약국')
    MainText.pack(anchor="center",fill="both")

    # 2.L 시군구 
    data = ["수원시", "성남시", "용인시", "안양시", "안산시", "과천시", "광명시", "광주시", "군포시", "부천시", "시흥시", "김포시", "안성시"\
        , "오산시", "의왕시", "이천시", "평택시", "하남시", "화성시", "여주시", "고양시", "구리시", "남양주시", "동두천시", "양주시", "의정부시"
        , "파주시", "포천시", "양평군", "연천군", "포천군", "가평군"]

    cityCombo = ttk.Combobox(frameCombo, values=data, font=fontNormal, textvariable=CityStr, width=20)
    cityCombo.set("경기도 시군구")
    cityCombo.bind('<<ComboboxSelected>>', getstr)             #콤보박스 선택시 이벤트 해주는 바인드 부분
    cityCombo.pack(side='left', padx=20)
    
    # 2.R 이메일
    emailimage = PhotoImage(file="image\\email.png")
    emailbutton = Button(frameCombo, text="이메일", image=emailimage,  command=email_send)
    emailbutton.image = emailimage
    emailbutton.pack(side='right', padx=20)
    
    #CaftUrl = "https://openapi.gg.go.kr/Resrestrtcvnstr?KEY=9dff4350fafe400db05270b8161c46d3"      #카페
    #ConvenienceUrl = "https://openapi.gg.go.kr/Genrestrtcate?KEY=9dff4350fafe400db05270b8161c46d3" #편의점
    #PharmacyUrl = "https://openapi.gg.go.kr/Parmacy?KEY=9dff4350fafe400db05270b8161c46d3"          #약국

    # 3. 카페, 편의점, 약국 버튼
    restingimage = PhotoImage(file="image\\Restinglogo.png")
    Restingbutton = Button(frameselect, text="휴게음식점", image=restingimage ,padx=20, pady=20, command=RestingUrl)     # 카페 버튼 누르면 밑에 리스트 박스에 정보 송출
    Restingbutton.image = restingimage
    Restingbutton.grid(row=0, column=0, padx=55)

    Convenienceimage = PhotoImage(file="image\\Convenience.png")
    Conveniencebutton = Button(frameselect, text="편의점", image=Convenienceimage, padx=30, pady=20, command=ConvenienceUrl)
    Conveniencebutton.image = Convenienceimage
    Conveniencebutton.grid(row=0, column=1)

    Pharmacyimage = PhotoImage(file="image\\Pharmacy.png")
    Pharmacybutton = Button(frameselect, text="약국",image=Pharmacyimage, padx=30, pady=20, command=PharmacyUrl)
    Pharmacybutton.image = Pharmacyimage
    Pharmacybutton.grid(row=0, column=2, padx=80)


    # 4. 리스트 및 상세정보
    global left_listbox, right_listbox 
    #좌측 리스트박스----- page넘기기 한페이지 = 1000개 데이터
    LBscrollbar = Scrollbar(framelist)
    left_listbox = Listbox(framelist, font=fontNormal, width = 20, yscrollcommand=LBscrollbar.set)
    left_listbox.pack(side='left')
    LBscrollbar.pack(side='left', fill='y')
    LBscrollbar.config(command=left_listbox.yview)

    # Center 검색
    searchebutton = Button(framelist, text="검색", padx=10, pady=10, command=Search)
    searchebutton.pack(side='left')
    #우측 리스트박스
    RBscrollbar = Scrollbar(framelist)  
    right_listbox = Listbox(framelist,font=fontNormal, width = 43, yscrollcommand=RBscrollbar.set)
    right_listbox.pack(side='right')
    RBscrollbar.pack(side='right', fill='y')
    RBscrollbar.config(command=right_listbox.yview)

    # 5. 지도 및 그래프 부분
    mapimage = PhotoImage(file="image\\maplogo.png")
    Map_button = Button(framemap, image=mapimage, command=Map_new_tap)
    Map_button.image = mapimage
    Map_button.pack(side='left')

    # 그래프 로직: 시군구에 휴게음식점 or 편의점 or 약국을 선택하면 나오는 개수를 data에 저장
    global Graph
    Graph = Canvas(framemap, width=600, height=200, bg='white')
    Graph.pack(side='right')

def drawGraph(canvas, data, canvasWidth, canvasHeight):     # 그래프 함수는 편의시설 버튼 클릭시 나오는 시설의 개수를 각 시설그래프에추가
    canvas.delete("grim")

    if not len(data): # 데이터 없으면 return
        canvas.create_text(canvasWidth/2,(canvasHeight/2), text="No Data", tags="grim")
        return
    nData = len(data)
    nMax = max(data)
    nMin = min(data)

    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill='white', tag="grim")

    if nMax == 0:
        nMax = 1

    rectWidth = (canvasWidth // nData)
    bottom = canvasHeight - 20 
    maxheight = canvasHeight - 40 
    wherelist = ['휴게음식점', '편의점', '약국']   # 그래프 밑에 출력할 글
    for i in range(nData):                        # 각 데이터에 대해.. # max/min은 특별한 색으로.
        if nMax == data[i]: color="red"
        elif nMin == data[i]: color='blue'
        else: color="grey"
        
        curHeight = maxheight * data[i] / nMax  # 최대값에 대한 비율 반영
        top = bottom - curHeight 
        left = (i + 0.3) * rectWidth 
        right = (i + 0.7) * rectWidth
        canvas.create_rectangle(left, top, right, bottom, fill=color, tag="grim", activefill='yellow')
        # 위에 값, 아래에 어느시설인지
        canvas.create_text((left+right)//2, top-10, text=data[i], tags="grim")
        canvas.create_text((left+right)//2, bottom+10, text=wherelist[i], tags="grim")


def Map_new_tap():                            #맵 함수는 지도 출력 가능한경우 위도 경도를 가져와 새창에서 지도를 출력
    global Latitude, longitude, branch_name
    if (Latitude != None and longitude != None):
        map_osm = folium.Map(location=[float(Latitude), float(longitude)], zoom_start=25)
        folium.Marker([float(Latitude), float(longitude)], popup=branch_name).add_to(map_osm)
        map_osm.save('osm.html')            # html 파일로 저장
        webbrowser.open_new('osm.html')

def Search():                                 # 가운데 검색버튼 누르면 좌측리스트박스에 selection된 것의 상세정보 우측 리스트박스에 표시
    global right_listbox

    selection = left_listbox.curselection()
    if (len(selection) > 0):

        conn = openAPIserver(Complete_Url)
        tree = ElementTree.fromstring(conn)

        right_listbox.delete(0, left_listbox.size())      # 입력된거 리셋
        value = left_listbox.get(selection[0])
        i = 1

        itemele = tree.iter("row")
        for item in itemele:
            global branch_name
            branch_name = item.find("BIZPLC_NM")
            if (branch_name.text == value):
                global Latitude, longitude                     #위도 , 경도 , 도로명 or 지번 주소 가져가서 지도 출력용
                operation = item.find("BSN_STATE_NM")          # 영업 중인지
                road_name_add = item.find("REFINE_LOTNO_ADDR") # 도로명 주소  
                address = item.find("REFINE_ROADNM_ADDR")      # 지번 주소
                zip_code = item.find("REFINE_ZIP_CD")          # 우편번호
                callNum = item.find("LOCPLC_FACLT_TELNO")      # 전화번호

                Latitude = item.find("REFINE_WGS84_LAT").text        #위도
                longitude = item.find("REFINE_WGS84_LOGT").text       #경도

                right_listbox.insert(i - 1, "지점명 :" + str(branch_name.text))
                right_listbox.insert(i, "운영여부 :" + str(operation.text))
                if address != None:
                    right_listbox.insert(i + 1, "지번주소 :" + str(address.text))
                else:
                    right_listbox.insert(i + 1, "주소 없음")
                if road_name_add != None:
                    right_listbox.insert(i + 2, "지번주소 :" + str(road_name_add.text))
                else:
                    right_listbox.insert(i + 2, "도로명 주소 없음")
                if zip_code != None:
                    right_listbox.insert(i + 3, "우편번호 :" + str(zip_code.text))
                else:
                    right_listbox.insert(i + 3, "우편번호 없음")
                if callNum != None:
                    right_listbox.insert(i + 4, "전화번호 :" + str(callNum.text))
                else:
                    right_listbox.insert(i + 4, "전화번호 없음.")
                if Latitude != None and longitude != None:
                    right_listbox.insert(i + 5, "지도 출력 가능")
                else:
                    right_listbox.insert(i + 5, "지도 출력 불가")
                print(right_listbox.get(0, right_listbox.size()))
                break

def email_send():                       # G이메일 보내는 부분
    from email.mime.text import MIMEText
    global right_listbox
    a = str(right_listbox.get(0, right_listbox.size()))
    msg = MIMEText(a)
    msg['Subject'] = '제목: ' + right_listbox.get(0)
    sendMail('mykimis73@gmail.com', 'mykimis73@gmail.com', msg)

def sendMail(fromAddr, toAddr, msg):    # 이메일 보내기 추가 함수 부분
    import smtplib
    #  메일 서버와 connect하고 통신 시작
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()

    s.login('mykimis73@gmail.com','vhamicemykmacgyp')
    s.sendmail(fromAddr, [toAddr], msg.as_string())
    s.close()

def RestingUrl():          #휴게음식점 api   # GUi 편의시설 3종 버튼을 누르면 각각에 알맞는 Url을 주어 인터넷에서 가져오기까지의 시작점
    global Url
    Url = "RESRESTRT?KEY=9dff4350fafe400db05270b8161c46d3"
    whichpoint = 1                          # whichpoint는 그래프에 사용할 때 어느 시설에 추가하는지용
    listbox_print(whichpoint)

def ConvenienceUrl():     # 편의점 api
    global Url
    Url = "Resrestrtcvnstr?KEY=9dff4350fafe400db05270b8161c46d3"
    whichpoint = 2
    listbox_print(whichpoint)
    
def PharmacyUrl():         # 약국 api
    global Url
    Url = "Parmacy?KEY=9dff4350fafe400db05270b8161c46d3"
    whichpoint = 3
    listbox_print(whichpoint)

def listbox_print(whichpoint):      #위 3개의 Url중 하나를 받아서 인터넷 연결 및 가져온 데이터 출력함수 연결
    global Url
    global SIGUN_CD
    global Complete_Url
    global conn

    Complete_Url = 0
    Complete_Url = "https://openapi.gg.go.kr/" + Url + "&Type=xml" + SIGUN_CD # + "&pIndex=1" + "&pSize=100" 
    #Complete_Url = "https://openapi.gg.go.kr/Resrestrtcvnstr?KEY=9dff4350fafe400db05270b8161c46d3&Type=xml&pIndex=1&pSize=50&SIGUN_CD=41270"
    #print(SIGUN_CD)            # 3개 디버깅용
    #print(Complete_Url)

    conn = openAPIserver(Complete_Url)
    extractData(conn, whichpoint)


def openAPIserver(Complete_Url):            #인터넷 연결
    return requests.get(Complete_Url).text.encode('utf-8')

def extractData(strXml, whichpoint):
    tree = ElementTree.fromstring(strXml)   #인터넷에서 가져와서 리스트박스 출력부분

    global left_listbox
    left_listbox.delete(0,left_listbox.size())      # 입력된거 리셋
    i = 1
    cnt = 0
    itemElements = tree.iter("row") # item 엘리먼트 리스트 추출
    for item in itemElements:
        BIZPLC_NM = item.find("BIZPLC_NM")
        operation = item.find("BSN_STATE_NM")
        if (operation.text == "폐업" or operation.text == "폐업 등"):
            continue
        elif len(BIZPLC_NM.text) > 0:
            left_listbox.insert(i - 1, BIZPLC_NM.text)    #----리스트박스 출력완료 -> 리스트 클릭하면 오른쪽 상세알려줌
            cnt += 1
    
    global breakshop_cnt, conveniencestore_cnt, pharmacy_cnt
    if whichpoint == 1:
        breakshop_cnt += cnt
    elif whichpoint == 2:
        conveniencestore_cnt += cnt
    elif whichpoint == 3:
        pharmacy_cnt += cnt
    print(cnt)
    grapgdata = [breakshop_cnt, conveniencestore_cnt, pharmacy_cnt]       # 1 휴게점, 2 편의점 3, 약국
    drawGraph(Graph, grapgdata, 600, 200)     

def getstr(event):                                  # 콤보박스에서 가져온 떙땡시를 알맞는 번호로 변환하여 인터넷 Url완성부에 붙이는 용
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
