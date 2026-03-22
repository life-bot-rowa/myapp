import os
from datetime import datetime
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    name_result = None
    future_result = None
    if request.method == "POST":
        name = request.form["name"]
        day = request.form["day"]
        month = request.form["month"]
        year = request.form["year"]
        birthdate = f"{day} {month} {year}"
        today = datetime.now().strftime("%d %B %Y")

        r1 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Дай нумерологическую характеристику имени {name}. Кратко, 3-4 предложения."}]
        )
        name_result = r1.choices[0].message.content

        r2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Сегодня {today}. Человека зовут {name}, дата рождения {birthdate}. Что его ожидает в ближайший месяц начиная с сегодняшней даты? Нумерология и астрология. Кратко, 3-4 предложения."}]
        )
        future_result = r2.choices[0].message.content

    return render_template("index.html", name_result=name_result, future_result=future_result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
