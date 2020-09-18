import ccxtMd.ccxtClass as ccxtCalss
import  siteObj.siteObj as site
import time
from openpyxl import Workbook
from datetime import datetime

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
databasename = str(datetime.today().month)+'_'+str(datetime.today().day)+'_'+str(datetime.today().hour)+'_'+str(datetime.today().minute)+'_'+'dataBase.xlsx'
def timeTest():
    start = time.time()
    #가격비교
    marketOpen.compare_coin_price()
    marketOpen.account_info()
    for key, val in marketOpen.sell_buy_coin.items():
        sheet.append([key, val["buy"][0], val["buy"][1], val["sell"][0], val["sell"][1], val["gap"]])
    wb.save(databasename)
    time.sleep(1)
    print("time :", time.time() - start)


if __name__ == '__main__':
    while True:
        timeTest()
