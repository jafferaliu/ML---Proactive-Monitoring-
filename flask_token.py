from flask import Flask

app = Flask(__name__)

@app.route('/')

def content():
    with open('/root/access_token.txt', 'r') as f:
        data=f.read()
    return data

if __name__ =='__main__':  
    app.run(host='0.0.0.0', port=80)
