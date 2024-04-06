from flask import Flask, send_file
import requests
import yaml
import io
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route("/")
def index():
    return "Bruh."

config = {
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "esk": "6a5d4c5320339c326f791e50e60be8981938c94b32922799d840c38390bea8423d1c7099cf3dce921767779c8373d63f37d06fa8a6280d5b35987e260038cc8e123e2e6b4fff995e1a4c3b795db2acefccde924ada50ac0d0599d1c2da7aa45a167e7cd13fa349d98f1e957d3bac9664e748ac6295aac8a007891ce667fc939c",
    "params": 'kLZgf1mKliiSDpk9A0Z5dAGNBP1UePJwdEOnoPO2Oz1R5UJpBTtApsNYVWtyKohI27hOZ8ALhilkAMeF+2kcXeuHoPLsZ2Q2aldfAIyv3vOHX8u5+H26Lj/iY0L+zNvlCnt2RBVEtWP1u84SKQAHmGd+xuGl41Eu6896AXnTmGqVkdZ8hYdN61UE6dP6kR2iJt/8okDwFf229A6Iuo93LgOWfvwXtg/cC6IuMcYSJ6o=',
    "csrf": "0f503f6ece43ce33419e80bbcf95166a",
    "id": "1663685209",
    "cookie": "_ntes_nnid=0a63051a304257b24653863204fb2de7,1699664829996; _ntes_nuid=0a63051a304257b24653863204fb2de7; NMTID=00OVNbWkymyQIPUnUgvrMWZAerlpaEAAAGOk6hNjw; _iuqxldmzr_=32; WEVNSM=1.0.0; WNMCID=pszrdp.1711874262790.01.0; WM_TID=zLXlZ1%2FHJa5BUABUQQaQys%2FfqM5buWcy; ntes_utid=tid._.9t6AZvX5Y%252FBAA1UUQFaE29%252Fa%252BM5xFqVQ._.0; sDeviceId=YD-gCOmpTBJv5FBR1BUVRKVzs%2Fa7c9lV%2BQa; WM_NI=pwDggB704PS2XdV3PGyOvxAtD5n%2FEDHq0EvmknAHFoKcT%2BZDrPpRJVQCb0JfszXyRnc2xtrQQF2D287aazuxSjLjCkuvtidpL6anuGwg8XmZ943SF9EENHrEKSNXawnibjI%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee86d546b88ae1b0c2808fb08ba6d45b879a9aadc421a8e89cabc74783b596d9d62af0fea7c3b92ab4a98c88e64af5f0fcb1d23a9cbc9ad4d34dbb91ba99c48088eba2d0c8508caf00a6f567a9b28fa9c56589bd9cccd950b290c0b3c95e939daed1c96eb1a6989ad166a1eeb895f15b939afea5b134f5bfaf9bf87491b6848bc261b7aabc8ae77c90eaaf8ff84db5b9f8b9f052fbecfdb4c533879b82a9f14f898d82b9e47daeb7ae8bcc37e2a3; __snaker__id=S749L3aPis1BPNo6; gdxidpyhxdE=KOdMu8c%2F%5CHNzKyEM8ItBysosjSYQVONYoIeQrOmBI2NxqITzydZA0M8zA%2Fy2TsNYKfAVrJdSQ5t3rX9QB0iOqSZ4BGhCKdMYZUllJx2YR8qQNpEtmLC1gE%5Cyu9aKtzr9WtoMKTSSNk9k7aocVSRebjmWU%2FbSdDB64B4lX1tQYcX5SEAf%3A1712371973514; MUSIC_U=00A485CB9B12721ED5E6141CB524C7A1E733A53F509F41D855C8692E8AA9FAA71E051D2F2B21819F79ACE99D66082FCE24155387E2CD34DE7FA71E4E440DC32EA4B8E756EB98B9B434EA8667B8739F3EBF19E3BEBADCEC1E62FA2B976E0057785B1242F24A4A3260786D5AB32D95C636BFCA35997B3682E219156AE2E8D44E2DC6CDCD9B9D322D841A5FE8C94C373B467035FDF774973E42FF312444DA46E9D52EF838AE441CEA605BF2DE9F5AA44B59A9BD44C8A584FB297EBC281AA2935E389F7B3B48D77A591ACFD27AC8900BD3EAC455AF8BFF5C2AA1D463C2416B8A48905CC223C66DCEE51E356863109FE3FC74CD937E752227DF7207996903CCDC63C90DCF3360B8046103725DDDE730BCDE3F556DAB6CEA5456DFE316C1AD0F9BE35E159D607CF7D7AC18571E4E66A26CA06DE8CD183F74763B8091D20F4B8C3A5AA68CF35D31C8068D7B68DB1EFF16DA590553A35BA3F9849429F51E424E181F91C657E213E81662C74E1C5BEAFFCAA7F5D64A; __csrf=0f503f6ece43ce33419e80bbcf95166a; __remember_me=true; ntes_kaola_ad=1; JSESSIONID-WYYY=0CwClXR2x9gkyfoG%2BdP44J6jFo39gyaEH0%2BvycAdSQWWJsJC4zGT0QT9nDA4cGoAJqdi30n2G%2BXAzkEyZo%5CiVBNwd45IrESfC2zRZIBzbPe7Gc28rihWautC9fBn9I8U9Y027HM%2Fce12hHmcaCSwTrEI3eRCjWOPGQe4uWh7WJsC1qHE%3A1712382113645"
}

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
    font = ImageFont.truetype('Deng.ttf', 60)
    text = "本周网易云个人听歌排行" if num else "网易云个人历史听歌排行"
    draw.text((10, 10), text, fill=(0, 0, 0), font=font)
    font = ImageFont.truetype('Deng.ttf', 20)
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