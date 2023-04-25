from flask import Flask,request
import os
import json
import requests
import logging
import openai

app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


#假设每颗药丸比正常药丸中x克，分别从一号瓶，二号瓶，三号瓶，四号瓶中拿出一颗两颗三颗四颗药丸放到天平左边，再从一号瓶中拿出十颗药丸放到天平右边，如果右侧重则是一号瓶药品变质，如果左侧比右侧中2x克是2号瓶变质，3x克是3号瓶变质，4x克是4号瓶变质



@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'

@app.route('/chat', methods=['POST'])
def text_process():
    bot = chat()
    if request.method == 'GET':
        return 'This is a GET request to /chat'
    if request.method == 'POST':
        data = json.loads(request.data)
        key = data['key']
        del data['key']
        response = chat.create_chatgpt_request(key,data)
        return response
    


@app.route('/audio' ,methods=['GET','POST'])
def audio_process():
    bot = chat()
    if request.method == 'GET':
        return "this audio test"
    if request.method == 'POST':

        request_data = request.get_data().decode('utf-8', errors='ignore')

        print("Request Headers:")
        # for header in request.headers:
        #     print(f"{header[0]}: {header[1]}")
        for header in request.headers:
            if(header[0] == "Authorization"):  
                key = header[1].replace('Bearer ','')

       # key = request.form.get('key')
        # data = request.form.to_dict()
        for file_name in request.files:
            file = request.files.get(file_name) 
            
        #file = request.files.get('1.wav')
        print(file)

        response = chat.whisper_transcribe(key,file)
        #return "11"
        return response
    
class chat ():
    def create_chatgpt_request(OPENAI_API_KEY,data):
        url = "https://api.openai.com/v1/chat/completions"
        model = "gpt-3.5-turbo"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + OPENAI_API_KEY
        }
        # character = "Humor"
        #messages=[{"role":"system", "content": "You are a helpful assistant and answer every question by one sentence."},
        print(data)
        response_json = requests.post(url, headers=headers, json=data).json()
        return response_json

    def whisper_transcribe(OPENAI_API_KEY,audio_file):
        url="https://api.openai.com/v1/audio/transcriptions"
        headers = {
            # "Content-Type": "multipart/from-data",
            "Authorization": "Bearer " + OPENAI_API_KEY,
        }

        # files = {
        #     'file': audio_file,
        #     'model': (None, "whisper-1"),
        # }
        # response = requests.post(url, headers=headers, files=files)
        # #response = requests.request(url,data)
        #files = open("record.wav",'rb')
        
        files = {
                'file': (audio_file.filename, audio_file.read()),
                'model': (None, "whisper-1"),
                 }
        openai.api_key = OPENAI_API_KEY
        response = requests.post(url, headers=headers, files=files)
        # response = openai.Audio.transcribe("whisper-1", files)
        #return response
        return response.json()

    def whisper_translate(OPENAI_API_KEY,audio_file):
        url="https://api.openai.com/v1/chat/translations"
        headers = {
            # "Content-Type": "application/json",
            "Authorization": "Bearer " + OPENAI_API_KEY
        }

        files = {
            'file': open(audio_file, "rb"),
            'model': (None, "whisper-1"),
        }
        response = requests.post(url, headers=headers, files=files)

        return response.json()['text']


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
