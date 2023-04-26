from flask import Flask,request
import os
import json
import requests
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')






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
        model = data['model']
        content = data['messages'][0]['content']
        response = chat.create_chatgpt_request(key,model,content)
        return response
    


@app.route('/audio' ,methods=['GET','POST'])
def audio_process():
    bot = chat()
    if request.method == 'GET':

        return "this audio test"
    if request.method == 'POST':
        model = "gpt-3.5-turbo"



        for header in request.headers:
            if(header[0] == "Authorization"):  
                key = header[1].replace('Bearer ','')

       # key = request.form.get('key')
        # data = request.form.to_dict()
        for file_name in request.files:
            file = request.files.get(file_name) 
            
        #file = request.files.get('1.wav')
        logger.info(file)

        response_stt = chat.whisper_transcribe(key,file)
        response_stt_json = response_stt.json()
        if(response_stt.status_code != 200):
             
             response_stt_json['model'] = "whisper"
             logger.warn(response_stt_json)
             
             return response_stt_json
        
        else:
            logger.info(response_stt_json)
            response_gpt = chat.create_chatgpt_request(key,model,response_stt)
            response_gpt_json = response_gpt.json()

            if(response_gpt.status_code != 200):

                response_gpt_json['model'] = model
                logger.warn(response_gpt_json)

            else:

                response_gpt_json['whisper'] = response_stt_json['text']
                logger.info(response_gpt)

            return response_gpt_json
    
class chat ():
    def create_chatgpt_request(OPENAI_API_KEY, model, content):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + OPENAI_API_KEY
        }

        messages=[{"role":"user", "content": content}]
        data = {
        "model":model,
        "messages": messages,
        }
        print(data)
        response = requests.post(url, headers=headers, json=data)
 
        return response

    def whisper_transcribe(OPENAI_API_KEY,audio_file):
        url="https://api.openai.com/v1/audio/transcriptions"
        headers = {
            # "Content-Type": "multipart/from-data",
            "Authorization": "Bearer " + OPENAI_API_KEY,
        }


        files = {
                'file': (audio_file.filename, audio_file.read()),
                'model': (None, "whisper-1"),
                 }
        response = requests.post(url, headers=headers, files=files)
        

        return response

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
