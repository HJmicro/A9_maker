import json
import requests
import time
import hmac
import hashlib
import base64
import random

class FeiShuRobot:


    def __init__(self, robot_id, secret) -> None:
        self.robot_id = robot_id
        self.secret = secret


    def gen_sign(self):
        # 拼接timestamp和secret
        timestamp = int(time.time())
        #timestamp = int(round(time.time() * 1000))
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        print(timestamp, sign)
        return str(timestamp), str(sign)

    def get_token(self):
        """获取应用token，需要用app_id和app_secret，主要是上传图片需要用到token"""

        url = r"https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        headers = {"Content-Type": "text/plain"}
        Body = {
            "app_id": self.robot_id,
            "app_secret": self.secret
        }
        r = requests.post(url, headers=headers, json=Body)
        return json.loads(r.text)['tenant_access_token']


    def send_text(self, text):
        """发送普通消息"""

        try:
            url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{self.robot_id}"
            headers = {"Content-Type": "text/plain"}
            timestamp, sign = self.gen_sign()
            data = {
                "timestamp": timestamp,
                "sign": sign,
                "msg_type":"text",
                "content":{
                    "text":text
                }

            }
            r = requests.post(url, headers=headers, json=data)
            print("发送飞书成功")
            print(r.text)
            return r.text
        except Exception as e:
            print("发送飞书失败:", e)


def feishu_test(coin):
    robot_id = 'ed670adc-8c8d-4fd5-9d9c-b40549ff0900'
    secret = 'FBN06TuEvhiKHCU4I98lch'

    feishu = FeiShuRobot(robot_id, secret)
    feishu.send_text(coin)


def get_res():

    proxy_list = [
        '183.95.80.102:8080',
        '123.160.31.71:8080',
        '115.231.128.79:8080',
        '166.111.77.32:80',
        '43.240.138.31:8080',
        '218.201.98.196:3128'
    ]

    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    ]
    # urls_old = ["nothing"]
    # check_value = [0] * len(urls_old)
    with open('address','r') as url_file:
        urls_old = url_file.readlines()
    try:
        with open('coinlist','r') as coin_file:
            check_value = coin_file.readlines()
            for i in range(len(check_value)):
                check_value[i] = check_value[i].replace('\n','')
            if len(urls_old) > len(check_value):
                for i in range(len(urls_old) - len(check_value)):
                    check_value.append(0)
    except Exception as e:
        print("no coin_list file found,create")
        check_value = [0] * len(urls_old)

    while True:
        with open("address", 'r') as file:
            urls_new = file.readlines()
        if len(urls_new) < len(urls_old):
            for i, url in enumerate(urls_old):
                if url not in urls_new:
                    check_value.pop(i)
            urls_old = urls_new
            print("urls decreates,now check_value is:", end="")
            print(check_value)
        if len(urls_new) > len(urls_old):
            for i in range(len(urls_new) - len(urls_old)):
                check_value.append(0)
            urls_old = urls_new
            print("urls decreates,now check_value is:", end="")
            print(check_value)
        for line in urls_old:
            url = line.strip('\n')
            for i in range(1, 20):
                header = random.choice(my_headers)
                proxy = random.choice(proxy_list)
                res = requests.get(
                    url,
                    headers={'User-Agent': header},
                    proxies={'HTTPS': proxy}
                )

                if str(res) == '<Response [200]>':
                    print(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                        time.time()))) + " " + url.split('=')[-1] + " connect ok")
                    break
            else:
                print("爬取" + url + "重试20次超时，请检查")
                # feishu_test("爬取" + url + "重试20次超时，请检查")
            time.sleep(1)
        with open('delete', 'r') as delete_file:
            tmp_list = delete_file.readlines()
            delete_list = [s.rstrip() for s in tmp_list]
            print("delete list is: ", delete_list)
        for i,my_url in enumerate(urls_old):
            header = random.choice(my_headers)
            proxy = random.choice(proxy_list)
            url = my_url.strip('\n')
            res = requests.get(
                url,
                headers={'User-Agent': header},
                proxies={'HTTPS': proxy}
            )
            res_list = res.text.strip().split('\n')
            address = url.split('=')[-1]
            with open('binance_address','r') as binance_file:
                binance_address = binance_file.readlines()

            # if not binance_vlaue :
            #     binance_value = [0] * len(binance_address)
            for j in range(len(res_list)):

                if "address/" + address in res_list[j]:

                    if  all( i.strip() not in res_list[j + 1] for i in binance_address):
                        cur_mount = res_list[j + 5]
                        coin = cur_mount.split(" ")[-1]

                        if check_value[i] == 0:
                            check_value[i] = cur_mount
                            break
                        elif coin in delete_list:
                            print("coin delete catch,now detele address:" + address)
                            with open('deleted_address','a') as delete_address:
                                delete_address.write(coin + "  " + urls_old[i])
                            urls_old.pop(i)
                            check_value.pop(i)
                            break
                        elif cur_mount == "0 " + coin:
                            print("need delete address " + address)
                            with open('deleted_address','a') as delete_address:
                                delete_address.write(coin + "  " + urls_old[i])
                            urls_old.pop(i)
                            check_value.pop(i)
                            break
                        elif str(cur_mount) != check_value[i]:
                            feishu_test(
                                coin + " changed，before:" + check_value[i].split('.')[0] + ",after:" + cur_mount.split('.')[0] + " refer to ：" + url)
                            check_value[i] = str(cur_mount)
                            break
                        print(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                            time.time()))) + " " + coin + " " + address + " no change current"
                                                                          " count: " + cur_mount)
                    else:
                        print('binance address catched,address is:',address)
                        cur_mount = res_list[j + 6]
                        coin = cur_mount.split(" ")[-1]
                        cur_value = res_list[j + 10]
                        if coin in delete_list:
                            print("coin delete catch,now detele address:" + address)
                            with open('deleted_address','a') as delete_address:
                                delete_address.write(coin + "  " + urls_old[i])
                            urls_old.pop(i)
                            check_value.pop(i)
                            break
                        #print('current binance address: ' + address +"current hold coin: " + coin +": " + cur_mount  +" hold value: " + cur_value)
                        if str(cur_mount) != check_value[i]:
                            feishu_test(
                                coin + "币安地址有变化，变化前持仓:" + str(check_value[i]) + ",变化后持仓:" + str(cur_mount) + "请到：" + url + "查看")
                            check_value[i] = str(cur_mount)
                        break

        print("now check_value is:",end="")
        print(check_value)
        with open('coinlist','w') as coin_file:
            for coin_list in check_value:
                coin_file.write(str(coin_list) + '\n')
        if urls_old != urls_new:
            with open('address','w') as file_new:
                for urls in urls_old:
                    file_new.write(urls)
        print("***********************************华丽的分割线*************************************")
        time.sleep(random.randint(100,300))


if __name__ == '__main__':
    get_res()

