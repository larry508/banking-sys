from datetime import date
from hashlib import sha256

from flask import Blueprint, make_response, redirect, render_template, request

from common.app import db
from common.db import customer as db_customer
from common.db import user as db_user
from common.db import customer_details as db_customer_details
from common.models import Customer, User
from common.security import admin_view, verify_user, generate_auth_token, hash_sha256, is_authenticated, login_required
from utils.string_tables import ERRORS
from utils.default_context import get_default_context

from sqlalchemy import Column, Table
blueprint = Blueprint('admin', __name__)




@blueprint.route('/customers', methods=['GET'])
@admin_view
def all_customers():
    if request.method == 'GET':
        customers = db_customer.find_all()
        return render_template('admin/customers.html', context=get_default_context(), customers=customers)


@blueprint.route('/customer-details', methods=['GET'])
@admin_view
def all_customer_details():
    if request.method == 'GET':
        customer_details = db_customer_details.find_all()
        return render_template('admin/customer_details.html', context=get_default_context(), customer_details=customer_details)


@blueprint.route('/users', methods=['GET'])
@admin_view
def all_users():
    if request.method == 'GET':
        users = db_user.find_all()
        return render_template('admin/users.html', context=get_default_context(), users=users)


@blueprint.route('/customers/delete/<id>', methods=['POST'])
@admin_view
def delete_user_by_id(id: str):
    if request.method == 'POST':
        db_customer.delete_by_id(id)
        return redirect('/admin/customers') # in future - just reload previous page