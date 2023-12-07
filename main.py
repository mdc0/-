from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
# from apscheduler.schedulers.blocking import BlockingScheduler

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?key=00c14e612859ea5ca608e65d61c3e345&city=370200"
  res = requests.get(url).json()
  print('天气'+str(res))
  print('天气0'+str(res['lives'][0]))
  weather = res['lives'][0]
  return weather['weather'], weather['temperature']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  print('文字'+str(words.json()['data']['text']))
  # if words.status_code != 200:
  #   return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

# def get_weChat():
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words()}}
# data = {"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
print('推送：'+str(data))
res = wm.send_template(user_id, template_id, data)
print(res)
  
# scheduler = BlockingScheduler()
# scheduler.add_job(get_weChat, 'cron', second='*/5', args=['job1'])
# scheduler.start()
