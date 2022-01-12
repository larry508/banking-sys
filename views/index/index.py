from datetime import date

from flask import Blueprint, render_template

from common.db import customer
from common.security import login_required
from common.service import db
from utils.default_context import get_default_context

blueprint = Blueprint('index', __name__)

@blueprint.route('/')
@login_required
def index():
    context = get_default_context()
    context['customers'] = customer.findAll()
    return render_template('index.html', context=context)
