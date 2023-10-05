# app.py
from flask import Flask, render_template, request, jsonify
from post_token import FakeGPT

app = Flask(__name__)
messages = []
fakegpt = FakeGPT()

@app.route('/')
def index():
    return render_template('chat.html', messages=messages)

# @app.route('/send_message', methods=['POST'])
# def send_message():
#     message = request.form.get('message')
#     messages.append(message)
#     return jsonify({'status': 'success'})

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')

    # 这里是一个简单的回复示例。在实际项目中，你可能会根据接收到的消息内容或其他逻辑来生成回复。
    input = "请扮演大慈大悲的观世音菩萨，现在请你尽可能用佛教的说法来回复用户这句话："+user_message
    server_reply = fakegpt.get_result(input)

    return jsonify(status='success', reply=server_reply)


if __name__ == '__main__':
    app.run(port=6060)