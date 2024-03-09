from flask import render_template
from app import app
from app import ct_client
import datetime

public_calendar_ids = [
        80,  # Sonntagsschule
        89,  # Jugend
        77,  # Chor
        86,  # Konfa
        83,  # Reli
        27,  # Gottesdienste
        30,  # Gemeinde
        74,  # Instrumental
        #37,  # Bezirkstermine
    ]


def get_calendar_entries(next_n_days):
    # enable to see all calendar ids
    # for c in ct_client.calendars.list():
    #     print(c.name, c.id, c.color)
    entries = ct_client.calendars.appointments(public_calendar_ids,
                                               datetime.datetime.now(),
                                               datetime.datetime.now() + datetime.timedelta(days=next_n_days))
    # filter out entries with duplicate names and entries with the name Gottesdienst
    seen_entries = []
    filtered_entries = []
    for e in entries:
        if (e.caption, e.startDate) not in seen_entries and e.caption != "Gottesdienst":
            filtered_entries.append(e)
            seen_entries.append((e.caption, e.startDate))
    return filtered_entries


def get_calendar_colors():
    return [(c.id, c.color) for c in ct_client.calendars.list() if c.id in public_calendar_ids]


@app.route('/')
@app.route('/index')
def index():
    calendar_entries = get_calendar_entries(next_n_days=28)
    calendar_colors = get_calendar_colors()
    # print(calendar_entries)
    return render_template('index.html', entries=calendar_entries, colors=calendar_colors)
