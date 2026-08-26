import requests
from flask import Flask, request

app = Flask(__name__)
app.json.ensure_ascii = False

TELEGRAM_TOKEN = "8988065911:AAHE-Y1YMhFjW-YcuEqZjn5p00JejHCPLbg"
GROQ_KEY = "gsk_حط_المفتاح_بتاعك_هنا" # الصق مفتاح Groq بتاعك هنا

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        user_message = data['message']['text']
        send_message(chat_id, "ثواني بفكر... 🤔")
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": user_message}]}
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        reply = response.json()['choices'][0]['message']['content']
        send_message(chat_id, reply)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
