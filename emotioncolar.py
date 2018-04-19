import json
import requests
import cv2
import numpy as np

URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

headers = {
    'Content-Type': 'application/{type}',
    'Ocp-Apim-Subscription-Key': '###########################',#yourkey
}

params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
}

def makewindow(colar):
    img =  cv2.imread('whitep.jpg')
    high = img.shape[0]
    wide = img.shape[1]

    for i in range(wide):
        cv2.line(img, (i, 0), (i, high), colar, 20)#(青、緑、赤)(B,G,R)

    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def makecalar(data):
    color = [0, 0, 0]
    for key in data:
        if(key == 'anger'):
            anger = [0, 0, 255]
            for i in range(3):
                color[i] = color[i] + (anger[i] * data[key])
        
        elif(key == 'contempt'):
            contempt = [255, 0, 255]
            for i in range(3):
                color[i] = color[i] + (contempt[i] * data[key])

        elif(key == 'disgust'):
            disgust = [0, 0, 0]
            for i in range(3):
                color[i] = color[i] + (disgust[i] * data[key])
        
        elif(key == 'fear'):
            fear = [255, 255, 0]
            for i in range(3):
                color[i] = color[i] + (fear[i] * data[key])
                    
        elif(key == 'happiness'):
            happiness = [0, 255, 255]
            for i in range(3):
                color[i] = color[i] + (happiness[i] * data[key])

        elif(key == 'neutral'):
            neutral = [255, 255, 255]
            for i in range(3):
                color[i] = color[i] + (neutral[i] * data[key])
            
        elif(key == 'sadness'):
            sadness = [255, 0, 0]
            for i in range(3):
                color[i] = color[i] + (sadness[i] * data[key])

        elif(key == 'surprise'):
            surprise = (0, 255, 0)
            for i in range(3):
                color[i] = color[i] + (surprise[i] * data[key])
    
    for i in range(3):
        color[i] = int(color[i])
    
    newcolor = tuple(color)

    return newcolor

while (True):
    mode = input("画像のURL->'u'\n画像の参照->'r'\n")

    if(mode == 'u'):
        png = input("画像のURLを入力：")
        headers['Content-Type'] = headers['Content-Type'].format(type = 'json')
        pyload = {
            'url' : png,
        }
        try:
            r = requests.post(URL, headers = headers, params = params, data = json.dumps(pyload))
            data = json.loads(r.text)
            face = data[0]#返ってくる値はリストの中に辞書が入っている状態
            emo = face['faceAttributes']['emotion']
            
            makewindow(makecalar(emo))
        except NameError:
            print("ERROR")  
    
    elif(mode == 'r'):
        
        pig = input("参照したい画像の名前を入力：")
        headers['Content-Type'] = headers['Content-Type'].format(type = 'octet-stream')
        try:
            r = requests.post(URL, headers = headers, params = params, data = open(pig,'rb')) 
            data = json.loads(r.text)
            face = data[0]#返ってくる値はリストの中に辞書が入っている状態
            emo = face['faceAttributes']['emotion']

            makewindow(makecalar(emo))
        except:
            print("そのディレクトリにその画像ははいっていますか")
            print("ERROR")
    else:
        print("画像のURLまたは画像が添付されていません")
    
    keyword = input("終了したい場合は'exit()'と入力してください\n")
    if(keyword == 'exit()'):
        break
