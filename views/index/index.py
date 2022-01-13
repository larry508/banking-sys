from datetime import date

from flask import Blueprint, render_template, redirect

from common.db import customer
from common.security import admin_view, login_required, get_current_user
from common.app import db
from utils.default_context import get_default_context
from views.index.utils import registration_completed


blueprint = Blueprint('index', __name__)


# @blueprint.route('/')
# @login_required
# def index():
#     context = get_default_context()
#     context['customers'] = customer.findAll()
#     return render_template('index.html', context=context)

@blueprint.route('/')
@login_required
def index():
    if get_current_user().user_type == 'ADMIN':
        return redirect('/index/admin')
    return redirect('/index/customer')


@blueprint.route('/index/customer')
@login_required
def home_customer():
    registered = True
    if not registration_completed(get_current_user()):
        registered = False
    context = get_default_context()
    context['customers'] = customer.findAll()
    return render_template('customer_index.html', context=context, registered=registered)



@blueprint.route('/index/admin')
@admin_view
def home_admin():
    registered = True
    if not registration_completed(get_current_user()):
        registered = False
    context = get_default_context()
    context['customers'] = customer.findAll()
    return render_template('customer_index.html', context=context, registered=registered)