from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/f', methods=['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        return 'This is a GET request to /'
    elif request.method == 'POST':
        return 'This is a POST request to /’  
    #return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})




if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
