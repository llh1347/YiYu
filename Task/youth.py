#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可 YOUTH_WITHDRAWBODY
# 分享一篇文章，找到 put.json 的请求，拷贝请求体，放入对应参数 YOUTH_SHAREBODY
# 清除App后台，重新启动App，找到 start.json 的请求，拷贝请求体，放入对应参数 YOUTH_STARTBODY

cookies1 = {
  'YOUTH_HEADER': {"Accept": "*/*","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-cn","Connection": "keep-alive","Content-Type": "","Cookie": "sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2213547618%22%2C%22%24device_id%22%3A%2217d1f520595380-038f8883c9ab93-724c1251-250125-17d1f520596229%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217d1f520595380-038f8883c9ab93-724c1251-250125-17d1f520596229%22%7D; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1637141984,1637142104,1637142416,1637142613; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1637141872,1637141942,1637141985,1637142614","Host": "kd.youth.cn","Referer": "https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=3380db0f62bd93cb19c3f0bcc73590b4&sign=2cc6bf4816d1b5b276efe2c4c44bdf46&channel_code=80000000&uid=13547618&channel=80000000&access=WIfI&app_version=1.7.0&device_platform=iphone&cookie_id=e797b2c0673af4ee6361be81f3eb2d7b&openudid=3380db0f62bd93cb19c3f0bcc73590b4&device_type=1&device_brand=iphone&sm_device_id=202108170839191618b14042c73782c099854d47064d7e01bebba4c9480575&version_code=170&os_version=13.5&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIej3q6ruWKx3Y2xhnyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLDdjWmFso7grqnIapqGcXY&device_model=iPhone_6&subv=1.5.1&","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148p","X-Requested-With": "XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjab0hHSxXenkWHSkCwB26b0x_gtnWSAWxe4W5DsfKJWZCtYjtG-pISRI05IOO_tWwKsjHS2coC8oRXfSq-9lTAagrC-ydpEPghdlY8NOPcQv8F0Lahi7CuB03j1gJr86JaOW7ZzzZzjqLuHW38aqQ37pAuTLrCqwSoWUr1K2_rC65VVW1xGBbhpu2mmF9ZPuXpotQEtDITAzKPOCM3RuMHTCuKe7zzYjjCN59crc88bkK7U-g24fMwohQo0K9jiXH0BKvwU7Z_vV9EKB_WqADnAWtxL_aouUpS613U7bkHdVMOZLszQypKW00w77-tSya9WkjeUimh4s_InK9B2qB8wJrfy-J1Oz0n4kLb86KDpn2HJBZ7PIKBG2vbkaU7V7FJWguDb-g2VHTar8eAudj5hMdAzyejIm-buuWGFQ72xhoPUpYeMzwlrWwI0aEPLrOCXM2ET93k3g9CV-qcD5udeRtXaoxVnOIxJWLavQGNw7TdxzkENTzj9GwXHGIA_7PqnWmRNsb2C2HS8bHF5oVFW8gvKmQJXhsPw4QdnEf3htklW8hxzC_rJs1nU7BlK6ybrZ6R6Rp4BNNzrZVfpMyhEQV6BBeMCRSTknZUeVCWYZy7FRfk5LOD6PfjRdpjBgK8duDD0K3txas8dPetKdmg4K6L-fZvm8Hnk57wievZG4WQfBYKUN_u_mcVbJ2zi3-GAIyPWXFKPEH1HultLSbtdpZoupyqPHSAEvn1V1Sv5YuGpc_famofEBidrOyuIb8SALrIkXkPNWM4JNIab_7wiOtcJJWjMFJgee9MX6XMXoz7Y22P-35ieethsnlWrehr1bONmm9kyNYaa3CkKm_LDAGPzvr1Rqkc%3D',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBAHpRMEOlwzczjbU6gjTSizZFE2TSUamRRME0wnUyUTr0y-jd030OIXuUm1sg1C3Nm_OLIp7vmIodzb74mUjURcDqrs1rj7PXYhbtbWLp-rmZMgxgBGOM0RW0E-R_ph5AeoUBOIMEBkINIei-6Nh9nlrgbr7iujWU6WhxGWPwQTfj0JrQeUzE_q-HFhClO47fwYM3zYLSOvRGQvlpgQv6uLjOow762OPhFzsuiAlbyapxuzEhh-GwTODkalz9nxXkgU9Mh4sQGj4CDXT8HhorLKAH7GGsDqeRkBWZ057tu88Se5b3vi5TBXIC1vhVt6IC6p8y3s4fQW2NHC3qjQEfZum7W1b1lahutEqJZp4aMIz_-HcQu_7vmJSAxX3NsHFF3BM39pxPls8R9YK9ydDxTo1vbzmjESKBBuN-HBY7toFfj3sw29vbBf1jNzf272nzg3ulbbcWkrax6cHEZ4pSlMmtfkwxGAb26SlLtHPd3HtopYNqEPK4hWg6xjeb1oC1oTB4pG7Zy9QuEQ3OSeXcAcx-uh7D2FFjLXLXPGcDXiOB5hLRH4BXMQlUivJIn23d-yzGRzWx9bTTdxwvoOKes6wr5sJQSqxte2jgiT7a5WlMFyA4puMAgwZ69f_cNw3QZEpjkhovdteIlNEmnZ-K7HrtORIsoT5Qk%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'stype=WEIXIN&channel_code=80000000&uid=13547618&article_id=40841339&channel=80000000&app_version=1.7.0&from=2&phone_network=WIfI&device_type=1&client_version=1.7.0&phone_code=3380db0f62bd93cb19c3f0bcc73590b4&sm_device_id=202108170839191618b14042c73782c099854d47064d7e01bebba4c9480575&is_hot=0&sign=b23fe038251c326bfb4aae22fdb1b303',
  'YOUTH_STARTBODY': 'access=WIFI&app_version=1.7.0&channel=80000000&channel_code=80000000&cid=80000000&client_version=1.7.0&device_brand=iphone&device_id=&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=1&openudid=3380db0f62bd93cb19c3f0bcc73590b4&os_version=13.5&phone_code=3380db0f62bd93cb19c3f0bcc73590b4&phone_network=WIFI&platform=3&request_time=1637149937&resolution=750x1334&sm_device_id=202108170839191618b14042c73782c099854d47064d7e01bebba4c9480575&szlm_ddid=D223H%2B7ZWPN0h8iyHUQrFBdfRnZSWpkam2457KnGsBs2IXe1&time=1637149937&token=66fe00b4cadad8b486a3ef8b90f10e86&uid=13547618&uuid=3380db0f62bd93cb19c3f0bcc73590b4' 
}
cookies2 = {
  'YOUTH_HEADER': {"Accept": "*/*","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-cn","Connection": "keep-alive","Content-Type": "","Cookie": "Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1637142416,1637142613,1637144000,1637144394; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1637141985,1637142614,1637144000,1637144394; sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2258457176%22%2C%22%24device_id%22%3A%2217d1f520595380-038f8883c9ab93-724c1251-250125-17d1f520596229%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217d1f520595380-038f8883c9ab93-724c1251-250125-17d1f520596229%22%7D","Host": "kd.youth.cn","Referer": "https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=3380db0f62bd93cb19c3f0bcc73590b4&sign=23bc25ff8f324d34f38a96e3805feb9d&channel_code=80000000&uid=58457176&channel=80000000&access=WIfI&app_version=1.7.0&device_platform=iphone&cookie_id=b9aeceb6fa6457bcab21bd9d7991af9f&openudid=3380db0f62bd93cb19c3f0bcc73590b4&device_type=1&device_brand=iphone&sm_device_id=202108170839191618b14042c73782c099854d47064d7e01bebba4c9480575&version_code=170&os_version=13.5&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOyp4VqhbJ6ma_OqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFooKZrrmyY4Gvm7OEY2Ft&device_model=iPhone_6&subv=1.5.1&","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","X-Requested-With": "XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjab0hHSxXenkWHSkCwB26b0x_gtnWSAWxe4W5DsfKJWZCtYjtG-pISRI05IOO_tWwKsjHS2coC8oRXfSq-9lTAagrC-ydpEPghdlY8NOPcQv8F0Lahi7CuB03j1gJr86JaOW7ZzzZzjqLuHW38aqQ37pAuTLrCqwSoWUr1K2_rC65VVW1xGBbhpL4IXsuQRhzNl-UO1QbDyn8WJJiQVma993ComWaOQNKeCiPBmYNX6jACKYMGMtmZgWrJ1crQmbFz-tR-l44MiJ23TdBNT0q3GSwafMVCMFpVyW9naaF6Dd-I1XIt7De8d47GNsOiV2zNvE9r4klbZuyQo1H-5RnHBmHSuOLz42NScXlp7ouvlqf3Yx42V7dX2SzImujk5KyCG_oNhfA-vowY8DFg8r6tNJIPpfrMVVwcfrvcVcY8BfO35aLn00QIflBMOmIvFB0Uz1lj0oM8DMKYz13OII4nbNXPZ2biIMtM6emugz0Vncpa4Tcgfgn7F0Nur4GHsqOgWxx-2GuCyuxjxbXaUVgi2-tWb8vEN7dKDgCguFr_Cq1pB1f5kRZjysnPB9zidmSkglLadSSgFd5Ubv8VjPOIhACcf3qWWQA-9InTC3wH7Xucd6XAsGofoEw0pBkZXk8H7ScWhSQ_3FbBCaDJ0djeKw12NxpglkVuZYeJSrrodY4LvCUYyttXbYzshgbYutXssCTDqBqPfUkO8gXMPfkfGg3AsggYh8pmevUSdDOAtUTbPV3oc-yzssD-XhYGe7puHAgO0irK4aVBAZRAfHwiE1gmpsYgpkkCmB3BE9bC2Qpo9WhFJvYOT5nu1EIOetarrBNfkFsKaof_CTILYeZbb0eOvsRRfU3Y%3D','YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBDA-0KEhOYijSsJjfZCSyNFN8GmIV_nwxaRvXsh5A05xUFH8ir7aLQdfJ-jr9Pbk-URN8sILeQY-BJvPcmktoIgPiGzoLyZ1PWyBIxTZKZwmNa0wnHAhckfOageW9BwD5Rx28loKp2eAku51yNEdm4BodzMj2u3t2HmZ9DoMossP2Du795dTiVryls5G5QBaw_z9HmkoE0wE7esRfkoz0nc2LEoKyV8Qa2hBUu6YiPX2iNJPt0e35nNWbr5PU2UjJMk41fV3IhGbS-PLa_AnCwgrLUEgqHwZB7rw1VMxavFAAjtHgubfNZAbH66nEKeib5ySq5Skwe7jT0KnOAg7k6g2O1bRQjQCtmWlXZ5yFpPq5uzu4HKwT18ebMpkqCYgwzZahqfQBttwPYnVZZrOAn71NiautoO_nyhDqAE1msreiWhH7mjRu4AhSmXwciaIPqXwZdIq34Ufsav1AwRyXmQwGUqRKiGLAtWCMEnw_82amxWQX1mG8KvUgF7dp4xB52AKnWaJEgcZTC3R4gpqAUZ626XPMuOu_oAmp3JdpBUqAi3ABCjYLZJscnP2LfQJ21Xkhz5nYB2aw4HC7qYu3pLciM8HYaEWFSuGD5doyjr1wF2MjOkX7v9fEKpVrNLTgyFUZ6JWXDsiL50pzxUG72aXW4D5qdxXbs%3D',
  #'YOUTH_WITHDRAWBODY': 'p=9NwGV8Ov71o%3DC5Jtxwc6iVuTcJotRQ4YI8A3NCwuYXT0EKsN_1lY-hyQIDxm06IFOuscnysqyQaOVYFM2zkVxN4RcXnskOBBUZVvSxZzH3OXF7KXX5GSWN3iARhhl6MTLPKFnk4Ejz2lrWP6KTi95XkKMCEyL80pi9a-JOPP_1Pya3sr2pVJC5Ep2dimAPNO-_PNE9g5WgFAayI1tRHUaBUQBHpZQbjYPYrkwIYUX58BJ_HRS5tMg6BCanTwGIbwDDRfLWQ707fi82jgORuWjD8VJETzfHnKyr8f3TDkdgcXw8JmLsakjdLLL74RWCNclgCWwIzV8gERjL82LwbQ4JO2v03dcVKH3OV5gupLy07cSR6FR89WNbhw0YWAHg0-e_-0ZfZGsHQV1JRALbQUxCbyZqxG-er8Egi0k1-X-xvi2yrQjqqrDlrgJxs4HAsnhgmGXCIKfp_eyv5GDvLSk2FboZ9YDDsfYw%3D%3D',
  'YOUTH_SHAREBODY': 'stype=WEIXIN&channel_code=80000000&uid=58457176&article_id=40832497&channel=80000000&app_version=1.7.0&from=2&phone_network=WIfI&device_type=1&client_version=1.7.0&phone_code=3380db0f62bd93cb19c3f0bcc73590b4&sm_device_id=202108170839191618b14042c73782c099854d47064d7e01bebba4c9480575&is_hot=0&sign=8e2376362e19de675707cc965224db66',
  'YOUTH_STARTBODY': 'access=WIFI&app_version=1.7.0&channel=80000000&channel_code=80000000&cid=80000000&client_version=1.7.0&device_brand=iphone&device_id=&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=1&openudid=3380db0f62bd93cb19c3f0bcc73590b4&os_version=13.5&phone_code=3380db0f62bd93cb19c3f0bcc73590b4&phone_network=WIFI&platform=3&request_time=1637144320&resolution=750x1334&sm_device_id=202108170839191618b14042c73782c099854d47064d7e01bebba4c9480575&szlm_ddid=D223H%2B7ZWPN0h8iyHUQrFBdfRnZSWpkam2457KnGsBs2IXe1&time=1637144321&token=9957451d3e15c692beae0b4ef026ed2c&uid=13547618&uuid=3380db0f62bd93cb19c3f0bcc73590b4'
  }


COOKIELIST = [cookies1,cookies2]  # 多账号准备

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
  COOKIELIST = []
  for i in range(5):
    headerVar = f'YOUTH_HEADER{str(i+1)}'
    readBodyVar = f'YOUTH_READBODY{str(i+1)}'
    readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
    withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
    shareBodyVar = f'YOUTH_SHAREBODY{str(i+1)}'
    startBodyVar = f'YOUTH_STARTBODY{str(i+1)}'
    if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
      globals()['cookies'+str(i + 1)]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
      globals()['cookies'+str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_SHAREBODY"] = os.environ[shareBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_STARTBODY"] = os.environ[startBodyVar]
      COOKIELIST.append(globals()['cookies'+str(i + 1)])
  print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"

def get_standard_time():
  """
  获取utc时间和北京时间
  :return:
  """
  # <class 'datetime.datetime'>
  utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
  beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
  return beijing_datetime

def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def sign(headers):
  """
  签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/sign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def signInfo(headers):
  """
  签到详情
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/getSign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到详情')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def punchCard(headers):
  """
  打卡报名
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/signUp'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('打卡报名')
    print(response)
    if response['code'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doCard(headers):
  """
  早起打卡
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/doCard'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('早起打卡')
    print(response)
    if response['code'] == 1:
      shareCard(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareCard(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
  endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
  try:
    response = requests_session().post(url=startUrl, headers=headers, timeout=30).json()
    print('打卡分享')
    print(response)
    if response['code'] == 1:
      time.sleep(0.3)
      responseEnd = requests_session().post(url=endUrl, headers=headers, timeout=30).json()
      if responseEnd['code'] == 1:
        return responseEnd
    else:
      return
  except:
    print(traceback.format_exc())
    return

def luckDraw(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/luckdraw'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('七日签到')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def timePacket(headers):
  """
  计时红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}TimePacket/getReward'
  try:
    response = requests_session().post(url=url, data=f'{headers["Referer"].split("?")[1]}', headers=headers, timeout=30).json()
    print('计时红包')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def watchWelfareVideo(headers):
  """
  观看福利视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/recordNum?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('观看福利视频')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def shareArticle(headers, body):
  """
  分享文章
  :param headers:
  :return:
  """
  url = 'https://ios.baertt.com/v2/article/share/put.json'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('分享文章')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def threeShare(headers, action):
  """
  三餐分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareNew/execExtractTask'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  body = f'{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('三餐分享')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def openBox(headers):
  """
  开启宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/openHourRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('开启宝箱')
    print(response)
    if response['code'] == 1:
      share_box_res = shareBox(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareBox(headers):
  """
  宝箱分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/shareEnd'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('宝箱分享')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendList(headers):
  """
  好友列表
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友列表')
    print(response)
    if response['error_code'] == '0':
      if len(response['data']['active_list']) > 0:
        for friend in response['data']['active_list']:
          if friend['button'] == 1:
            time.sleep(1)
            friendSign(headers=headers, uid=friend['uid'])
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendSign(headers, uid):
  """
  好友签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友签到')
    print(response)
    if response['error_code'] == '0':
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def sendTwentyScore(headers, action):
  """
  每日任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print(f'每日任务 {action}')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchAdVideo(headers):
  """
  看广告视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data="type=taskCenter", headers=headers, timeout=30).json()
    print('看广告视频')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchGameVideo(body):
  """
  激励视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
  headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('激励视频')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def visitReward(body):
  """
  回访奖励
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/mission/msgRed.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('回访奖励')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def articleRed(body):
  """
  惊喜红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/article/red_packet.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('惊喜红包')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def readTime(body):
  """
  阅读时长
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/user/stay.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('阅读时长')
    print(response)
    if response['error_code'] == '0':
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def rotary(headers, body):
  """
  转盘任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘任务')
    print(response)
    return response
  except:
    print(traceback.format_exc())
    return

def rotaryChestReward(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘宝箱')
    print(response)
    if response['status'] == 1:
      i = 0
      while (i <= 3):
        chest = response['data']['chestOpen'][i]
        if response['data']['opened'] >= int(chest['times']) and chest['received'] != 1:
          time.sleep(1)
          runRotary(headers=headers, body=f'{body}&num={i+1}')
        i += 1
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def runRotary(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('领取宝箱')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doubleRotary(headers, body):
  """
  转盘双倍
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘双倍')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def incomeStat(headers):
  """
  收益统计
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=50).json()
    print('收益统计')
    print(response)
    if response['status'] == 0:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def withdraw(body):
  """
  自动提现
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('自动提现')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def bereadRed(headers):
  """
  时段红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}Task/receiveBereadRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('时段红包')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def startApp(headers, body):
  """
  启动App
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v6/count/start.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('启动App')
    print(response)
    if response['success'] == True:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def run():
  title = f'📚中青看点'
  content = ''
  result = ''
  beijing_datetime = get_standard_time()
  print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
  hour = beijing_datetime.hour
  for i, account in enumerate(COOKIELIST):
    headers = account.get('YOUTH_HEADER')
    readBody = account.get('YOUTH_READBODY')
    readTimeBody = account.get('YOUTH_READTIMEBODY')
    withdrawBody = account.get('YOUTH_WITHDRAWBODY')
    shareBody = account.get('YOUTH_SHAREBODY')
    startBody = account.get('YOUTH_STARTBODY')
    rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'

    if startBody:
      startApp(headers=headers, body=startBody)
    sign_res = sign(headers=headers)
    if sign_res and sign_res['status'] == 1:
      content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
    elif sign_res and sign_res['status'] == 2:
      send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
      continue

    sign_info = signInfo(headers=headers)
    if sign_info:
      content += f'\n【账号】：{sign_info["user"]["nickname"]}'
      content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
      result += f'【账号】: {sign_info["user"]["nickname"]}'
    friendList(headers=headers)
    if hour > 12:
      punch_card_res = punchCard(headers=headers)
      if punch_card_res:
        content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
    if hour >= 5 and hour <= 8:
      do_card_res = doCard(headers=headers)
      if do_card_res:
        content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
    luck_draw_res = luckDraw(headers=headers)
    if luck_draw_res:
      content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
    visit_reward_res = visitReward(body=readBody)
    if visit_reward_res:
      content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
    if shareBody:
      shareArticle(headers=headers, body=shareBody)
      for action in ['beread_extra_reward_one', 'beread_extra_reward_two', 'beread_extra_reward_three']:
        time.sleep(5)
        threeShare(headers=headers, action=action)
    open_box_res = openBox(headers=headers)
    if open_box_res:
      content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
    watch_ad_video_res = watchAdVideo(headers=headers)
    if watch_ad_video_res:
      content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
    watch_game_video_res = watchGameVideo(body=readBody)
    if watch_game_video_res:
      content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
    read_time_res = readTime(body=readTimeBody)
    if read_time_res:
      content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
    if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
      beread_red_res = bereadRed(headers=headers)
      if beread_red_res:
        content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
    for i in range(0, 5):
      time.sleep(5)
      rotary_res = rotary(headers=headers, body=rotaryBody)
      if rotary_res:
        if rotary_res['status'] == 0:
          break
        elif rotary_res['status'] == 1:
          content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
          if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
            double_rotary_res = doubleRotary(headers=headers, body=rotaryBody)
            if double_rotary_res:
              content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

    rotaryChestReward(headers=headers, body=rotaryBody)
    for i in range(5):
      watchWelfareVideo(headers=headers)
    timePacket(headers=headers)
    for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward', 'first_share_article']:
      time.sleep(5)
      sendTwentyScore(headers=headers, action=action)
    stat_res = incomeStat(headers=headers)
    if stat_res['status'] == 0:
      for group in stat_res['history'][0]['group']:
        content += f'\n【{group["name"]}】：+{group["money"]}青豆'
      today_score = int(stat_res["user"]["today_score"])
      score = int(stat_res["user"]["score"])
      total_score = int(stat_res["user"]["total_score"])

      if score >= 100000 and withdrawBody:
        with_draw_res = withdraw(body=withdrawBody)
        if with_draw_res:
          result += f'\n【自动提现】：发起提现10元成功'
          content += f'\n【自动提现】：发起提现10元成功'
          send(title=title, content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现10元成功')

      result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
      content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

  print(content)

  # 每天 23:00 发送消息推送
  if beijing_datetime.hour == 23 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 50:
    send(title=title, content=result)
  elif not beijing_datetime.hour == 23:
    print('未进行消息推送，原因：没到对应的推送时间点\n')
  else:
    print('未在规定的时间范围内\n')

if __name__ == '__main__':
    run()
