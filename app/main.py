from flask import Flask, render_template, request, url_for, redirect
from collections import namedtuple
from itertools import starmap

app = Flask(__name__)


Period = namedtuple('Period', ['years', 'months', 'days'])

# TODO defensiveness
def parse(data):
    return starmap(Period, map(str.split, data.splitlines()))


def to_days(p):
    return int(p.years) * 365 + int(p.months) * 30 + int(p.days)


def add_up(periods):
    return sum(map(to_days, periods))


def to_period(days):
    DAYS_IN_YEAR = 365
    DAYS_IN_MONTH = 30
    years = days // DAYS_IN_YEAR
    days %= DAYS_IN_YEAR
    months = days // DAYS_IN_MONTH
    days %= DAYS_IN_MONTH
    return Period(years, months, days)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html.j2')
    elif request.method == 'POST':
        calculations = request.form['calculations']
        result = to_period(add_up(parse(calculations)))
        return render_template('index.html.j2', calculations=calculations, result=result)
    else:
        print('wrong')

