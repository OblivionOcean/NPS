from flask import Flask, send_file
import requests
import yaml
import io
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route("/")
def index():
    return "Bruh."

def get_yaml(file):
    rf = open(file, mode='r', encoding='utf-8')
    crf = rf.read()
    rf.close()
    yaml_data = yaml.load(stream=crf, Loader=yaml.FullLoader)
    return yaml_data

config = get_yaml("./config.yaml")
url_record = "https://music.163.com/weapi/v1/play/record?csrf_token="+config["csrf"]

header = {
    'User-Agent': config["ua"],
    'Cookie': config["cookie"],
    'Origin': "https://music.163.com",
    'Referer': "https://music.163.com/user/songs/rank?id=" + config["id"],
}

def get_record(url):
    params = {
        'params': config["params"],
        'encSecKey': config["esk"]
    }
    response = requests.post(url, headers=header, params=params)
    return response.json()

def parse_record(data):
    allsongs, weeksongs = data['allData'], data['weekData']
    all_time_songs_list, one_week_song_list = [], []
    for song in allsongs:
        name = song['song']['name']
        singer = song['song']['ar'][0]['name']
        playCount = song['playCount']
        a = (name, singer, playCount)
        all_time_songs_list.append(a)
    for song in weeksongs:
        name = song['song']['name']
        singer = song['song']['ar'][0]['name']
        playCount = song['playCount']
        a = (name, singer, playCount)
        one_week_song_list.append(a)
    return [all_time_songs_list, one_week_song_list]

def drawer(ds, name, num = 0):
    # 创建一个新的白色图像
    width, height = 1200, len(ds[num])*30+80
    image = Image.new('RGB', (width, height), (255, 255, 255))

    # 创建一个可以在图像上绘图的对象
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./Deng.ttf', 60)
    text = "本周网易云个人听歌排行" if num else "网易云个人历史听歌排行"
    draw.text((10, 10), text, fill=(0, 0, 0), font=font)
    font = ImageFont.truetype('./Deng.ttf', 20)
    for i in range(len(ds[num])):
        text = "    ".join([ds[num][i][0],ds[num][i][1],str(ds[num][i][2])])
        draw.text((10, i*30+80), text, fill=(0, 0, 0), font=font)
    image.save(name, format="PNG")

@app.route('/week_poster.png')
def week_post():
    week = io.BytesIO()
    json_record = get_record(url_record)
    dataset = parse_record(json_record)
    drawn = drawer(ds=dataset, name = week, num = 1)
    week.seek(0)
    return send_file(week, mimetype="image/png")

@app.route('/all_time_post.png')
def all_time_post():
    alltime = io.BytesIO()
    json_record = get_record(url_record)
    dataset = parse_record(json_record)
    drawn2 = drawer(ds=dataset, name = alltime, num = 0)
    alltime.seek(0)
    return send_file(alltime, mimetype="image/png")

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='2333')