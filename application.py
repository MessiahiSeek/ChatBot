from flask import Flask, request, send_file
from datetime import datetime
from logger import log
import time
import base64
import os
import sys
import json

log = log()
application = Flask(__name__)
log.startup()

#from objectDetection.yolo_opencv import objectDetect
#from voiceDetection.voice_detect import voiceDetect
from chatbot_class import chatBot
#from objectDetection.read_video import  videoDetect

#Create Instance of Critical objecs
#voice = voiceDetect()
chat = chatBot()

@application.route('/')
def hello_world():
    log.endpointReached('hello_world', request.remote_addr)
    return "<h1>hello world iseek.</h1>"


@application.route('/time')
def send_time():
    log.endpointReached('time', request.remote_addr)
    print('hello world')
    return {'time': time.time()}

@application.route('/chatbot', methods=['POST', 'GET'])
def chatbot():
    if request.method == 'POST':
        print("Chatbot endpoint reached")

        data = json.loads(request.json)
        
        message = data['textString']
        print(message)
        answer = chat.chatbot_response(message)
        print(answer)
        return answer
    

    if request.method == 'GET':
        return "<h1>Hello world iSeek</h1>"

"""
@application.route('/text', methods=['POST', 'GET'])
def recieveText():
    log.endpointReached('text', request.remote_addr)
    image = objectDetect()
    if request.method == 'POST':
        print("hello world")
        data = request.json
        pic_as_base64 = data['pictureString']
        with open("textToDetect.jpg",'wb') as fh:
            fh.write(base64.b64decode(pic_as_base64))

        imagePath = "./textToDetect.jpg"
        text = image.readText(imagePath)

        os.remove("./textToDetect.jpg")

        log.success()
        return{
            "imageText": text,
        }
    else:
        log.fail(sys.exc_info()[0])
        return "failed check system log"
"""
@application.route('/image', methods=['POST', 'GET'])
def receivePic():
    try:
        log.endpointReached('image',request.remote_addr)
        image = objectDetect()
        print('endpoint reachde')
        if request.method == 'POST':
            print("hello world")
            data = request.json
            pic_as_base64 = data['pictureString']
            with open("imageToDetect.jpg",'wb') as fh:
                fh.write(base64.b64decode(pic_as_base64))


            imagePath = "./imageToDetect.jpg"
            imageDetected, objectList = image.processImage(imagePath)
            objects = ""
            for i in range(len(objectList)):
                objects += objectList[i] +"\n"

            os.remove("./imageToDetect.jpg")
            os.remove("./imageToDetect_yolo3.jpg")
            log.success()
            return {
                "pictureResponse": imageDetected,
                "objects": objects
            }
        if request.method == 'GET':
            return "<h1>Hello world iSeek</h1>"
    except:
        log.fail(str(sys.exec_info()))
        return "failed check system log"

"""
@application.route('/recording', methods=['POST','GET'])
def receiveWav():
    log.endpointReached('recording',request.remote_addr)
    chatbot = chatBot()
    print('endpoint reached')
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                log.write("ERROR:\nNo File Given")
                return "no file added"

            wavFile = request.files['file']

            if wavFile.filename != '':
                wavFile.save(wavFile.filename)
            else:
                return "no file name given"
            
            filePath = "./{}".format(wavFile.filename)
            text = voice.wavToText(filePath)
            
            os.remove("./{}".format(wavFile.filename))
            respond = chatbot.chatbot_response(text)
            log.success()
            return respond

        except:
            log.fail(str(sys.exc_info()))
            return "failed check system log"

    if request.method == 'GET':
        # return "<h1>Hello world iSeek</h1>"
        return chatbot.chatbot_response('hello')







#@application.route('/video',methods=['POST','GET'])
def recieveVid():
    print('endpoint reached')
    if request.method == 'POST':
        v = videoDetect()
        if 'file' not in request.files:
            return "no file added"

        vid = request.files['file']

        if vid.filename != '':
            vid.save(vid.filename)

        filePath = "./{}".format(vid.filename)

        vid = v.processVideo(filePath)

        #os.remove(filePath)

        return{
            "videoResponse": send_file(vid)
        }

"""
if __name__ == "__main__":
    application.run(host='0.0.0.0',port=5001)#,threaded=True)
