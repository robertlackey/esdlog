from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, ESDForm
from forms import SubmitForm
from datetime import datetime, date, timedelta

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
    # Calculate the date of the most recent Sunday
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    last_sunday = today - timedelta(days=days_since_sunday)

    # Calculate the date of the Sunday two weeks before the most recent Sunday
    two_weeks_ago = last_sunday - timedelta(weeks=2)

    # Calculate the date of the most recent Saturday
    last_saturday = last_sunday + timedelta(days=6)

    # Get ESDForm objects within the 2-week period
    data = ESDForm.query.filter(ESDForm.date.between(two_weeks_ago, last_saturday)).order_by(ESDForm.date.asc()).all()

    # Create a list of start and end dates for each week
    week_dates = []
    start_date = two_weeks_ago
    while start_date <= last_saturday:
        end_date = start_date + timedelta(days=6)
        week_dates.append((start_date, end_date))
        start_date += timedelta(days=7)

    return render_template('items_by_week.html', data=data, week_dates=week_dates)


@bp.route('/list')
def list():
    forms = ESDForm.query.order_by(ESDForm.id.desc()).all()
    return render_template('list.html', forms=forms)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = SubmitForm()

    items = ESDForm.query.get_or_404(id)

    form.type.default = items.type
    form.company.default = items.company
    form.position.default = items.position
    form.method.default = items.method
    form.contact_info.default = items.contact_info
    form.date.default = items.date
    form.notes.default = items.notes

    form.process()

    if request.method == 'POST':
        items.type = request.form['type']
        items.company = request.form['company']
        items.position = request.form['position']
        items.method = request.form['method']
        items.contact_info = request.form['contact_info']
        items.date = request.form['date']
        items.notes = request.form['notes']
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('routes.index'))

    return render_template('edit.html', form=form, items=items)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    form = ESDForm.query.get_or_404(id)
    db.session.delete(form)
    db.session.commit()
    flash('Form has been deleted.')
    return redirect(url_for('routes.list'))
