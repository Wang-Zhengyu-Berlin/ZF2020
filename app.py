from flask import Flask
from flask import Flask, request, jsonify
import getpass
import time
import requests
from bs4 import BeautifulSoup as soup
from hex2b64 import HB64
import RSAJS
import urllib
import sys
import re
import json
import datetime
app = Flask(__name__)

# app.config.update(DEBUG=True)
@app.route('/', methods=['POST', 'GET'])
def get_score():
    s = requests.session()
    times = int(time.time() * 1000)
    user = str(request.args.get('user'))
    passwd = str(request.args.get('passwd'))
    xnm = str(request.args.get('xnm'))
    xqm = str(request.args.get('xqm'))
    if xnm == '全部':
        xnm = ''

    if xqm == '1':
        xqm = 3
    elif xqm == '2':
        xqm = 12
    else:
        xqm = ''

    print(xqm)
    url = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?time=' + str(times)
    res = s.get(url)

    csrftoken = soup(res.text, 'html.parser').find('input', attrs={'id': 'csrftoken'}).attrs['value']
    url2 = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time=' + str(times)
    r = s.get(url2)
    pub = r.json()
    print(pub)

    exponent = HB64().b642hex(pub['exponent'])
    modulus = HB64().b642hex(pub['modulus'])
    rsa = RSAJS.RSAKey()
    rsa.setPublic(modulus, exponent)
    cry_data = rsa.encrypt(passwd)
    process_public = HB64().hex2b64(cry_data)
    print(process_public)

    url3 = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?time=' + str(times)
    header3 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '486',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jwxt.nytdc.edu.cn',
        'Origin': 'http://jwxt.nytdc.edu.cn',
        'Referer': 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=' + str(times),
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
    }
    data3 = {
        'csrftoken': csrftoken,
        'mm': process_public,
        'mm': process_public,
        'yhm': user
    }
    res3 = s.post(url3, data=data3, headers=header3)
    res_success = soup(res3.text, 'lxml')
    Cookie = res3.request.headers['cookie']
    ppot = r'用户名或密码不正确'
    if re.findall(ppot, str(res_success)):
        print('用户名或密码错误,请查验..')
        response = 'failed'
    else:
        print("登陆成功")
        url4 = "http://jwxt.nytdc.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N100801&su={}".format(user)
        payload = 'xh_id={}&xnm={}&xqm={}&_search=false&nd=1600489869289&queryModel.showCount=999&queryModel.currentPage=1&queryModel.sortName=&queryModel.sortOrder=asc&time=0'.format(
            user, xnm, xqm, times)
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '157',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': Cookie,
            'Host': 'jwxt.nytdc.edu.cn',
            'Origin': 'http://jwxt.nytdc.edu.cn',
            'Referer': 'http://jwxt.nytdc.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su={}'.format(
                user),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url4, headers=headers, data=payload).json()

    print(response)
    return response


@app.route('/get_lesson', methods=['POST', 'GET'])
def get_lesson():
    s = requests.session()
    times = int(time.time() * 1000)
    user = str(request.args.get('user'))
    passwd = str(request.args.get('passwd'))
    xnm = str(request.args.get('xnm'))
    xqm = str(request.args.get('xqm'))

    if xqm == '1':
        xqm = 3
    else:
        xqm = ''
    # print(self.xqm)
    url = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?time=' + str(times)
    res = s.get(url)

    csrftoken = soup(res.text, 'html.parser').find('input', attrs={'id': 'csrftoken'}).attrs['value']
    url2 = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time=' + str(times)
    r = s.get(url2)
    pub = r.json()
    print(pub)

    exponent = HB64().b642hex(pub['exponent'])
    modulus = HB64().b642hex(pub['modulus'])
    rsa = RSAJS.RSAKey()
    rsa.setPublic(modulus, exponent)
    cry_data = rsa.encrypt(passwd)
    process_public = HB64().hex2b64(cry_data)
    print(process_public)

    url3 = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?time=' + str(times)
    header3 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '486',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jwxt.nytdc.edu.cn',
        'Origin': 'http://jwxt.nytdc.edu.cn',
        'Referer': 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=' + str(times),
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
    }
    data3 = {
        'csrftoken': csrftoken,
        'mm': process_public,
        'mm': process_public,
        'yhm': user
    }
    res3 = s.post(url3, data=data3, headers=header3)
    res_success = soup(res3.text, 'lxml')
    Cookie = res3.request.headers['cookie']
    ppot = r'用户名或密码不正确'
    if re.findall(ppot, str(res_success)):
        print('用户名或密码错误,请查验..')
        response = 'failed'
    else:
        print("登陆成功")
        url4 = "http://jwxt.nytdc.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N100801&su={}".format(user)
        payload = 'xnm=2020&xqm=3'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '157',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': Cookie,
            'Host': 'jwxt.nytdc.edu.cn',
            'Origin': 'http://jwxt.nytdc.edu.cn',
            'Referer': 'http://jwxt.nytdc.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su={}'.format(
                user),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url4, headers=headers, data=payload).json()

    print(response)
    return response


@app.route('/get_today_lesson', methods=['POST', 'GET'])
def get_today_lesson():
    s = requests.session()
    times = int(time.time() * 1000)
    user = str(request.args.get('user'))
    passwd = str(request.args.get('passwd'))
    xnm = str(request.args.get('xnm'))
    xqm = str(request.args.get('xqm'))

    if xqm == '1':
        xqm = 3
    else:
        xqm = ''
    # print(self.xqm)
    url = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?time=' + str(times)
    res = s.get(url)

    csrftoken = soup(res.text, 'html.parser').find('input', attrs={'id': 'csrftoken'}).attrs['value']
    url2 = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time=' + str(times)
    r = s.get(url2)
    pub = r.json()
    print(pub)

    exponent = HB64().b642hex(pub['exponent'])
    modulus = HB64().b642hex(pub['modulus'])
    rsa = RSAJS.RSAKey()
    rsa.setPublic(modulus, exponent)
    cry_data = rsa.encrypt(passwd)
    process_public = HB64().hex2b64(cry_data)
    print(process_public)

    url3 = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?time=' + str(times)
    header3 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '486',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jwxt.nytdc.edu.cn',
        'Origin': 'http://jwxt.nytdc.edu.cn',
        'Referer': 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=' + str(times),
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
    }
    data3 = {
        'csrftoken': csrftoken,
        'mm': process_public,
        'mm': process_public,
        'yhm': user
    }
    res3 = s.post(url3, data=data3, headers=header3)
    res_success = soup(res3.text, 'lxml')
    Cookie = res3.request.headers['cookie']
    ppot = r'用户名或密码不正确'
    if re.findall(ppot, str(res_success)):
        print('用户名或密码错误,请查验..')
        response = 'failed'
    else:
        print("登陆成功")
        url4 = "http://jwxt.nytdc.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N100801&su={}".format(user)
        payload = 'xnm=2020&xqm=12'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '157',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': Cookie,
            'Host': 'jwxt.nytdc.edu.cn',
            'Origin': 'http://jwxt.nytdc.edu.cn',
            'Referer': 'http://jwxt.nytdc.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su={}'.format(
                user),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url4, headers=headers, data=payload).json()

    print(type(response))
    print()
    weekStr = "星期一星期二星期三星期四星期五星期六星期日"
    weekId = int(time.strftime("%w"))
    pos = (weekId - 1) * 3
    week_name = weekStr[pos: pos + 3]
    print(week_name)
    json_dict = response
    lesson_today = []
    lesson_today_num = {
        "is_week": "Don't Know!",
        "lesson_today_have": 1,
        "lesson_today_is" :[]
    }
    lesson_today_is_out = []
    lesson_info = {}
    lesson_today.append(lesson_today_num)
    is_week = ""
    today_info = datetime.datetime.now().isocalendar()
    # print("今天是：",today_info[1])
    if (today_info[1] % 2 == 0):
        is_week = "单"
    elif (today_info[1] % 2 == 1):
        is_week = "双"
    for item in range(len(json_dict["kbList"])):
        if(str(json_dict["kbList"][item]['xqjmc']) == str(week_name) ):
        # if (str(json_dict["kbList"][item]['xqjmc']) == str('星期二')):
            if (str(json_dict["kbList"][item]["zcd"][-2]) == str(is_week)
                    or str(json_dict["kbList"][item]["zcd"][-2]) == str(8)
                    or str(json_dict["kbList"][item]["zcd"][-2]) == str(7)):
                lesson_info = {"name": "{}".format(json_dict["kbList"][item]["kcmc"]),
                               "jc": "{}".format(json_dict["kbList"][item]["jc"]),
                               "dd": "{}".format(json_dict["kbList"][item]["cdmc"]),
                               "zc": "{}".format(json_dict["kbList"][item]["zcd"]),
                               "xm": "{}".format(json_dict["kbList"][item]["xm"])
                               }
                lesson_today_is_out.append(lesson_info)
    lesson_today[0]['lesson_today_is']= lesson_today_is_out
    # lesson_today.append(lesson_today_is)
    lesson_today[0]['is_week'] = is_week
    lesson_today[0]['lesson_today_have'] = len(lesson_today[0]['lesson_today_is'])
    print(is_week)
    print(lesson_today)
    lesson_today = json.dumps(lesson_today, indent=2, ensure_ascii=False)
    return lesson_today




@app.route('/get_range_lesson',methods=['POST', 'GET'])
def get_range_lesson():
    s = requests.session()
    times = int(time.time() * 1000)
    user = str(request.args.get('user'))
    passwd = str(request.args.get('passwd'))
    xnm = str(request.args.get('xnm'))
    xqm = str(request.args.get('xqm'))
    today = str(request.args.get('today'))
    if xqm == '1':
        xqm = 3
    else:
        xqm = ''
    # print(self.xqm)
    url = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?time=' + str(times)
    res = s.get(url)

    csrftoken = soup(res.text, 'html.parser').find('input', attrs={'id': 'csrftoken'}).attrs['value']
    url2 = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time=' + str(times)

    r = s.get(url2)
    pub = r.json()
    print(pub)

    exponent = HB64().b642hex(pub['exponent'])
    modulus = HB64().b642hex(pub['modulus'])
    rsa = RSAJS.RSAKey()
    rsa.setPublic(modulus, exponent)
    cry_data = rsa.encrypt(passwd)
    process_public = HB64().hex2b64(cry_data)
    print(process_public)

    url3 = 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?time=' + str(times)
    header3 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '486',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jwxt.nytdc.edu.cn',
        'Origin': 'http://jwxt.nytdc.edu.cn',
        'Referer': 'http://jwxt.nytdc.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=' + str(times),
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
    }
    data3 = {
        'csrftoken': csrftoken,
        'mm': process_public,
        'mm': process_public,
        'yhm': user
    }
    res3 = s.post(url3, data=data3, headers=header3)
    res_success = soup(res3.text, 'lxml')
    Cookie = res3.request.headers['cookie']
    ppot = r'用户名或密码不正确'
    if re.findall(ppot, str(res_success)):
        print('用户名或密码错误,请查验..')
        response = 'failed'
    else:
        print("登陆成功")
        url4 = "http://jwxt.nytdc.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N100801&su={}".format(user)
        payload = 'xnm=2020&xqm=12'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '157',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': Cookie,
            'Host': 'jwxt.nytdc.edu.cn',
            'Origin': 'http://jwxt.nytdc.edu.cn',
            'Referer': 'http://jwxt.nytdc.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su={}'.format(
                user),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url4, headers=headers, data=payload).json()


    # print(time)
    # thisTime = "2021-01-28"
    # thisTime = thisTime.replace('-', '/')
    thisTime = time.strptime(today, "%Y-%m-%d")
    # thisTime = time.strptime(thisTime, "%Y-%m-%d")
    print(thisTime.tm_yday)
    print(thisTime)

    is_week_num = ((int(thisTime.tm_yday) - 4) // 7) - 6
    print(is_week_num)
    weekStr = "星期一星期二星期三星期四星期五星期六星期日"
    # weekId = int(time.strftime("%w"))
    pos = (thisTime.tm_wday) * 3
    week_name = weekStr[pos: pos + 3]
    print(week_name)

    json_dict = response
    lesson_today = []
    lesson_today_num = {
        "is_week": "Don't Know!",
        "lesson_today_have": 1
    }
    lesson_today_is_out = []
    lesson_today.append(lesson_today_num)
    is_week = ""
    for item in range(len(json_dict["kbList"])):
        if(str(json_dict["kbList"][item]['xqjmc']) == str(week_name) ):
        # if (str(json_dict["kbList"][item]['xqjmc']) == str('星期二')):
            if (str(json_dict["kbList"][item]["zcd"][-2]) == str(is_week)
                    or str(json_dict["kbList"][item]["zcd"][-2]) == str(8)
                    or str(json_dict["kbList"][item]["zcd"][-2]) == str(7)):
                lesson_info = {"name": "{}".format(json_dict["kbList"][item]["kcmc"]),
                               "jc": "{}".format(json_dict["kbList"][item]["jc"]),
                               "dd": "{}".format(json_dict["kbList"][item]["cdmc"]),
                               "zc": "{}".format(json_dict["kbList"][item]["zcd"]),
                               "xm": "{}".format(json_dict["kbList"][item]["xm"])
                               }
                lesson_today_is_out.append(lesson_info)
    lesson_today[0]['lesson_today_is'] = lesson_today_is_out
    lesson_today[0]['is_week'] = is_week_num
    lesson_today[0]['lesson_today_have'] = len(lesson_today[0]['lesson_today_is'])
    print(is_week)
    print(lesson_today)
    lesson_today = json.dumps(lesson_today, indent=2, ensure_ascii=False)
    return lesson_today

if __name__ == '__main__':
    app.run()
