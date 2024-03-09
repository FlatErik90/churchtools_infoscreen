from flask import render_template
from app import app
from app import ct_client
import datetime


def get_calender_entries(next_n_days=21):
    public_calender_ids = [
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
    # enable to see all calender ids
    # for c in ct_client.calendars.list():
    #     print(c.name, c.id)
    entries = ct_client.calendars.appointments([c.id for c in ct_client.calendars.list()
                                                if c.id in public_calender_ids],
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


@app.route('/')
@app.route('/index')
def index():
    calender_entries = get_calender_entries()
    print(calender_entries)
    return render_template('index.html', title='Home', entries=calender_entries)
