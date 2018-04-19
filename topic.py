import requests
import json

apikey = "##############################################################"#yourkey
api = "https://api.apigw.smt.docomo.ne.jp/webCuration/v3/contents?APIKEY={key}&genreId={topic}&s=1&n={pup}&lang=ja"

print("あなたが知りたいトレンドは？")
print("数字の入力\n1:ニュース\n2:エンタメ\n3:スポーツ\n4:ライフスタイル\n5:テクノロジー\n11:グルメ\n12:旅行\n13:ゲーム\n14:アニメ\n")

while(True):
    topics_num = input(':')
    num = int(topics_num)
    topics_sum = input("いくつ記事を表示しますか(1以上50以下)\n")
    page = int(topics_sum) 

    if((num == 1 or num == 2 or num == 3 or num == 4 or num == 5
    or num == 11 or num == 12 or num == 13 or num == 14) and (page > 0 and page < 51)):
        break
    else:
        print("該当する数字がありません。もう一度やり直してください。")

url = api.format(key = apikey, topic = num, pup = page)
tx = requests.get(url)

data = json.loads(tx.text)
print(type(data))
total = int(data["totalResults"])
if(page > total or page == total):
    time = total
else:
    time = page

if(time == 0):
    print("すみません　あなたの探したいトレンドのトピックはヒットしませんでした...")

for i in range (time):
    print("タイトル：" + data["articleContents"][i]["contentData"]["title"])
    print("記事：" + data["articleContents"][i]["contentData"]["body"])
    print("参照サイト：" + data["articleContents"][i]["contentData"]["linkUrl"])
    print('\n')