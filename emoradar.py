from math import pi
import matplotlib.pyplot as plt
import json
import requests

def makegraph(emolist):
# Set data
    cat = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']

    N = len(cat)

    x_as = [n / float(N) * 2 * pi for n in range(N)]
    values = emolist
    # Because our chart will be circular we need to append a copy of the first 
    # value of each list at the end of each list with data
    values += values[:1]
    x_as += x_as[:1]


    # Set color of axes
    plt.rc('axes', linewidth=0.5, edgecolor="#888888")

    # Create polar plot
    ax = plt.subplot(111, polar=True)


    # Set clockwise rotation. That is:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)


    # Set position of y-labels
    ax.set_rlabel_position(0)

    Title =  'emotion'
    ax.set_title(Title, weight='bold', size='medium', position=(0.5, 1.1),

    horizontalalignment='center', verticalalignment='center')

    # Set color and linestyle of grid
    ax.xaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)
    ax.yaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)


    # Set number of radial axes and remove labels
    plt.xticks(x_as[:-1], [])

    # Set yticks
    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"])


    # Plot data
    ax.plot(x_as, values, linewidth=1, linestyle='solid', zorder=3)

    # Fill area
    ax.fill(x_as, values, 'b', alpha=0.3)


    # Set axes limits
    plt.ylim(0, 100)


    # Draw ytick labels to make sure they fit properly
    for i in range(N):
        angle_rad = i / float(N) * 2 * pi

        if angle_rad == 0:
            ha, distance_ax = "center", 10
        elif 0 < angle_rad < pi:
            ha, distance_ax = "left", 1
        elif angle_rad == pi:
            ha, distance_ax = "center", 1
        else:
            ha, distance_ax = "right", 1

        ax.text(angle_rad, 100 + distance_ax, cat[i], size=10, horizontalalignment=ha, verticalalignment="center")


    # Show polar plot
    plt.show()

def addlist(emo):
    values = []
    for word in emo:
        values.append((float(emo[word])) * 100)
    
    return values
        
URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

headers = {
    'Content-Type': 'application/{type}',
    'Ocp-Apim-Subscription-Key': '#########################',#your keynumber
}

params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
}
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

            statas = addlist(emo)
            makegraph(statas)
             
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

            statas = addlist(emo)
            
            makegraph(statas)
        
        except:
            print("そのディレクトリにその画像ははいっていますか")
            print("ERROR")
    else:
        print("画像のURLまたは画像が添付されていません")
    
    keyword = input("終了したい場合は'exit()'と入力してください\n")
    if(keyword == 'exit()'):
        break
