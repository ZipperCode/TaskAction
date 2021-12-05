import json
import random
import time

import requests
import uuid
import hashlib

import os

type_sign = 103
type_read_news = 104
type_video_ad = 105
type_game = 106
type_rec_red_package = 107
type_search = 108
type_invite_code = 109
type_time_box = 110
type_first_with_draw = 112
type_lottery_phone_coin = 113
type_read_rain = 114
type_lottery_phone = 115
type_double_coin = 116
type_extra_coin = 117
type_short_video = 118
with_draw = 1001
flow = 1002
send_red_package = 1003

class oupeng:

    def __init__(self, token):
        self.token = token
        self.reward_coin = 0
        self.user_coin = 0

    def rule_info(self, key):
        url = "http://wz.oupeng.com/rule/info"
        data = "{\"type\": 0}"
        res_data = self.req(url, data)

        if res_data is not None:
            delay(5)
            return res_data[key]
        delay(5)

    def coin_double(self, type, coin):
        """
        收取金币
        @:param type 任务id
        @:param coin 金币
        :return:
        """
        url = "http://wz.oupeng.com/coin/double"
        data = {
            "type": type,
            "coinAmount": coin
        }
        data = str(json.dumps(data))
        res_data = self.req(url, data)
        if res_data is not None:
            self.reward_coin += res_data["coinAmount"]
        pass

    def coin_popuptask(self):
        """
        :return:
        """
        url = "http://wz.oupeng.com/coin/popuptask"
        data = "{}"
        res_data = self.req(url, data)
        if res_data is not None:
            self.reward_coin += int(res_data['coinAmount'])
        pass

    def account_info(self):
        url = "http://wz.oupeng.com/account/info"
        data = "{}"
        res_data = self.req(url, data)
        if res_data is not None:
            self.user_coin = res_data['coinAmount']
        pass

    def check_in(self):
        """
        签到
        :return:
        """
        url = "http://wz.oupeng.com/checkin"
        data = "{}"
        res_data = self.req(url, data)
        if res_data is not None:
            try:
                self.reward_coin += int(res_data['data'])
            except TypeError:
                pass
            time.sleep(10)
            self.coin_double(103, 99)
        delay(15)

    def coin_list(self):
        url = "http://wz.oupeng.com/coin/list"
        data = {
            "type": 0,
            "beginDate": "20211204",
            "endDate": "20211204"
        }
        res_data = self.req(url, json.dumps(data))

        if res_data is not None:
            delay(5)
            return res_data
        delay(10)

    def detail(self, key):
        url = "http://wz.oupeng.com/coin/detail"
        data = "{}"
        res_data = self.req(url, data)
        if res_data is not None:
            return res_data[key]

    def video_ad(self):
        """
        看视频
        [{\"type\":105,\"amount\":200,\"id\":\"dc8053db008ee07bb663528621a258fd\",
        \"posId\":\"adPool\",\"name\":\"toutiao\",\"slotId\":\"945699354\"}]
        :return:
        """
        log("开始执行看视频领金币")

        detail_data = self.detail("rewardVideo")
        if detail_data is None:
            log("detail_data#rewardVideo 数据获取为空")
            return
        rule_video_ad = self.rule_info("videoAd")
        name = "toutiao"
        slot_id = "945699354"

        amount = detail_data['coinAmount']
        total = detail_data['total']
        current = detail_data['current']

        for index in range(current, total):
            log("执行第{0}/${1}次看视频".format(index, total))
            if rule_video_ad is not None:
                ad = random.choice(list(rule_video_ad["adPool"]))
                if ad is not None:
                    name = ad['name']
                    slot_id = ad['slotId']
            id = hashlib.md5(uuid_str().encode("utf-8")).hexdigest()
            data = {
                "type": type_video_ad,
                "amount": amount,
                "id": id,
                "posId": "adPool",
                "name": name,
                "slotId": slot_id
            }
            self.coin_earn(type_read_news, amount, json.dumps([data]))
            delay(25)
        log("开始执行看视频领金币执行结束, 10s后执行下一个任务")
        delay(10)

    def read_news(self):
        """
        阅读文章
        :return:
        """
        log("开始执行阅读领金币")

        detail_data = self.detail("readNews")
        if detail_data is None:
            log("detail_data#readNews 数据获取为空")
            return
        delay(5)
        amount = detail_data['coinAmount']
        total = detail_data['total']
        current = detail_data['current']
        for index in range(current, total):
            log("执行第{0}/${1}次阅读，延迟25s".format(index, total))
            id = hashlib.md5(uuid_str().encode("utf-8")).hexdigest()
            data = {
                "type": type_read_news,
                "amount": amount,
                "id": id
            }
            self.coin_earn(type_search, amount, json.dumps([data]))
            delay(25)
        log("执行阅读领金币执行结束, 10s后执行下一个任务")
        delay(10)

    def search(self):
        """
        搜索
        :return:
        """
        log("开始执行搜索领金币")

        detail_data = self.detail("search")
        if detail_data is None:
            log("detail_data#search 数据获取为空")
            return

        amount = detail_data['coinAmount']
        total = detail_data['total']
        current = detail_data['current']
        for index in range(current, total):
            log("执行第{0}/${1}次搜索，延迟25s".format(index, total))
            id = hashlib.md5(uuid_str().encode("utf-8")).hexdigest()
            data = {
                "type": type_search,
                "amount": amount,
                "id": id
            }
            self.coin_earn(type_search, amount, json.dumps([data]))
            delay(25)
        log("执行搜索领金币执行结束, 10s后执行下一个任务")
        delay(10)

    def coin_earn(self, type, amount, data):
        """
        看视频
        104 阅读文章 40 [{\"type\":104,\"amount\":40,\"id\":\"075c08d4aeba18d2c83d379d76dcd796\"}]
        搜索 [{\"type\":108,\"amount\":100,\"id\":\"eed546148fc1c2bdf08b49827ed4ba86\"}]
        :return:
        """
        url = "http://wz.oupeng.com/coin/earn"
        try:
            res_data = self.req(url, data)
            if res_data is not None:
                self.reward_coin += int(res_data['coinAmount'])
                delay(20)
                self.coin_double(type, amount)
        except:
            pass
        delay(10)
        pass

    def drawprizecount(self):
        url = "http://wz.oupeng.com/coin/query/drawprizecount"
        data = "{}"
        res_data = requests.post(url, headers=get_header_2(self.token), json=data).json()
        if res_data is not None:
            redpackrain = res_data['data']['redpackrain']
            a = redpackrain['amount']
            t = redpackrain['total']
            for index in range(0, t):
                log("红包雨当前次数{0}/{1}".format(index, t))
                try:
                    if a == 0:
                        self.earndrawprizecount(type_read_rain)
                        delay(5)
                    coins, rid = self._start_redpackrain()
                    if coins == 0 and rid == "":
                        continue
                    delay(30)
                    self._redpackrain(rid, coins)
                except:
                    pass

    def _start_redpackrain(self):
        url = "http://wz.oupeng.com/coin/start/redpackrain"
        res_data = requests.post(url, headers=get_header_2(self.token)).json()
        if res_data is not None:
            if res_data['code'] == 1003:
                return 0, ""
            coins = sum(res_data['data']['redpackList'])
            rid = res_data['data']['rid']
            return coins, rid
        return 0, ""

    def _redpackrain(self, rid, coins):
        url = "http://wz.oupeng.com/coin/redpackrain"
        data = {
            "rid": rid,
            "coinAmount": coins
        }
        requests.post(url, headers=get_header_2(self.token), data=data).json()
        self.reward_coin += coins
        delay(5)

    def earndrawprizecount(self, type):
        """
        获取红包雨次数
        :return:
        """
        url = "http://wz.oupeng.com/coin/earndrawprizecount"
        data = {
            "type": type
        }
        res_data = self.req(url, json.dumps(data))
        if res_data is not None:
            return res_data['redpackRainCount'], res_data['drawphoneCount']

    def drawphone(self):
        """
        抽奖手机

        :return:
        """
        url = "http://wz.oupeng.com/coin/drawphone"
        res_data = self.req(url, None)
        if res_data is not None:
            pass
        pass

    def with_draw(self):
        url = "http://wz.oupeng.com/withdraw/product"
        data = "{}"
        res_data = self.req(url, data)
        if res_data is not None:
            product_list = res_data["list"]
            if product_list is not None and isinstance(product_list, list):
                self.account_info()
                delay(5)
                sorted(product_list, key=lambda v: v['coinAmount'], reverse=True)
                for p in product_list:
                    coin_amount = p['coinAmount']
                    if self.user_coin >= coin_amount:
                        url = "http://wz.oupeng.com/coin/withdraw"
                        data = {
                            "productId": p['productId'],
                            "vendor": 1
                        }
                        delay(5)
                        res_data = self.req(url, data)
                        if res_data is not None:
                            log("提现成功 提现花费：{0} 金币 ".format(res_data['coinAmount']))
        pass

    def run(self):
        self.account_info()
        self.check_in()
        self.video_ad()
        self.search()
        self.read_news()
        self.drawprizecount()
        log("任务执行完毕，总获得{0}, 开始执行提现".format(self.reward_coin))
        self.with_draw()
        pass

    def req(self, url, data):
        t = time_str()
        nonce = uuid_str()
        print("data = " + data)
        payload = json.dumps({
            "data": data,
            "sign": sign(data, t, nonce)
        })
        resp = requests.request("POST", url, headers=get_header(self.token, t, nonce), data=payload).json()
        print("resp = " + str(resp))
        if resp['code'] == 0:
            data = resp['data']
            if isinstance(data, str):
                data = json.loads(str(resp['data']))
            return data


def delay(second):
    time.sleep(second)


def log(msg):

    print("【欧朋极速版】 >> {0}".format(msg))


def time_str():
    return str(int(time.time()))


def uuid_str():
    return str(uuid.uuid1())


def sign(data, timestamp, nonce):
    s = "{0}{1}{2}diafiWQERQ303redafDpKIQZF!)7lambXEDOjia3".format(data, timestamp, nonce)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def get_header(token, timestamp, nonce):
    return {
        'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)',
        'X-Branding': 'oupengtor_13_03',
        'X-Campaign': 'oupengtor-13-b',
        'X-Channel': 'xiaomi_001',
        'X-Package-Name': 'com.oupeng.browser',
        'X-Security-ANDROID-Id': 'a2030a6423d20d22',
        'X-Security-Device-Id': '14b6e4b51f6e4d4e9144ed1306d82bbf',
        'X-Security-IMEI-Id': 'NONE',
        'X-Security-MAC': 'e6:86:9d:65:1d:55',
        'X-Security-Nonce': str(nonce),
        'X-Security-OS_BRANDING': 'Xiaomi',
        'X-Security-OS_MODEL': 'MI 6',
        'X-Security-Source': '9458e58f',
        'X-Security-Timestamp': str(timestamp),
        'X-Security-Token': str(token),
        'X-Security-VERSIONNAME': '13.03.0.4',
        'Content-Type': 'application/json'
    }


def get_header_2(token):
    return {
        "Origin": "http://wzw.oupeng.com",
        "Referer": "http://wzw.oupeng.com/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; MI 6 Build/RQ3A.210605.005; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.101 Mobile Safari/537.36",
        "X-Requested-With": "com.oupeng.browser",
        "X-Security-Token": token
    }


if __name__ == "__main__":
    config = str(os.getenv("OUPENG_CONFIG"))
    if config is not None and config != "":
        log("config = " + str(config))
        config = json.loads(config)
        if isinstance(config, list):
            for c in config:
                token = c['token']
                oupeng(token).run()
            pass
        else:
            token = config['token']
            oupeng(token).run()

    log("未获取到相关配置信息")

