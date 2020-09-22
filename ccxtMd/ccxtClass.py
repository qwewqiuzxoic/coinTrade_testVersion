import ccxt

class ccxtClass():
    def __init__(self):
        # 코인 갭
        self.gap_per = 3

        #거래서 사이트 리스트
        self.exchange_sites_list = []

        #거래소 별 API 딕셔너리
        self.exchange_sites_apiKey_dict = {}

        #거래소 이름 : 거래소 오브젝트 딕셔너리
        self.exchange_sites_obj_dict = {}

        #코인 리스트
        self.coins_list = []

        #같은 코인 리스트
        self.same_coins_list = []

        #코인 사고 팔 것
        self.sell_buy_coin = {}

        #코인 주문 리스트
        self.buy_book_list = {}
        self.sell_book_list = {}

    #마켓 로드 하기 , 마켓을 변수에 할당하기
    def load_coin_market(self):
        for exchange in self.exchange_sites_list:
            site = getattr(ccxt, exchange)(self.exchange_sites_apiKey_dict[exchange])
            site.load_markets()
            self.exchange_sites_obj_dict[exchange] = site
            self.coins_list.append(set(site.markets.keys()))


    #코인 같은거 찾기
    def select_same_coin(self):
        for idx, coins in enumerate(self.coins_list):
            if idx == 0:
                list = coins
            else:
                list = list.intersection(coins)
        self.same_coins_list = list
        if len(self.same_coins_list) == 0:
            print('일치하는 코인이 없습니다.')


    #같은 코인 가격 비교하기 후 3퍼 차이 고르기
    def compare_coin_price(self):
        big_dict = dict()
        small_dict = dict()
        for coin_name in self.same_coins_list:
            for key, site in self.exchange_sites_obj_dict.items():
                site_info = site.fetch_trades(coin_name, limit=1)
                small_dict[site.id] = site_info[0]['price']
            buy_coin_price = min(small_dict.values())
            sell_coin_price = max(small_dict.values())
            buy_site_name = min(small_dict, key=lambda k: small_dict[k])
            sell_site_name = max(small_dict, key=lambda k: small_dict[k])
            per = (sell_coin_price - buy_coin_price) / sell_coin_price * 100
            if per > self.gap_per:
                big_dict[coin_name] = {
                    "buy": [buy_site_name, buy_coin_price],
                    "sell": [sell_site_name, sell_coin_price],
                    "gap": per
                }
            small_dict = {}
        self.sell_buy_coin = big_dict
        #print(self.sell_buy_coin)
        '''
        for key,val in self.sell_buy_coin.items():
            print("%s : %s" %(key, val))
        '''
        #self.book_buy_sell_price()
    #잔고 조회 후 코인 거래  +++++++++++++++++++++ 여기에 로직 추가 할 것
    def account_info(self):
        for key, val in self.sell_buy_coin.items():
            try:
                #self.buy_coin()
                print(self.exchange_sites_obj_dict[val['buy'][0]].fetch_balance(), 'ok')

            except Exception as e:
                print(111111)

                print('account info def %s:' %e)
            try:
                #self.sell_coin()
                print(self.exchange_sites_obj_dict[val['sell'][0]].fetch_balance(), 'ok')
            except Exception as e:
                print('account info def %s:' %e)


    #코인사기
    def buy_coin(self):
        for key, val in self.sell_buy_coin.items():
            try:
                order = self.exchange_sites_obj_dict[val['buy'][0]].create_limit_buy_order(key, 1, val['buy'][1], {'execInst': 'ParticipateDoNotInitiate'})
                self.buy_book_list[key] = order
            except Exception as e:
                print('buy def %s:' %e)

    #코인 팔기
    def sell_coin(self):
        for key, val in self.sell_buy_coin.items():
            try:
                order = self.exchange_sites_obj_dict[val['sell'][0]].create_limit_sell_order(key, 1, val['sell'][1], {'execInst': 'ParticipateDoNotInitiate'})
                self.sell_book_list[key] = order
            except Exception as e:
                print('sell def %s:' %e)

    #주문 확인
    def buy_order_confirm(self):
        for key, val in self.buy_book_list.items():
            self.exchange_sites_obj_dict[key].fetch_order(val['info']['orderID'], val['symbol'])

    def sell_order_confirm(self):
        for key, val in self.sell_book_list.items():
            self.exchange_sites_obj_dict[key].fetch_order(val['info']['orderID'], val['symbol'])

    #주문 취소
    def buy_order_cancel(self):
        print(11)
        #site.cancel_order(order['info']['orderID'], 'BTC/USD')

    def sell_order_cancel(self):
        print(11)
        #site.cancel_order(order['info']['orderID'], 'BTC/USD')


    #매도 매수 가격으로 구분
    def book_buy_sell_price(self):
        big_dict = dict()
        small_dict = dict()
        for coin in self.same_coins_list:
            for key, val in self.exchange_sites_obj_dict.items():
                order_book_info = val.fetch_order_book(coin)
                buy_first = order_book_info['bids'][0][0] ## 매도 1호
                sell_first = order_book_info['asks'][0][0] ## 매수 1호
                small_dict[key] = {
                    "buy" : buy_first,
                    "sell" : sell_first
                }
                #print("site :: %s   ///  coinname :: %s    ///    buy: %s,  sell:%s " %(key, coin, buy_first, sell_first))
            buy_min = min(small_dict, key=lambda k: small_dict[k]["buy"])
            sell_max = max(small_dict, key=lambda k: small_dict[k]["sell"])
            check_same = buy_min == sell_max
            if check_same:
                sell_max = sorted(small_dict, key=lambda k: small_dict[k]["sell"], reverse=True)[1]
            per = (small_dict[sell_max]["sell"]-small_dict[buy_min]["buy"])/small_dict[sell_max]["sell"] * 100
            if per>self.gap_per:
                big_dict[coin] ={
                    "buy": [buy_min, small_dict[buy_min]["buy"]],
                    "sell": [sell_max, small_dict[sell_max]["sell"]],
                    "gap": per
                }
            small_dict = {}
        self.sell_buy_coin = big_dict
