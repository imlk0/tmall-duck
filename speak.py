import re
import sys
import json
import base64
import time
import requests
import os
import time


def do_tasks(config, tasks):
    for task in tasks:
        if not task['finished']:
            text = re.match(r'对我说 “(.*)”', task['content']).group(1)
            speak(config, '天猫精灵')
            time.sleep(1)
            speak(config, text)
            time.sleep(1)


def speak(config, text: str):
    file = '/tmp/duck_clock_in.mp3'
    tss(config, text, file)
    os.system('mpg123 {}'.format(file))


# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
PER = 0
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 3

CUID = "123456PYTHON"


def fetch_token(api_key, secret_key):
    params = {'grant_type': 'client_credentials',
              'client_id': api_key,
              'client_secret': secret_key}
    resp = requests.get('http://openapi.baidu.com/oauth/2.0/token', params)
    result = resp.json()
    return result['access_token']


def tss(config, text, path):
    token = fetch_token(config['api_key'], config['secret_key'])
    params = {'tok': token, 'tex': text, 'per': PER, 'spd': SPD, 'pit': PIT,
              'vol': VOL, 'aue': AUE, 'cuid': CUID, 'lan': 'zh', 'ctp': 1}
    resp = requests.get('http://tsn.baidu.com/text2audio', params)
    content = resp.content
    with open(path, 'wb') as f:
        f.write(content)
