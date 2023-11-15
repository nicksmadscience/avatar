from flask import Flask, request
import json, pprint, PIL

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello_world():
    omfg = json.loads(request.data)
    # print (request.data)
    # pprint.pprint(omfg)

    # payload = {"innerHeight": innerHeight,
    #             "sessionLength": sessionLength,
    #             "pageHeight": pageHeight,
    #             "scrollEvents": scrollEvents};

    innerHeight = omfg["innerHeight"]
    sessionLength = omfg["sessionLength"]
    pageHeight = omfg["pageHeight"]
    scrollEvents = omfg["scrollEvents"]
    scrollEventCount = len(scrollEvents)

    print ("innerHeight: ", innerHeight)
    print ("sessionLength: ", sessionLength)
    print ("pageHeight ", pageHeight)
    print ("scrollEvents: ", scrollEvents)
    print ("scrollEventCount: ", scrollEventCount)

    heatmap = [0] * pageHeight

    lastScrollEvent = 0
    lastScrollValue = 0
    for ms in range(0, sessionLength):
        if str(ms) in scrollEvents:
            lastScrollEvent = ms
            lastScrollValue = int(scrollEvents[str(ms)])
            # print (lastScrollEvent, lastScrollValue)
        for verticalLine in range(0, innerHeight):
            heatmap[lastScrollValue + verticalLine] += 1

    

    
    heatmapHighestValue = 0
    for jawn in heatmap:
        if jawn > heatmapHighestValue:
            heatmapHighestValue = jawn

    heatmapNormalized = [0.0] * pageHeight
    for jawn in range(0, len(heatmap)):
        print (jawn)
        heatmapNormalized[jawn] = heatmap[jawn] / heatmapHighestValue

    print (heatmapNormalized)
    with open("heatmap.csv", "w") as heatmapFile:
        for jawn in heatmapNormalized:
            heatmapFile.write("{jawn},".format(jawn=jawn))

    from PIL import Image, ImageDraw


    im = Image.open("bg.png")


    # im = Image.new('RGBA', (1728, pageHeight), (0, 0, 0, 0)) 
    draw = ImageDraw.Draw(im) 

    for jawn in range(0, len(heatmapNormalized)):
        heat = int(heatmapNormalized[jawn] * 255)
        red = clamp(heat * 2, 0, 255)
        green = clamp((255 - heat) * 2, 0, 255)
        
        draw.line((0,jawn, 1728,jawn), fill=(red, green, 0, 255))
        # draw.line((0, jawn, 15, jawn), fill=(red, green, 0, 255))
        # draw.line((1713, jawn, 1728, jawn), fill=(red, green, 0, 255))
        

    # innerHeight = omfg["innerHeight"]
    # sessionLength = omfg["sessionLength"]
    # pageHeight = omfg["pageHeight"]
    # scrollEvents = omfg["scrollEvents"]
    # scrollEventCount = len(scrollEvents)

    # draw.text((220, 10), "Session Length", align ="left")
    # draw.text((220, 30), str(sessionLength), align ="left")

    bg = Image.open("bg.png")
    bg.putalpha(192)

    # im.paste(bg, (0, 0))

    Image.alpha_composite(im, bg).show()


    # im.show()


    return "<p>Hello, World!</p>"