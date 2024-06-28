from flask import Flask, send_file, request, jsonify
import requests
import yaml
import io
from PIL import Image, ImageDraw, ImageFont
from os.path import dirname, abspath, join

dir = dirname(abspath(__file__))

def get_yaml():
    global dir
    with open(join(dir, "..", "config.yaml"), mode='r') as file:
        crf = file.read()
    yaml_data = yaml.load(stream=crf, Loader=yaml.FullLoader)
    return yaml_data

app = Flask(__name__)
config = get_yaml()

@app.route("/")
def index():
    return "Bruh."

def get_record(id, csrf):
    header = {
        'User-Agent': config["ua"],
        'Cookie': config["cookie"],
        'Origin': "https://music.163.com",
        'Referer': "https://music.163.com/user/songs/rank?id=" + id,
        }
    params = {
        'params': config["params"],
        'encSecKey': config["esk"]
    }
    response = requests.post("https://music.163.com/weapi/v1/play/record?csrf_token=" + csrf, headers=header, params=params)
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
    width, height = 1200, len(ds[num])*30+80
    image = Image.new('RGB', (width, height), (255, 255, 255))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(join(dir, "..", "static", "Deng.ttf"), 60)
    text = "Favourite Songs of the Week" if num else "Favourite Songs of All Time"
    draw.text((10, 10), text, fill=(0, 0, 0), font=font)
    font = ImageFont.truetype(join(dir, "..", "static", "Deng.ttf"), 20)
    for i in range(len(ds[num])):
        text = "    ".join([ds[num][i][0],ds[num][i][1],str(ds[num][i][2])])
        draw.text((10, i*30+80), text, fill=(0, 0, 0), font=font)
    image.save(name, format="PNG")

@app.route('/week')
def week_post():
    week = io.BytesIO()
    id = request.args.get('id')
    csrf = request.args.get('csrf')
    json_record = get_record(id, csrf=csrf)
    dataset = parse_record(json_record)
    drawn = drawer(ds=dataset, name = week, num = 1)
    week.seek(0)
    return send_file(week, mimetype="image/png")

@app.route('/alltime')
def all_time_post():
    alltime = io.BytesIO()
    id = request.args.get('id')
    csrf = request.args.get('csrf')
    json_record = get_record(id, csrf=csrf)
    dataset = parse_record(json_record)
    drawn2 = drawer(ds=dataset, name = alltime, num = 0)
    alltime.seek(0)
    return send_file(alltime, mimetype="image/png")

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='2333')