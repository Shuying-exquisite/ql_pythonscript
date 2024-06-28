import streamlit as st
import hashlib
import random
import string
import time
import re
import requests
from os import environ, path
from functools import partial
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import urllib.parse
class log:
    def __init__(self):
        self.log_data = {}
    def dllog(self):
        url = "https://api.txttool.cn/netcut/note/info/"
        headers = {
            'Host': 'api.txttool.cn',
            'Origin': 'https://netcut.cn',
            'Referer': 'https://netcut.cn/396838qq',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
        data = {'note_name': '396838qq', 'note_pwd': '888888'}
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            self.log_data = response.json().get('data', {})
            self.ip()
        else:
            st.write("请求失败")

    def xieru(self):
        url = 'https://api.txttool.cn/netcut/note/save/'
        headers = {
            'Host': 'api.txttool.cn',
            'Origin': 'https://netcut.cn',
            'Referer': 'https://netcut.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
        content = f"{self.log_data.get('note_content', '')}\n时间：{self.log_data.get('updated_time', '')} 次数{self.log_data.get('read_count', 0)}{self.nr}"
        data = {
            'note_name': self.log_data.get('note_name', ''),
            'note_id': self.log_data.get('note_id', ''),
            'note_content': content,
            'note_token': self.log_data.get('note_token', ''),
            'expire_time': '259200',
            'note_pwd': '888888'
        }
        response = requests.post(url, headers=headers, data=data)
    def ip(self):
        url = "https://api.jingjiequ.com/tools/local_ip"
        headers = {
            'Origin': 'https://jingjiequ.com',
            'Referer': 'https://jingjiequ.com/',
            'Sec-Ch-Ua': 'Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':"Windows",
            'accept':'application/prs.jjq.v1+json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
        r = requests.get(url, headers=headers)
        i= r.json()['addresses']
        dz=i[0]['address']
        dze=i[1]['address']
        url='https://test.ipw.cn/api/ip/myip?json'
        headers={'Origin':'https://ipw.cn','Referer':'https://ipw.cn/ipv6webcheck/?','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 'querySuccess':
               ip = data.get('IP', '') 
               IPVersion = data.get('IPVersion', '')
               if not ip or not IPVersion:
                    ip='没有查询到IP'
                    IPVersion='没有查询到IP'
            sj = time.localtime()
            ts = time.strftime("%Y-%m-%d %H:%M:%S", sj)
        self.nr = (f"\n当前登录IP：{ip}  {IPVersion} \n当前登录地址：{dz}     {dze}\n时间：{ts}\n==============================================================")
        st.write(self.nr)
        self.xieru()





def get_environ(key, default="", output=True):
    def no_read():
        if output:
            st.write(f"未填写环境变量 {key} 请添加")

        return default

    return environ.get(key) if environ.get(key) else no_read()


def generate_random_string(length):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def pd1(ck):
    plaintext = ck
    public_key_base64 = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD6XO7e9YeAOs+cFqwa7ETJ+WXizPqQeXv68i5vqw9pFREsrqiBTRcg7wB0RIp3rJkDpaeVJLsZqYm5TW7FWx/iOiXFc+zCPvaKZric2dXCw27EvlH5rq+zwIPDAJHGAfnn1nmQH7wR3PCatEIb8pz5GFlTHMlluw4ZYmnOwg+thwIDAQAB"

    public_key = RSA.import_key(base64.b64decode(public_key_base64))
    cipher = PKCS1_v1_5.new(public_key)
    cipher_text = cipher.encrypt(plaintext.encode('utf-8'))
    encrypted_data_base64 = base64.b64encode(cipher_text).decode('utf-8')
    cipher_text = encrypted_data_base64
    url_safe_cipher_text = urllib.parse.quote(cipher_text, safe='')
    return url_safe_cipher_text


class Ghdy:
    
    def __init__(self, ck):
        url = "https://passport.tmuyun.com/web/oauth/credential_auth"
        url_d = 'https://vapp.taizhou.com.cn/api/zbtxz/login'
        m = pd1(ck[0])
        s = ck[1]  
        head ={
            'Cache-Control': 'no-cache',
            'User-Agent': 'ANDROID;9;10019;5.3.1;1.0;null;16T',
            'X-REQUEST-ID': '2120678b-84a7-40f1-8c92-df789980f821',
            'X-SIGNATURE': '06152b2984fd2b976e183cba4d588693c55b9ebc46814c59ac49b0e7bb63e946',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'COOKIE': 'SESSION=YTVlNTllZmUtNjliNy00YjZiLWI0MjUtMmExZjFhYzRlYzQ5; Path=/; HttpOnly; SameSite=Lax',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Length': '232',
        }
        head_d = {
            "X-SESSION-ID": "6498052ebf15a44961f350e1",
            "X-REQUEST-ID": "7c549049-a97b-4acb-96c6-3e2db706667d",
            "X-TIMESTAMP": "1687685127765",
            "X-SIGNATURE": "50e1530a02086535f5f0c2c58e7bbdea521468d3e5a2874541456da7755bbd6e",
            "X-TENANT-ID": "64",
            "User-Agent": "5.3.1;00000000-699e-76bc-ffff-ffff9e3d172a;Meizu 16T;Android;9;huawei",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "67",
            "Host": "vapp.taizhou.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        data = f'client_id=10019&password={m}&phone_number={s}'
      #  st.write(data)
        
        r = requests.post(url,headers=head,data=data)
        time.sleep(2)
        if r.json()['code'] == 0:
            yzm = r.json()['data']['authorization_code']['code']
            data_d = f'check_token=&code={yzm}&token=&type=-1&union_id='
         #   st.write(data_d)
            r_d = requests.post(url=url_d,headers=head_d,data=data_d)
            if r_d.json()['code'] == 0:
                sessid = r_d.json()['data']['session']['id']
                accid = r_d.json()['data']['account']['id']
            else:
                st.write('账号或密码错误:具体报错',r_d.text)
            
        elif r.json()['code'] == 100:
            st.write(r.json()['message'])
            return
        else:
            st.write('未知错误具体看响应:',r.text)
            return
        
        self.account = accid
        self.session = sessid
        self.id_dict = {}
        self.JSESSIONID = ''
        self.s_JSESSIONID = ''
        self.msg = ''

        
    def login(self):
        try:
            time.sleep(0.5)
            url = "https://xmt.taizhou.com.cn/prod-api/user-read/app/login"
            headers = {
                'Host': 'xmt.taizhou.com.cn',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app',
                'Accept': '*/*',
                'X-Requested-With': 'com.shangc.tiennews.taizhou',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://xmt.taizhou.com.cn/readingAward/',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            params = {
                'id': self.account,
                'sessionId': self.session,
                'deviceId':'00000000-699e-76bc-ffff-ffff9e3d172a'
            }
            r = requests.get(url, params=params, headers=headers)
            if '成功' in r.json()['msg']:
               # xx = f'🚀登录成功：{r.json()["data"]["nickName"]}'
                #self.msg += xx + '\n'
               # st.write(xx)
                jsessionid = r.cookies
                cookies_dict = jsessionid.get_dict()
                for k, y in cookies_dict.items():
                    self.JSESSIONID = f'{k}={y}'
            elif '失败' in r.json()['msg']:
                xx = f'⛔️{r.json()["msg"]}'
                self.msg += xx + '\n'
                st.write(xx)
        except Exception as e:
            st.write(e)

    def get_id(self):
        try:
            today = datetime.today().strftime('%Y%m%d')
            url = f'https://xmt.taizhou.com.cn/prod-api/user-read/list/{today}'
            headers = {
                'Host': 'xmt.taizhou.com.cn',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app',
                'Accept': '*/*',
                'X-Requested-With': 'com.shangc.tiennews.taizhou',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://xmt.taizhou.com.cn/readingAward/',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': self.JSESSIONID,
            }

            r = requests.get(url, headers=headers)
            if '成功' in r.json()['msg']:
                r_list = r.json()['data']['articleIsReadList']
                id_dict = {}
                for i in r_list:
                    id_dict[i['id']] = i['newsId']
                self.id_dict = id_dict
                if self.id_dict:
                    xx = "✅文章加载成功"
                    self.msg += xx + '\n'
                    st.write(xx)
            elif '重新' in r.json()['msg']:
                xx = f'⛔️文章加载失败：{r.json()["msg"]}'
                st.write(xx)
                self.msg += xx + '\n'

            else:
                xx = f'⛔️请求异常：{r.json()["msg"]}'
                st.write(xx)
                self.msg += xx + '\n'

        except Exception as e:
            st.write(e)

    def look(self):
        try:
            for idd, new_id in self.id_dict.items():
                a8 = generate_random_string(8)
                b4 = generate_random_string(4)
                c4 = generate_random_string(4)
                d4 = generate_random_string(4)
                e12 = generate_random_string(12)
                request = f'{a8}-{b4}-{c4}-{d4}-{e12}'
                current_timestamp = int(time.time() * 1000)
                sha = f'/api/article/detail&&{self.session}&&{request}&&{current_timestamp}&&FR*r!isE5W&&64'
                sha256 = hashlib.sha256()
                sha256.update(sha.encode('utf-8'))
                signature = sha256.hexdigest()
                url = 'https://vapp.taizhou.com.cn/api/article/detail'
                headers = {
                    'X-SESSION-ID': self.session,
                    'X-REQUEST-ID': f'{request}',
                    'X-TIMESTAMP': f'{current_timestamp}',
                    'X-SIGNATURE': f'{signature}',
                    'X-TENANT-ID': '64',
                    'User-Agent': '5.3.1;00000000-699e-0680-ffff-ffffc24c26a8;Xiaomi Redmi Note 8 Pro;Android;11;tencent',
                    'X-ACCOUNT-ID': self.session,
                    'Cache-Control': 'no-cache',
                    'Host': 'vapp.taizhou.com.cn',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                }

                params = {
                    'id': new_id,
                }
                r = requests.get(url, params=params, headers=headers)
                if r.json()['message'] == 'success':
                    xx = f'✅开始浏览《{r.json()["data"]["article"]["list_title"]}》'
                    st.write(xx)
                    self.msg += xx + '\n'
                    time.sleep(3)
                    current_timestamp = int(time.time() * 1000)
                    sha = f'&&{idd}&&TlGFQAOlCIVxnKopQnW&&{current_timestamp}'
                    md5 = hashlib.md5()
                    md5.update(sha.encode('utf-8'))
                    signature = md5.hexdigest()
                    headers = {
                        'Host': 'xmt.taizhou.com.cn',
                        'Connection': 'keep-alive',
                        'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app',
                        'Accept': '*/*',
                        'X-Requested-With': 'com.shangc.tiennews.taizhou',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Dest': 'empty',
                        'Referer': 'https://xmt.taizhou.com.cn/readingAward/',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Cookie': self.JSESSIONID,
                    }
                    params = {
                        'articid': idd,
                        'timestamp': current_timestamp,
                        'signature': signature,
                    }
                    r = requests.get(
                        'https://xmt.taizhou.com.cn/prod-api/already-read/article',
                        params=params,
                        headers=headers,
                    )
                    if '成功' in r.json()['msg']:
                        xx = f'✅浏览完成'
                        st.write(xx)
                        self.msg += xx + '\n'
                    elif '重新' in r.json()['msg']:
                        xx = f'⛔️浏览失败：{r.json()["msg"]}'
                        st.write(xx)
                        self.msg += xx + '\n'
                    else:
                        xx = f'⛔️浏览异常：{r.json()["msg"]}'
                        st.write(xx)
                        self.msg += xx + '\n'
                elif '不存在' in r.json()['msg']:
                    xx = f'⛔️浏览失败：{r.json()["msg"]}'
                    st.write(xx)
                    self.msg += xx + '\n'

                else:
                    xx = f'⛔️浏览异常：{r.json()["msg"]}'
                    st.write(xx)
                    self.msg += xx + '\n'

            c_headers = {
                'Host': 'xmt.taizhou.com.cn',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app',
                'Accept': '*/*',
                'X-Requested-With': 'com.shangc.tiennews.taizhou',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://xmt.taizhou.com.cn/readingAward/',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': self.JSESSIONID,
            }
            today = datetime.today().strftime('%Y%m%d')
            c_r = requests.get(f'https://xmt.taizhou.com.cn/prod-api/user-read-count/count/{today}', headers=c_headers)
            if '成功' in c_r.json()['msg']:
                xx = f'✅全部浏览完成，准备开始抽红包吧！'
                st.write(xx)
                self.msg += xx + '\n'
            else:
                xx = c_r.json()['msg']
                st.write(xx)
                self.msg += xx + '\n'
        except Exception as e:
            st.write(e)

    def chou(self):
        try:
            c_headers = {
                'Host': 'srv-app.taizhou.com.cn',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app',
                'Accept': '*/*',
                'X-Requested-With': 'com.shangc.tiennews.taizhou',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://srv-app.taizhou.com.cn/luckdraw/',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': '',
            }
            c_params = {
                'accountId': self.account,
                'sessionId': self.session,
            }
            c_r = requests.get('https://srv-app.taizhou.com.cn/tzrb/user/loginWC', params=c_params, headers=c_headers)
            jsessionid = c_r.cookies
            cookies_dict = jsessionid.get_dict()
            for k, y in cookies_dict.items():
                JSESSIONID = f'{k}={y}'
                self.s_JSESSIONID = JSESSIONID
            url = 'https://srv-app.taizhou.com.cn/tzrb/userAwardRecordUpgrade/saveUpdate'
            headers = {
                'Host': 'srv-app.taizhou.com.cn',
                'Connection': 'keep-alive',
                'Content-Length': '63',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app',
                'Content-type': 'application/x-www-form-urlencoded',
                'Accept': '*/*',
                'Origin': 'https://srv-app.taizhou.com.cn',
                'X-Requested-With': 'com.shangc.tiennews.taizhou',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://srv-app.taizhou.com.cn/luckdraw-ra-1/',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': self.s_JSESSIONID,
            }
            data = {
                'activityId': '67',
                'sessionId':'undefined',
                'sig':'undefined',
                'token':'undefined'
            }
            r = requests.post(url, headers=headers, data=data)
            if '成功' in r.json()['message']:
                xx = f'✅抽奖成功'
                st.write(xx)
                self.msg += xx + '\n'
            elif '明天' in r.json()['message']:
                xx = f'❌{r.json()["message"]}'
                st.write(xx)
                self.msg += xx + '\n'
            else:
                xx = f'⛔️{r.json()["message"]}'
                st.write(xx)
                self.msg += xx + '\n'
            jl_headers = {
                'Host': 'srv-app.taizhou.com.cn',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app',
                'Accept': '*/*',
                'X-Requested-With': 'com.shangc.tiennews.taizhou',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://srv-app.taizhou.com.cn/luckdraw/',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': self.s_JSESSIONID,
            }
            jl_params = {
                'pageSize': '10',
                'pageNum': '1',
                'activityId': '67',
            }
            jl_r = requests.get('https://srv-app.taizhou.com.cn/tzrb/userAwardRecordUpgrade/pageList', params=jl_params, headers=jl_headers)
            if '成功' in jl_r.json()['message']:
                jl_list = jl_r.json()['data']['records']
                xx = '🎁抽奖记录🎁'
                st.write(xx)
                self.msg += xx + '\n'
                for i in jl_list:
                    xx = f'⏰{i["createTime"]}: {i["awardName"]}'
                    st.write(xx)
            else:
                send("🔔原神启动", self.msg)
        except Exception as e:
            st.write(e)


def main():
    logs = log()
    logs.dllog()




if __name__ == '__main__':
    markdown_text = """
# 望潮阅读有礼阅读程序
"""
    st.markdown(markdown_text)
    wc = st.text_input("请输入变量值，变量格式：密码#手机号", "")
    if st.button("执行操作"):
        if wc:
            st.write("您输入的变量值是:", wc)
        else: st.write("您输入的ck有误，请重新输入。")
    if not wc: st.stop()
    main()
    st.write = partial(st.write, flush=True)
    token = wc
    cks = token.split("&")
    st.write("🔔检测到{}个ck记录\n🔔".format(len(cks)))
    for ck_all in cks:
        ck = ck_all.split("#")
        wc = Ghdy(ck)
        zh=ck[1]
        st.write(f"\n\n开始执行   {zh}  \n==============================================================")
        wc.login()
        wc.get_id()
        wc.look()
        wc.chou()