import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
import re
from datetime import date, datetime
import noti

def replyAptData(SIGUN_CD, user, Url):
    print(user, SIGUN_CD, Url)
    if Url == '100': Url = 'RESRESTRT?KEY=9dff4350fafe400db05270b8161c46d3'
    elif Url == '200': Url = "Resrestrtcvnstr?KEY=9dff4350fafe400db05270b8161c46d3"
    elif Url == '300': Url = "Parmacy?KEY=9dff4350fafe400db05270b8161c46d3"
    res_list = noti.getData( Url, SIGUN_CD )
    # 하나씩 보내면 메세지 개수가 너무 많아지므로
    # 300자까지는 하나의 메세지로 묶어서 보내기.
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.'%SIGUN_CD )

def save(user, loc_param):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTSusers( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return
    text = msg['text']
    args = text.split(' ')
    if text.startswith('검색') and len(args)>0:
        print('try to 검색', args[1])
        replyAptData(args[1], chat_id, args[2] )
    elif text.startswith('지역') and len(args)>0:
        print('try to 지역', args[1])
        replyAptData( '202205', chat_id, args[1] )
    elif text.startswith('저장') and len(args)>0:
        print('try to 저장', args[1])
        save( chat_id, args[1] )            # 세이브 부분
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )                    # 체크 부분
    else:
        noti.sendMessage(chat_id, '''모르는 명령어입니다.\n 검색 [지역번호] [100 = 휴게음식점, 200 = 편의점, 300 = 약국 중 숫자 입력]
 \n확인 중 하나의 명령을 입력하세요.\n 지역 ["가평군" : 41820, "고양시":  41280, "과천시": 41290, "광명시":  41210, "광주시" : 41610, "구리시" : 41310, "군포시" : 41410,\
        "김포시" : 41570, "남양주시": 41360, "동두천시" :  41250, "부천시": 41190, "성남시" : 41130, "수원시" :  41110, "시흥시" : 41390,\
        "안산시" : 41270, "안성시" :  41550, "안양시" : 41170, "양주시" : 41630, "양평군" : 41830, "여주시" :  41670, "연천군" :  41800,\
        "오산시" : 41370, "용인시" :  41460, "의왕시" :  41430, "의정부시" :  41150, "이천시"    :  41500, "파주시" :  41480, "평택시" : 41220,\
        "포천시" : 41650, "하남시" :  41450, "화성시" :  41590]
''')

#검색 지역번호 휴게음식점 == 이렇게 누르면 그에 해당하는 모든 휴게음식점 이름 및 정보 출력


today = date.today()
print('[',today,']received token :', noti.TOKEN)

from noti import bot
pprint(bot.getMe())

bot.message_loop(handle)

print('Listening...')

while 1:
    time.sleep(10)