# coding=utf-8

import re
import time
import speak
from datetime import datetime

# 唤醒词
hello_words = '天猫精灵'


def do_tasks(config, tasks_info):
    tasks = tasks_info[3]
    for task in tasks:
        if not task['finished']:
            print('正在处理：{}'.format(task['content']))
            if not try_all_day_speak_task(config, task) and not try_time_range_speak_task(config, task):
                print("未知任务类型")
    speak.speak(config, hello_words)
    time.sleep(1)
    speak.speak(config, '闭嘴')


def try_all_day_speak_task(config, task):
    gp = re.match(r'对我说 *["”“](.*)["”“]', task['content'])
    if gp is None:
        return False
    text = gp.group(1)
    time.sleep(2)
    speak.speak(config, hello_words)
    time.sleep(2)
    speak.speak(config, text)
    time.sleep(2)
    return True


def try_time_range_speak_task(config, task):
    gp = re.match(
        r'.*在([0-9]{2}:[0-9]{2})-([0-9]{2}:[0-9]{2}).*说 *["”“](.*)["”“]', task['content'])
    if gp is None:
        return False

    time_cur = datetime.now()
    start_time = gp.group(1)
    end_time = gp.group(2)
    if (time_cur.hour > int(start_time.split(':')[0]) or (time_cur.hour == int(start_time.split(':')[0]) and time_cur.minute > int(start_time.split(':')[1]))) and (time_cur.hour < int(end_time.split(':')[0]) or (time_cur.hour == int(end_time.split(':')[0]) and time_cur.minute < int(end_time.split(':')[1]))):
        text = gp.group(3)
        time.sleep(2)
        speak.speak(config, hello_words)
        time.sleep(2)
        speak.speak(config, text)
        time.sleep(2)
    else:
        print("不在时间范围内，当前时间为：{}:{} 任务时间为：{}-{}".format(time_cur.hour, time_cur.minute, start_time, end_time))
    return True



