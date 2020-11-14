#!/bin/python
# coding=utf-8

from time import strftime, localtime
import json
import fetch
import notify
import speak
import os
import worker

print("--------- 触发打卡 ---------")
print("当前系统时间：{}".format(strftime('%Y-%m-%d %H:%M:%S', localtime())))

project_dir = os.path.dirname(os.path.realpath(__file__))
config_private_file = project_dir + '/config_private.json'
config_file = project_dir + '/config.json'
if os.path.exists(config_private_file):
    config = json.load(open(config_private_file, 'r'))
else:
    config = json.load(open(config_file, 'r'))

tasks_info = fetch.fetch_tasks_info(config) # finished_all, days_of_checkin, schedule, tasks, ele_tasks.screenshot_as_png
# 输出首次获取任务结果
msg = notify.build_task_info_msg(tasks_info)
print(msg)

if tasks_info[0] is None:
    # 获取失败
    print("推送微信通知")
    notify.notify_owner(config, tasks_info)
elif not tasks_info[0]:
    # 如果今天需要打卡
    print("开始做任务")
    worker.do_tasks(config, tasks_info)
    print("重新检测任务状态")

    tasks_info = fetch.fetch_tasks_info(config)
    msg = notify.build_notify_msg(tasks_info)
    print(msg)

    print("推送微信通知")
    notify.notify_owner(config, tasks_info)

print("--------- 打卡完毕 ---------")
