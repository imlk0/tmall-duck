import requests
import json
from time import strftime, localtime


def build_nitofy_msg(tasks_info):
    res = ''
    res += tasks_info[1]
    res += '\n'
    res += tasks_info[2]
    for task in tasks_info[3]:
        res += '\n'
        res += ('[{}] {}'.format('已完成' if task['finished']
                                 else '未完成', task['content']))
    if tasks_info[0]:
        res += '\n'
        res += '今日任务已完成'
    return res


def notify(config, tasks_info):
    access_token = get_access_token(config['corpid'], config['secret'])
    if tasks_info[0] is None:
        content = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": int(config['agentid']),
            "text": {
                "content": "获取今日打卡信息失败\n时间：{}".format(strftime('%Y-%m-%d %H:%M:%S', localtime()))
            }
        }

    else:
        # pic_url = upload_pic(access_token, tasks_info[4])
        msg = build_nitofy_msg(tasks_info)
        content = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": int(config['agentid']),
            "text": {
                "content": "天猫精灵打卡结束[{}]\n时间：{}\n{}".format('已完成' if tasks_info[0] else '未完成',
                                                            strftime(
                                                                '%Y-%m-%d %H:%M:%S', localtime()),
                                                            msg)
            }
        }

    resp = requests.post(
        'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token, data=json.dumps(content))
    j = resp.json()
    if j['errcode'] != 0:
        print("文字消息推送请求异常：", resp.json())

    if tasks_info[4] is not None:
        media_id = upload_pic(access_token, tasks_info[4])
        content = {
            "touser": "@all",
            "msgtype": "image",
            "agentid": int(config['agentid']),
            "image": {
                "media_id": media_id
            }
        }
        resp = requests.post(
            'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token, data=json.dumps(content))
        j = resp.json()
        if j['errcode'] != 0:
            print("图片消息推送请求异常：", resp.json())


def upload_pic(access_token, pic_bytes):
    files = {'media': pic_bytes}
    resp = requests.post('https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type=image'.format(access_token),
                         files=files)
    j = resp.json()
    return j['media_id']


def get_access_token(corpid, corpsecret):
    params = {
        'corpid': corpid,
        'corpsecret': corpsecret
    }
    resp = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken', params)
    return resp.json()['access_token']
