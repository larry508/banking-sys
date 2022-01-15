from datetime import date

from flask import Blueprint, render_template, redirect

from common.db import customer
from common.security import admin_view, login_required, get_current_user
from common.app import db
from utils.default_context import get_default_context
from views.index.utils import registration_completed


blueprint = Blueprint('index', __name__)


@blueprint.route('/')
@login_required
def index():
    if get_current_user().user_type == 'ADMIN':
        return redirect('/index/admin')
    return redirect('/index/customer')


@blueprint.route('/index/customer')
@login_required
def home_customer():
    if not registration_completed(get_current_user()):
        return redirect('/self/details')
    context = get_default_context()
    context['customers'] = customer.find_all()
    return render_template('customer/customer_index.html', context=context)



@blueprint.route('/index/admin')
@admin_view
def home_admin():
    context = get_default_context()
    context['customers'] = customer.find_all()
    return render_template('admin/home.html', context=context)