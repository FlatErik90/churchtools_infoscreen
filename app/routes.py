import os

from flask import render_template
from app import app
from app import ct_client
import datetime
from pytz import timezone


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
        # 99,  # Test-Kalender
    ]

tz = timezone("Europe/Berlin")


def get_calendar_entries(next_n_days):
    # enable to see all calendar ids
    # for c in ct_client.calendars.list():
    #     print(c.name, c.id, c.color)
    now = datetime.datetime.now(tz=tz)
    end = now + datetime.timedelta(days=next_n_days)
    entries = ct_client.calendars.appointments(public_calendar_ids, now, end)
    # filter out appointments that are longer ago than half an hour and
    # filter out entries with duplicate names and entries with the name Gottesdienst (unless note is filled)
    seen_entries = []
    filtered_entries = []
    for e in entries:
        # print(e.caption, e.startDate.astimezone(tz) + datetime.timedelta(minutes=30) >= now)
         if (e.caption, e.startDate) not in seen_entries \
                and (e.caption != "Gottesdienst" or e.note is not None) \
                and e.startDate.astimezone(tz) + datetime.timedelta(minutes=30) >= now:
            filtered_entries.append(e)
            seen_entries.append((e.caption, e.startDate))
    for entry in filtered_entries:
        if entry.calendar.id == 27:
            entry.calendar.name = ""
        elif entry.calendar.id == 30:
            entry.calendar.name = ""
        elif entry.calendar.id == 86:
            entry.calendar.name = "Konfirmanden"
        elif entry.calendar.id == 83:
            entry.calendar.name = "Reli"
        elif entry.calendar.id == 74:
            entry.calendar.name = "Instrumental"

    return filtered_entries


def get_calendar_entries_mask(calendar_entries):
    mask = [True]
    current_date = calendar_entries[0].startDate
    for entry in calendar_entries[1:]:
        mask.append(entry.startDate.date() != current_date.date())
        current_date = entry.startDate
    return mask


def get_calendar_colors():
    return [(c.id, c.color) for c in ct_client.calendars.list() if c.id in public_calendar_ids]


def get_image_paths():
    return os.listdir("app/static/gallery_images")


@app.route('/')
@app.route('/index')
def index():
    calendar_entries = get_calendar_entries(28)
    calender_entries_mask = get_calendar_entries_mask(calendar_entries)
    calendar_colors = get_calendar_colors()
    image_paths = get_image_paths()
    gallery_interval = 5000  # milliseconds = 1/1000 seconds
    gallery_mode = True
    max_image_height = 700  # pixels
    max_entries = 15
    # print(ct_client.wiki.categories())
    # pages = ct_client.wiki.pages(31)
    # for page in pages:
    #     real_page = ct_client.wiki.page(31, page.identifier)
    #     print(real_page.text)
    #     print(page.text, page.wikiCategory.name)
    # print(calendar_entries)
    # print(calender_entries_mask)
    # print(calendar_colors)
    # print(image_paths)
    return render_template('index.html',
                           entries=calendar_entries[:max_entries],
                           date_mask=calender_entries_mask[:max_entries],
                           colors=calendar_colors,
                           gallery=gallery_mode,
                           images=image_paths,
                           max_image_height=max_image_height,
                           interval=gallery_interval)


@app.route('/index_full')
def index_full():
    calendar_entries = get_calendar_entries(28)
    calender_entries_mask = get_calendar_entries_mask(calendar_entries)
    calendar_colors = get_calendar_colors()
    image_paths = get_image_paths()
    gallery_interval = 5000  # milliseconds = 1/1000 seconds
    gallery_mode = False
    max_image_height = 700  # pixels
    max_entries = 8
    return render_template('index.html',
                           entries=calendar_entries[:max_entries],
                           date_mask=calender_entries_mask[:max_entries],
                           colors=calendar_colors,
                           gallery=gallery_mode,
                           images=image_paths,
                           max_image_height=max_image_height,
                           interval=gallery_interval)
