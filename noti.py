import sys
import telepot
from pprint import pprint # 데이터를 읽기 쉽게 출력
from urllib.request import urlopen
import traceback
from xml.etree import ElementTree
from xml.dom.minidom import parseString

key = '9dff4350fafe400db05270b8161c46d3'
TOKEN = '5492320146:AAHmmPEGKY4uKwmNe-qczZiaK3u8W90WY_k'
MAX_MSG_LENGTH = 300
baseUrl = 'https://openapi.gg.go.kr/'
bot = telepot.Bot(TOKEN)

def getData(Url, SIGUN_CD):
    res_list = []
    Complete_Url = baseUrl + Url + "&Type=xml" + SIGUN_CD
    #"https://openapi.gg.go.kr/" + Url + "&Type=xml" + SIGUN_CD
    res_body = urlopen(Complete_Url).read()
    strXml = res_body.decode('utf-8')
    tree = ElementTree.fromstring(strXml)

    items = tree.iter("row")    # return list type
    for item in items:              #--------------------------할것
        branch_name = item.find("BIZPLC_NM").text
        operation = item.find("BSN_STATE_NM").text         # 영업 중인지
        road_name_add = item.find("REFINE_LOTNO_ADDR").text # 도로명 주소  
        callNum = item.find("LOCPLC_FACLT_TELNO")      # 전화번호
        if callNum != None:
            #right_listbox.insert(i + 4, "전화번호 :" + str(callNum.text))
            callNum = str(callNum.text)
        else: callNum = "전화번호 없음"

        if (operation == "폐업" or operation == "폐업 등"): #폐업 빼기
            continue

        row = str(branch_name) + '/' + str(operation) + '/' + str(road_name_add) + '/' +str(callNum)
        res_list.append(row)
        
    return res_list


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        # 예외 정보와 스택 트레이스 항목을 인쇄.
        traceback.print_exception(*sys.exc_info(), file=sys.stdout)