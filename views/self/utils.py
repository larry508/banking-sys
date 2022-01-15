from common.models import Address, Contact, Customer, User



def get_customer_details_prefill(address: Address, contact: Contact, customer: Customer):
    prefill = {}
    if customer:
        prefill['first_name'] = customer.first_name
        prefill['middle_name'] = customer.middle_name
        prefill['last_name'] = customer.last_name
        prefill['gender'] = customer.sex
        prefill['birth_date'] = customer.birth_date
    if address:
        prefill['country_code'] = address.country_code
        prefill['city'] = address.city
        prefill['zip_code'] = address.zip_code
        prefill['street_name'] = address.street_name
        prefill['street_number'] = address.street_number
        prefill['apartment_number'] = address.apartment_number
    if contact:
        prefill['email'] = contact.email
        prefill['phone_number'] = contact.phone_number

    return prefill


def update_customer_from_form(db, customer, form):
    customer.first_name = form['firstName']
    customer.middle_name = form['middleName']
    customer.last_name = form['lastName']
    customer.sex = form['gender']
    customer.birth_date = form['birthdate']
    db.session.commit()


def update_address_from_form(db, address, form):
    address.country_code = form['countryCode']
    address.city = form['city']
    address.zip_code = form['zipCode']
    address.street_name = form['streetName']
    address.street_number = form['streetNumber']
    address.apartment_number = form['apartmentNumber']
    print(address)
    db.session.commit()
    print(address)


def update_contact_from_form(db, contact, form):
    contact.email = form['email']
    contact.phone_number = form['phoneNumber']
    db.session.commit()