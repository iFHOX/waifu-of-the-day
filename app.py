from flask import Flask
from flask import render_template
import json
from pathlib import Path
from datetime import date, timedelta

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "characters.json", "r", encoding="utf-8") as file:
    data = json.load(file)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', c=datecharacter(date.today()))


def datecharacter(day):
    chosencharacter = day.toordinal() % len(data)
    return data[chosencharacter]
