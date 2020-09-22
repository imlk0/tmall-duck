# coding=utf-8

from time import strftime, localtime
import json
import fetch
import notify
import speak
import os

print("--------- 触发打卡 ---------")
print("当前系统时间：{}".format(strftime('%Y-%m-%d %H:%M:%S', localtime())))

config_private_file = './config_private.json'
config_file = './config.json'
if os.path.exists(config_private_file):
    config = json.load(open(config_private_file, 'r'))
else:
    config = json.load(open(config_file, 'r'))

tasks_info = fetch.fetch_tasks_info(config['taobao'])
# finished_all, days_of_checkin, schedule, tasks, ele_tasks.screenshot_as_png
if tasks_info[3] is None:
    print("获取任务信息失败")
else:
    msg = notify.build_nitofy_msg(tasks_info)
    print(msg)

notify.notify(config['weixin'], tasks_info)


# 如果今天需要打卡
if not tasks_info[0]:
    print("发送语言指令")
    speak.do_tasks(config['baidu_tts'], tasks_info[3])
    print("重新检测任务状态")

    tasks_info = fetch.fetch_tasks_info(config['taobao'])
    if tasks_info[3] is None:
        print("获取任务信息失败")
    else:
        msg = notify.build_nitofy_msg(tasks_info)
        print(msg)
    print("推送微信通知")
    notify.notify(config['weixin'], tasks_info)

print("--------- 打卡完毕 ---------")
