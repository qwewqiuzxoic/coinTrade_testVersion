import ccxtMd.ccxtClass as ccxtCalss
import  siteObj.siteObj as site
import time

marketOpen = ccxtCalss.ccxtClass()
marketOpen.exchange_sites_list = site.list
marketOpen.exchange_sites_apiKey_dict = site.obj

#마켓 오픈
marketOpen.load_coin_market()

#마켓별 같은 코인 고르기
marketOpen.select_same_coin()

def timeTest():
    start = time.time()
    #가격비교
    marketOpen.compare_coin_price()
    marketOpen.account_info()
    time.sleep(1)
    print("time :", time.time() - start)

if __name__ == '__main__':
    while True:
        timeTest()