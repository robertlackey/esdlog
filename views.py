from flask import Blueprint, render_template, request, redirect
from models import db, ESDForm
from forms import SubmitForm
from datetime import datetime, date, timedelta
from flask_paginate import Pagination, get_page_args

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = SubmitForm()
    search_query = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    if search_query:
        # Search for ESDForm objects containing the search query
        data = ESDForm.query.filter(ESDForm.type.ilike(f'%{search_query}%') |
                                    ESDForm.company.ilike(f'%{search_query}%') |
                                    ESDForm.position.ilike(f'%{search_query}%') |
                                    ESDForm.method.ilike(f'%{search_query}%') |
                                    ESDForm.contact_info.ilike(f'%{search_query}%') |
                                    ESDForm.notes.ilike(f'%{search_query}%')
                                    ).paginate(page=page, per_page=10)
    else:
        # Retrieve all ESDForm objects with pagination
        data = ESDForm.query.paginate(page=page, per_page=10)
    return render_template('index.html', form=form, data=data, search_query=search_query)


@bp.route('/form')
def form():
    form = SubmitForm()
    return render_template('form.html', form=form)

@bp.route('/submit', methods=['POST'])
def submit():
    type = request.form['type']
    company = request.form['company']
    position = request.form['position']
    method = request.form['method']
    contact_info = request.form['contact_info']
    date = request.form['date']
    notes = request.form['notes']
    new_form = ESDForm(type, company, position, method, contact_info, date, notes)
    db.session.add(new_form)
    db.session.commit()
    return redirect('form')

@bp.route('/items/two-weeks-sunday')
def show_items_last_two_weeks_sunday():
    # Calculate start and end dates for the previous 2 weeks
    today = datetime.today().date()
    last_sunday = today - timedelta(days=today.weekday() + 1)
    two_weeks_ago = last_sunday - timedelta(days=7, weeks=1)
    start_date = two_weeks_ago

    # Get ESDForm objects within the 2-week period
    data = ESDForm.query.filter(ESDForm.date.between(two_weeks_ago, last_sunday)).order_by(ESDForm.date.asc()).all()

    # Create a list of start and end dates for each week
    week_dates = []
    while start_date <= last_sunday:
        week_dates.append((start_date, start_date + timedelta(days=7)))
        start_date += timedelta(days=7)

    return render_template('items_by_week.html', data=data, week_dates=week_dates)

