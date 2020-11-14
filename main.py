#!/usr/bin/python3
# coding=utf-8

from time import strftime, localtime
import json
import fetch
import notify
import speak
import os
import worker
import argparse


project_dir = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser(description='tmall duck tool')
parser.add_argument('-c', '--config', dest='config_file', action='store', default=project_dir+'/config.json', required=False, help='config file path, default is config.json')
args = parser.parse_args()
config = json.load(open(args.config_file, 'r'))

print("--------- 触发打卡 ---------")
print("当前系统时间：{}".format(strftime('%Y-%m-%d %H:%M:%S', localtime())))


# finished_all, days_of_checkin, schedule, tasks, ele_tasks.screenshot_as_png
tasks_info = fetch.fetch_tasks_info(config)
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
