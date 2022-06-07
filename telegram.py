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