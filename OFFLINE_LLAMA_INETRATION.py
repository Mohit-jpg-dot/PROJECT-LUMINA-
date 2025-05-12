from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/get-answer', methods=['GET'])
def get_answer():
    text = request.args.get('text')
    response = requests.post('https://api.laion.ai/answer', json={'input': text})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
