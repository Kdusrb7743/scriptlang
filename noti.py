import sys
import telepot
from pprint import pprint # 데이터를 읽기 쉽게 출력
from urllib.request import urlopen
import traceback
from xml.etree import ElementTree
from xml.dom.minidom import parseString

key = '9dff4350fafe400db05270b8161c46d3'
TOKEN = '5544958695:AAFpwKDUT25HUTZ7i4pExUOHtdDr_Xgffeo'
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
        branch_name = item.find("BIZPLC_NM")
        operation = item.find("BSN_STATE_NM")          # 영업 중인지
        road_name_add = item.find("REFINE_LOTNO_ADDR") # 도로명 주소  
        address = item.find("REFINE_ROADNM_ADDR")      # 지번 주소
        zip_code = item.find("REFINE_ZIP_CD")          # 우편번호
        callNum = item.find("LOCPLC_FACLT_TELNO")      # 전화번호

        Latitude = item.find("REFINE_WGS84_LAT")        #위도
        longitude = item.find("REFINE_WGS84_LOGT")       #경도

        #row =
        res_list.append(row)
        
        return res_list


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        # 예외 정보와 스택 트레이스 항목을 인쇄.
        traceback.print_exception(*sys.exc_info(), file=sys.stdout)