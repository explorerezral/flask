from flask import Flask,jsonify,request
import os
import json

app = Flask(__name__)

#@app.route('/', methods=['GET'])
#def home():
    #return 'Hello, World!'

@app.route('/json', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return 'This is a GET request to /json'
    elif request.method == 'POST':
        data = json.loads(request.data) # 将json字符串转为dict
        name = data['name']
        age = data['age']
        return "user_name = %s, user_age = %s" % (name,age)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
