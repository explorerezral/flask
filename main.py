from flask import Flask,request
import os
import json
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'

@app.route('/chat', methods=['GET','POST'])
def form():
    bot = chat()
    if request.method == 'GET':
        return 'This is a GET request to /json'
    if request.method == 'POST':
        data = json.loads(request.data) # 将json字符串转为dict
        key = data['key']
        del data['key']
        
        response = chat.create_chatgpt_request(key,data)
        
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

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
