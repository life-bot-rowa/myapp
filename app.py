import os
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        name = request.form["name"]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Привет! Меня зовут {name}. Скажи мне что-нибудь интересное про моё имя."}]
        )
        answer = response.choices[0].message.content
    return render_template("index.html", greeting=answer)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
