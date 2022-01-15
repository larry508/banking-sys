from datetime import date

from flask import Blueprint, render_template, redirect, request

from common.app import get_db
from common.db import address as db_address
from common.db import contact as db_contact
from common.db import customer as db_customer
from common.db import user as db_user
from common.models import Address, Contact, Customer, Address
from common.security import admin_view, login_required, get_current_user
from utils.default_context import get_default_context
from utils.string_tables import MESSAGES
from views.index.utils import registration_completed


blueprint = Blueprint('customer', __name__)


