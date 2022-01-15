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
from views.self.utils import get_customer_details_prefill, update_address_from_form, update_contact_from_form, update_customer_from_form
from views.index.utils import registration_completed


blueprint = Blueprint('self', __name__)


@blueprint.route('/details', methods=['POST', 'GET'])
@login_required
def details():
    if request.method == 'GET':
        messages = []
        prefill = {}
        user = get_current_user()
        customer = db_customer.find_by_user(user)
        address = db_address.find_by_user(user)
        contact = db_contact.find_by_user(user)
        prefill = get_customer_details_prefill(address, contact, customer)
        if not customer:
            messages.append(MESSAGES['FILL_CUSTOMER_INFORMATION'])
        return render_template('self/details.html', prefill=prefill, messages=messages, context=get_default_context())
    
    if request.method == 'POST':
        messages = []
        db = get_db()
        form = request.form
        user = get_current_user()
        customer: Customer = db_customer.find_by_user(user)

        if customer:
            update_customer_from_form(db, customer, form)
        else:
            customer = Customer(
                first_name = form['firstName'],
                middle_name = form['middleName'],
                last_name = form['lastName'],
                sex = form['gender'],
                birth_date = form['birthdate'],
                user_id = user.user_id
            )
            customer = db_customer.create(customer)

        address: Address = db_address.find_by_user(user)
        if address:
            update_address_from_form(db, address, form)
        else:
            address = Address(
                customer_id = customer.customer_id,
                country_code = form['countryCode'],
                city = form['city'],
                zip_code = form['zipCode'],
                street_name = form['streetName'],
                street_number = form['streetNumber'],
                apartment_number = form['apartmentNumber']
            )
            address: Address = db_address.create(address)


        contact: Contact = db_contact.find_by_user(user)
        if contact:
            update_contact_from_form(db, contact, form)
        else:
            contact = Contact(
                customer_id = customer.customer_id,
                email = form['email'],
                phone_number = form['phoneNumber']
            )
            db_contact.create(contact)

        messages.append(MESSAGES['PROFILE_UPDATED'])

        return render_template('self/details.html', prefill=get_customer_details_prefill(address, contact, customer), messages=messages, context=get_default_context())

        