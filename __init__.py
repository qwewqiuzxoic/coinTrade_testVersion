import ccxtMd.ccxtClass as ccxtCalss #cctx 클래스
import siteObj.siteObj as site #cctx에 들어갈 key값 및 사이트 종류
import upbitMd.upbltClass as upbitWs
import telegramBot.telegramBot as tel #텔레그램
import time
from openpyxl import Workbook
from datetime import datetime


#tel 새로운 telegram에 연결시 생성자 파라미터에 토큰 집어넣기 
telBot = tel.telegramBot()

#마켓 설정
marketOpen = ccxtCalss.ccxtClass()
marketOpen.exchange_sites_list = site.list
marketOpen.exchange_sites_apiKey_dict = site.obj

#마켓 오픈
marketOpen.load_coin_market()

#마켓별 같은 코인 고르기
marketOpen.select_same_coin()

#엑셀
wb = Workbook()
sheet = wb.active

#저장 파일 이름 중복 오류 제거위해 이름 설정
databasename = str(datetime.today().month)+'_'+str(datetime.today().day)+\
               '_'+str(datetime.today().hour)+'_'+str(datetime.today().minute)+'_'+'dataBase.xlsx'

#타이머 + 로직 구성
def timeTest():
    start = time.time()

    #가격비교
    marketOpen.book_buy_sell_price()

    #가격 비교후 계좌 조회 -> 거래하기
    marketOpen.account_info()

    #excel File 로 저장하기
    for key, val in marketOpen.sell_buy_coin.items():
        sheet.append([key, val["buy"][0], val["buy"][1], val["sell"][0], val["sell"][1], val["gap"]])
    wb.save(databasename)
    
    #telegram 에 메세지 보내기 향 후 로직 수정 필요
    telBot.send_mess(marketOpen.sell_buy_coin)


    time.sleep(1)
    print("time :", time.time() - start)

upbit = upbitWs.upbitCalssWs()

if __name__ == '__main__':
    print(upbit.ws.on_open)
    upbit.ws.run_forever()
    '''
    while True:
        timeTest()
    '''