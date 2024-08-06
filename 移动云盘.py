# 软件：中国移动云盘
# 功能：签到 每日任务  新增果园任务
# 抓包 Cookie：任意Authorization
# Draw = 1 抽奖次数，每天首次免费， 每天可抽次数50，draw=1，只会抽奖一次
# num = 15 摇一摇，戳一戳次数
# ------------------------------
#
# 每日任务
# 先自行上传一个文件，抓/richlifeApp/devapp/IUploadAndDownload请求体中parentCatalogID的值，这是上传到哪个磁盘的id，不填默认根目录
# 先开抓包，进app，mnote.caiyun.feixin.10086.cn/noteServer/api/authTokenRefresh.do，抓这个，，请求体中authToken的值
# --------------新增任务-----------------
# 果园任务
# 水滴收取，签到，浇水，任务列表上传图片和视频暂时不做

# 云朵大作战，每月首次获得50云朵，每天3次免费次数，每月前2000名获得奖励
# 格式 ydypCk = Authorization值#手机号#authToken的值
# 定时：0 0 0 * * *
# 作者: 木兮
import os
import random
import re
import time

import requests

cookies = os.getenv("ydypCk")
ua = 'Mozilla/5.0 (Linux; Android 11; M2012K10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36 MCloudApp/10.0.1'
parent_catalogid = ''  # 上传文件的父文件夹id，不填默认根目录

draw = 1  # 抽奖次数，首次麻烦
num = 15  # 摇一摇戳一戳次数


class YP:
    def __init__(self, cookie):
        self.token = None
        self.jwtToken = None
        self.notebook_id = None
        self.note_token = None
        self.note_auth = None

        self.timestamp = str(int(round(time.time() * 1000)))
        self.cookies = {'sensors_stay_time': self.timestamp}
        self.Authorization = cookie.split("#")[0]
        self.account = cookie.split("#")[1]
        self.auth_token = cookie.split("#")[2]
        self.fruit_url = 'https://happy.mail.10086.cn/jsp/cn/garden/'

        self.jwtHeaders = {
            'User-Agent': ua,
            'Accept': '*/*',
            'Host': 'caiyun.feixin.10086.cn:7071',
        }
        self.treeHeaders = {
            'Host': 'happy.mail.10086.cn',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': ua,
            'Referer': 'https://happy.mail.10086.cn/jsp/cn/garden/wap/index.html?sourceid=1003',
            'Cookie': '',
        }

    def run(self):
        try:
            self.sso()
            self.jwt()
            self.signin_status()
            self.click()
            print(f'\n---每日任务---')
            self.get_tasklist()
            print(f'\n---云朵大作战---')
            self.cloud_game()
            print(f'\n---果园任务---')
            self.fruitLogin()
            print(f'\n---公众号任务---')
            self.wxsign()
            self.shake()
            self.surplus_num()
            self.receive()
        except Exception as e:
            print(f"出现异常: {e}")
            # 处理其他异常

    def send_request(self, url, headers, data=None, method='GET', cookies=None):
        with requests.Session() as session:
            session.headers.update(headers)
            if cookies is not None:
                session.cookies.update(cookies)

            try:
                if method == 'GET':
                    response = session.get(url, timeout = 5)
                elif method == 'POST':
                    response = session.post(url, json = data, timeout = 10)
                else:
                    raise ValueError('Invalid HTTP method.')

                response.raise_for_status()
                return response.json()

            except requests.Timeout as e:
                print("请求超时:", str(e))

            except requests.RequestException as e:
                print("请求错误:", str(e))

            except Exception as e:
                print("其他错误:", str(e))

    # 随机延迟默认1-1.5s
    def sleep(self, min_delay=1, max_delay=1.5):
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    # 刷新令牌
    def sso(self):
        url = 'https://orches.yun.139.com/orchestration/auth-rebuild/token/v1.0/querySpecToken'
        headers = {
            'Authorization': self.Authorization,
            'User-Agent': ua,
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'orches.yun.139.com'
        }
        data = {"account": self.account, "toSourceId": "001005"}
        return_data = self.send_request(url, headers = headers, data = data, method = 'POST')
        self.sleep()
        if 'success' in return_data:
            if return_data['success']:
                self.token = return_data['data']['token']
            else:
                print(return_data['message'])
                raise Exception("验证未通过")
        else:
            raise Exception("出现未知错误")

    # 获取jwttoken
    def jwt(self):
        url = f"https://caiyun.feixin.10086.cn:7071/portal/auth/tyrzLogin.action?ssoToken={self.token}"
        return_data = self.send_request(url = url, headers = self.jwtHeaders, method = 'POST')
        self.sleep()
        if return_data['code'] != 0:
            return print(return_data['msg'])
        self.jwtToken = return_data['result']['token']
        self.jwtHeaders['jwtToken'] = self.jwtToken
        self.cookies['jwtToken'] = self.jwtToken

    # 签到查询
    def signin_status(self):
        url = 'https://caiyun.feixin.10086.cn/market/signin/page/info?client=app'
        return_data = self.send_request(url, headers = self.jwtHeaders, cookies = self.cookies)
        self.sleep()
        if return_data['msg'] == 'success':
            today_sign_in = return_data['result'].get('todaySignIn', False)

            if today_sign_in:
                return print('已经签到了')
            else:
                print('未签到，去签到')
                config_url = 'https://caiyun.feixin.10086.cn/market/manager/commonMarketconfig/getByMarketRuleName?marketName=sign_in_3'
                config_data = self.send_request(config_url, headers = self.jwtHeaders, cookies = self.cookies)

                if config_data['msg'] == 'success':
                    print('签到成功')
                else:
                    print(config_data['msg'])
        else:
            print(return_data['msg'])

    # 戳一下
    def click(self):
        url = "https://caiyun.feixin.10086.cn/market/signin/task/click?key=task&id=319"
        for _ in range(num):
            return_data = self.send_request(url, headers = self.jwtHeaders, cookies = self.cookies)
            time.sleep(0.2)
            if 'result' in return_data:
                print(f'{return_data["result"]}')
            elif return_data.get('msg') == 'success':
                print('未获得')

    # 刷新笔记token
    def refresh_notetoken(self):
        url = 'http://mnote.caiyun.feixin.10086.cn/noteServer/api/authTokenRefresh.do'
        payload = {
            "authToken": self.auth_token,
            "userPhone": self.account
        }
        headers = {
            'X-Tingyun-Id': 'p35OnrDoP8k;c=2;r=1122634489;u=43ee994e8c3a6057970124db00b2442c::8B3D3F05462B6E4C',
            'Charset': 'UTF-8',
            'Connection': 'Keep-Alive',
            'User-Agent': 'mobile',
            'APP_CP': 'android',
            'CP_VERSION': '3.2.0',
            'x-huawei-channelsrc': '10001400',
            'Host': 'mnote.caiyun.feixin.10086.cn',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept-Encoding': 'gzip'
        }

        try:
            response = requests.post(url, headers = headers, json = payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print('出错了:', e)
            return

        self.note_token = response.headers.get('NOTE_TOKEN')
        self.note_auth = response.headers.get('APP_AUTH')

    # 任务列表
    def get_tasklist(self):
        url = 'https://caiyun.feixin.10086.cn/market/signin/task/taskList?marketname=sign_in_3'
        return_data = self.send_request(url, headers = self.jwtHeaders, cookies = self.cookies)
        self.sleep()
        task_list = return_data.get('result', {}).get('day', [])

        for value in task_list:
            task_id = value.get('id')
            if task_id == 404:
                continue
            task_name = value.get('name')
            task_status = value.get('button', {}).get('out', {}).get('text')

            if task_status == '已完成':
                print(f'已完成: {task_name}')
                continue
            print(f'去完成: {task_name}')
            self.day_task(task_id)

    def day_task(self, task_id):
        url = f'https://caiyun.feixin.10086.cn/market/signin/task/click?key=task&id={task_id}'
        return_data = self.send_request(url, headers = self.jwtHeaders, cookies = self.cookies)
        self.sleep()
        if return_data['msg'] != 'success':
            return print(return_data['msg'])
        if task_id == 106:
            print('开始上传文件，默认0kb')
            self.updata_file()
        elif task_id == 107:
            self.refresh_notetoken()
            print('获取默认笔记id')
            note_url = 'http://mnote.caiyun.feixin.10086.cn/noteServer/api/syncNotebookV3.do'
            headers = {
                'X-Tingyun-Id': 'p35OnrDoP8k;c=2;r=1122634489;u=43ee994e8c3a6057970124db00b2442c::8B3D3F05462B6E4C',
                'Charset': 'UTF-8',
                'Connection': 'Keep-Alive',
                'User-Agent': 'mobile',
                'APP_CP': 'android',
                'CP_VERSION': '3.2.0',
                'x-huawei-channelsrc': '10001400',
                'APP_NUMBER': self.account,
                'APP_AUTH': self.note_auth,
                'NOTE_TOKEN': self.note_token,
                'Host': 'mnote.caiyun.feixin.10086.cn',
                'Content-Type': 'application/json; charset=UTF-8',
                'Accept': '*/*'
            }
            payload = {
                "addNotebooks": [],
                "delNotebooks": [],
                "notebookRefs": [],
                "updateNotebooks": []
            }
            return_data = self.send_request(url = note_url, headers = headers, data = payload,
                                            method = 'POST')
            if return_data is None:
                return print('出错了')
            self.notebook_id = return_data['notebooks'][0]['notebookId']
            print('开始创建笔记')
            self.create_note(headers)

    def updata_file(self):
        url = 'http://ose.caiyun.feixin.10086.cn/richlifeApp/devapp/IUploadAndDownload'
        headers = {
            'x-huawei-uploadSrc': '1',
            'x-ClientOprType': '11',
            'Connection': 'keep-alive',
            'x-NetType': '6',
            'x-DeviceInfo': '6|127.0.0.1|1|10.0.1|Xiaomi|M2012K10C|CB63218727431865A48E691BFFDB49A1|02-00-00-00-00-00|android 11|1080X2272|zh||||032|',
            'x-huawei-channelSrc': '10000023',
            'x-MM-Source': '032',
            'x-SvcType': '1',
            'APP_NUMBER': self.account,
            'Authorization': self.Authorization,
            'X-Tingyun-Id': 'p35OnrDoP8k;c=2;r=1955442920;u=43ee994e8c3a6057970124db00b2442c::8B3D3F05462B6E4C',
            'Host': 'ose.caiyun.feixin.10086.cn',
            'User-Agent': 'okhttp/3.11.0',
            'Content-Type': 'application/xml; charset=UTF-8',
            'Accept': '*/*'
        }
        payload = '''
                            <pcUploadFileRequest>
                                <ownerMSISDN>{phone}</ownerMSISDN>
                                <fileCount>1</fileCount>
                                <totalSize>1</totalSize>
                                <uploadContentList length="1">
                                    <uploadContentInfo>
                                        <comlexFlag>0</comlexFlag>
                                        <contentDesc><![CDATA[]]></contentDesc>
                                        <contentName><![CDATA[000000.txt]]></contentName>
                                        <contentSize>1</contentSize>
                                        <contentTAGList></contentTAGList>
                                        <digest>C4CA4238A0B923820DCC509A6F75849B</digest>
                                        <exif/>
                                        <fileEtag>0</fileEtag>
                                        <fileVersion>0</fileVersion>
                                        <updateContentID></updateContentID>
                                    </uploadContentInfo>
                                </uploadContentList>
                                <newCatalogName></newCatalogName>
                                <parentCatalogID>{parent_catalogid}</parentCatalogID>
                                <operation>0</operation>
                                <path></path>
                                <manualRename>2</manualRename>
                                <autoCreatePath length="0"/>
                                <tagID></tagID>
                                <tagType></tagType>
                            </pcUploadFileRequest>
                        '''.format(phone = self.account, parent_catalogid = parent_catalogid)

        response = requests.post(url = url, headers = headers, data = payload)
        if response is None:
            return
        if response.status_code != 200:
            return print('上传失败')
        print('上传成功，快去领取奖励啦')

    def create_note(self, headers):
        note_id = self.get_note_id(32)  # 获取随机笔记id
        createtime = str(int(round(time.time() * 1000)))
        time.sleep(3)
        updatetime = str(int(round(time.time() * 1000)))
        note_url = 'http://mnote.caiyun.feixin.10086.cn/noteServer/api/createNote.do'
        payload = {
            "archived": 0,
            "attachmentdir": note_id,
            "attachmentdirid": "",
            "attachments": [],
            "audioInfo": {
                "audioDuration": 0,
                "audioSize": 0,
                "audioStatus": 0
            },
            "contentid": "",
            "contents": [{
                "contentid": 0,
                "data": "<font size=\"3\">000000</font>",
                "noteId": note_id,
                "sortOrder": 0,
                "type": "RICHTEXT"
            }],
            "cp": "",
            "createtime": createtime,
            "description": "android",
            "expands": {
                "noteType": 0
            },
            "latlng": "",
            "location": "",
            "noteid": note_id,
            "notestatus": 0,
            "remindtime": "",
            "remindtype": 1,
            "revision": "1",
            "sharecount": "0",
            "sharestatus": "0",
            "system": "mobile",
            "tags": [{
                "id": self.notebook_id,
                "orderIndex": "0",
                "text": "默认笔记本"
            }],
            "title": "00000",
            "topmost": "0",
            "updatetime": updatetime,
            "userphone": self.account,
            "version": "1.00",
            "visitTime": ""
        }
        return_data = requests.post(note_url, headers = headers, json = payload)
        if return_data.status_code == 200:
            print('创建笔记成功,快去领取奖励啦')
        else:
            print('创建失败')

    def get_note_id(self, length):
        characters = '19f3a063d67e4694ca63a4227ec9a94a19088404f9a28084e3e486b928039a299bf756ebc77aa4f6bfa250308ec6a8be8b63b5271a00350d136d117b8a72f39c5bd15cdfd350cba4271dc797f15412d9f269e666aea5039f5049d00739b320bb9e858504ca6c1426941ec82f22679b3f4b9d140b27c6e91286381cceadb2788529fc6125d74c96e0c820b308a587f941ffd7c9cc35b4a80d33e41ed739d893b61716bd66e77464fa1c6ab9d1422409ae7615b09660acc8e1eacc6cca7069b7979ec326003fe025831704c9df1211d3ed2b3bd97d49887200ce23baaa70be048f9ef875317c81ed2b72234b31fb20dd11e95a00f32480d03ffdbd226cb88f0746233a1f27766dba55e7b8dd59d2fc788eaa897a01db3f3593332574d0a66a0bf3e5bd4baaf46baf0d98a2cb6206c0386ffcce7c3aef88e3fda7429cc2abf91250ae8a269a9a160c04f34192c7dcc25fff37d4a8bbdc0fa0eb10864b11d40d0ec55bba0b41441873f3e11831357ab44b96cab3b69bcbf43da1096c7fc830a63b91713425cb5613130d1f5ebcfd74f71f9febaee7c895271de4e49954ffc6748b825fba0de16e38034c0fccd3e83d064045c9cb27d6a61a23faf07021740f5f273afae38721edd08905ee8eca4ca0d72cda4a076c443087cd14a04e14d53cb581efc276b6f7cfe747841536d0d3fea1b9aba07868286fdd76802964645ca4fed889d067497ef56ccb1606ac12fdec94b0e406a01b1aaf42948df326d7f219ed1a5ae297b233bb0112c764c756267cbe1b0bcbc0b25a38bc9aa2936bd16b4cd4ff0a7e4cd1039110a962dbb2b73b89ce56e3097bbeedb90c257c258731e581d97819923ac983d639c6576c2186d65cdb11b3359054df4b546810a7f71decb22649d295cad7030e458562b610b4147676adbb143431e54dbbae5bc67c290fc70911fc1c5f82b1f681c23751572b30a35c31d060562cd92944fa973c8b5cf2fa008b52c1cbd86970cae9476446f3e41871de8d9f6112db94b05e5dc7ea0a942a9daf145ac8e487d3d5cba7cea145680efc64794d43dd15c5062b81e1cda7bf278b9bc4e1b8955846e6bc4b6a61c28f831f81b2270289e5a8a677c3141ddc9868129060c0c3b5ef507fbd46c004f6de346332ef7f05c0094215eae1217ee7c13c8dca6d174cfb49c716dd42903bb4b02d823b5f1ff93c3f88768251b56cc'
        note_id = ''.join(random.choice(characters) for _ in range(length))
        return note_id

    # 公众号签到
    def wxsign(self):
        url = 'https://caiyun.feixin.10086.cn/market/playoffic/followSignInfo?isWx=true'
        return_data = self.send_request(url, headers = self.jwtHeaders, cookies = self.cookies)
        self.sleep()
        if return_data['msg'] != 'success':
            return print(return_data['msg'])
        if not return_data['result'].get('todaySignIn'):
            return print('签到失败')
        return print('签到成功')

    # 摇一摇
    def shake(self):
        url = "https://caiyun.feixin.10086.cn:7071/market/shake-server/shake/shakeIt?flag=1"
        for _ in range(num):
            return_data = self.send_request(url = url, cookies = self.cookies, headers = self.jwtHeaders,
                                            method = 'POST')
            time.sleep(1)
            shake_prize_config = return_data["result"].get("shakePrizeconfig")
            if shake_prize_config is not None:
                print("⭕摇一摇成功，获得：" + str(shake_prize_config["name"]))
            elif shake_prize_config is None:
                print("未摇中")
            else:
                print("出错了")

    # 查询剩余抽奖次数
    def surplus_num(self):
        draw_info_url = 'https://caiyun.feixin.10086.cn/market/playoffic/drawInfo'
        draw_url = "https://caiyun.feixin.10086.cn/market/playoffic/draw"

        draw_info_data = self.send_request(draw_info_url, headers = self.jwtHeaders)
        self.sleep()
        if draw_info_data.get('msg') == 'success':
            num1 = draw_info_data['result'].get('surplusNumber', 0)
            print(f'---剩余抽奖次数{num1}---')
            if num1 > 50 - draw:
                for _ in range(draw):
                    draw_data = self.send_request(url = draw_url, headers = self.jwtHeaders)
                    self.sleep()
                    if draw_data.get("code") == 0:
                        prize_name = draw_data["result"].get("prizeName", "")
                        print("⭕ 抽奖成功，获得：" + prize_name)
                    else:
                        print("❌ 抽奖失败")
            else:
                pass
        else:
            print(draw_info_data.get('msg'))

    # 果园专区
    def fruitLogin(self):
        refreshUrl = 'https://aas.caiyun.feixin.10086.cn/tellin/querySpecToken.do'
        headers = {
            'x-huawei-channelSrc': '10000023',
            'APP_NUMBER': self.account,
            'x-ExpRoute-Code': f'routeCode={self.account},type=10',
            'Authorization': self.Authorization,
            'Host': 'aas.caiyun.feixin.10086.cn',
            'User-Agent': 'okhttp/3.11.0',
            'Content-Type': 'application/xml; charset=UTF-8',
            'Accept': '*/*',
        }
        payload = f"<root>\r\n   <account>{self.account}</account>\r\n   <toSourceId>001003</toSourceId>\r\n</root>"
        try:
            refreshData = requests.request("POST", refreshUrl, headers = headers, data = payload).text
            # 使用正则表达式提取token
            pattern = r'<token>(.*?)</token>'
            match = re.search(pattern, refreshData)

            if match:
                token = match.group(1)
                print("--果园专区token刷新成功")
                self.sleep()
                login_info_url = f'{self.fruit_url}login/caiyunsso.do?token={token}&account={self.account}&targetSourceId=001208&sourceid=1003&enableShare=1'
                headers = {
                    'Host': 'happy.mail.10086.cn',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': ua,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Referer': 'https://caiyun.feixin.10086.cn:7071/',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
                }
                loginInfoData = requests.request("GET", login_info_url, headers = headers)
                treeCookie = loginInfoData.request.headers['Cookie']
                self.treeHeaders['cookie'] = treeCookie

                do_login_url = f'{self.fruit_url}login/userinfo.do'
                doLoginData = self.send_request(do_login_url, headers = self.treeHeaders)
                if doLoginData.get('result', {}).get('islogin') != 1:
                    return print('果园登录失败')
                # 去做果园任务
                self.fruitTask()
            else:
                print("果园专区token刷新失败")
        except requests.RequestException as e:
            print("发生网络请求错误:", e)

    # 任务查询
    def fruitTask(self):
        try:
            # 签到任务
            check_sign_data = self.send_request(f'{self.fruit_url}task/checkinInfo.do', headers = self.treeHeaders)
            if check_sign_data.get('success'):
                today_checkin = check_sign_data.get('result', {}).get('todayCheckin', 0)
                if today_checkin == 1:
                    print('果园今日已签到')
                else:
                    checkin_data = self.send_request(f'{self.fruit_url}task/checkin.do', headers = self.treeHeaders)
                    if checkin_data.get('result', {}).get('code', '') == 1:
                        print('果园签到成功')
                    self.sleep()
                    water_data = self.send_request(f'{self.fruit_url}user/clickCartoon.do?cartoonType=widget',
                                                   headers = self.treeHeaders)
                    given_water = water_data.get('result', {}).get('given', 0)
                    print(f'领取每日水滴: {given_water}')
            else:
                print('果园签到查询失败:', check_sign_data.get('msg', ''))

            # 获取任务列表
            task_list_data = self.send_request(f'{self.fruit_url}task/taskList.do?clientType=PE',
                                               headers = self.treeHeaders)
            task_state_data = self.send_request(f'{self.fruit_url}task/taskState.do', headers = self.treeHeaders)
            task_state_result = task_state_data.get('result', [])

            task_list = task_list_data.get('result', [])

            for task in task_list:
                task_id = task.get('taskId', '')
                task_name = task.get('taskName', '')
                water_num = task.get('waterNum', 0)
                if task_id == 2002 or task_id == 2003:
                    continue

                task_state = next(
                    (state.get('taskState', 0) for state in task_state_result if state.get('taskId') == task_id), 0)

                if task_state == 2:
                    print(f'已完成: {task_name}')
                else:
                    self.do_fruit_task(task_name, task_id, water_num)

            # 果树信息
            self.tree_info()

        except Exception as e:
            print(f"发生错误：{e}")

    # 做任务
    def do_fruit_task(self, task_name, task_id, water_num):
        try:
            print(f'去完成: {task_name}')
            do_task_url = f'{self.fruit_url}task/doTask.do?taskId={task_id}'
            do_task_data = self.send_request(do_task_url, headers = self.treeHeaders)

            if do_task_data.get('success'):
                get_water_url = f'{self.fruit_url}task/givenWater.do?taskId={task_id}'
                get_water_data = self.send_request(get_water_url, headers = self.treeHeaders)

                if get_water_data.get('success'):
                    print(f'已完成任务获得水滴: {water_num}')
                else:
                    print(f'领取失败: {get_water_data.get("msg", "")}')
            else:
                print(f'参与任务失败: {do_task_data.get("msg", "")}')
        except Exception as e:
            print(f"发生错误：{e}")

    # 果树信息
    def tree_info(self):
        try:
            treeinfo_url = f'{self.fruit_url}user/treeInfo.do'
            treeinfo_data = self.send_request(treeinfo_url, headers = self.treeHeaders)

            if not treeinfo_data.get('success'):
                error_message = treeinfo_data.get('msg', '获取果园任务列表失败')
                print(error_message)
            else:
                collect_water = treeinfo_data.get('result', {}).get('collectWater', 0)
                tree_level = treeinfo_data.get('result', {}).get('treeLevel', 0)
                print(f'当前小树等级: {tree_level} 剩余水滴: {collect_water}')

                watering_amount = collect_water // 20  # 计算需要浇水的次数
                watering_url = f'{self.fruit_url}user/watering.do?isFast=0'
                if watering_amount > 0:
                    for _ in range(watering_amount):
                        watering_data = self.send_request(watering_url, headers = self.treeHeaders)
                        if watering_data.get('success'):
                            print('浇水成功')
                            self.sleep()
        except Exception as e:
            print(f"发生错误：{e}")

    # 云朵大作战
    def cloud_game(self):
        game_info_url = 'https://caiyun.feixin.10086.cn/market/signin/hecheng1T/info?op=info'
        bigin_url = 'https://caiyun.feixin.10086.cn/market/signin/hecheng1T/beinvite'
        end_url = 'https://caiyun.feixin.10086.cn/market/signin/hecheng1T/finish?flag=true'
        try:
            game_info_data = self.send_request(game_info_url, headers = self.jwtHeaders, cookies = self.cookies)
            if game_info_data and game_info_data.get('code', -1) == 0:
                currnum = game_info_data.get('result', {}).get('info', {}).get('curr', 0)
                count = game_info_data.get('result', {}).get('history', {}).get('0', {}).get('count', '')
                rank = game_info_data.get('result', {}).get('history', {}).get('0', {}).get('rank', '')

                print(f'今日剩余游戏次数: {currnum}\n本月排名: {rank}    合成次数: {count}')

                for _ in range(currnum):
                    self.send_request(bigin_url, headers = self.jwtHeaders, cookies = self.cookies)
                    print('开始游戏,等待2分钟完成游戏')
                    time.sleep(120)
                    end_data = self.send_request(end_url, headers = self.jwtHeaders, cookies = self.cookies)
                    if end_data and end_data.get('code', -1) == 0:
                        print('游戏成功')
            else:
                print("获取游戏信息失败")
        except Exception as e:
            print(f"出现异常: {e}")

    # 领取云朵
    def receive(self):
        url = "https://caiyun.feixin.10086.cn/market/signin/page/receive"
        return_data = self.send_request(url, headers = self.jwtHeaders, cookies = self.cookies)
        if return_data['msg'] == 'success':
            receive_amount = return_data["result"].get("receive", "")
            total_amount = return_data["result"].get("total", "")
            print(f'当前待领取:{receive_amount}云朵')
            print(f'当前云朵数量:{total_amount}云朵')
        else:
            print(return_data['msg'])


if __name__ == "__main__":
    cookies = cookies.split("@")
    ydypqd = f"移动硬盘共获取到{len(cookies)}个账号"
    print(ydypqd)

    for i, cookie in enumerate(cookies, start = 1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        YP(cookie).run()
        print("\n随机等待5-10s进行下一个账号")
        time.sleep(random.randint(5, 10))
