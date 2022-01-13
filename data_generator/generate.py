from datetime import date

import random
from faker import Faker
from hashlib import sha256
from common.models import Address, Contact, User, Customer

from common.app import db

sex_dict = {
    0: 'M',
    1: 'F'
}

fake = Faker()
for _ in range(133):
    sex = sex_dict[random.randint(0, 1)]
    first_name = fake.first_name_male() if sex == 'M' else fake.first_name_female()
    middle_name = (fake.first_name_male() if sex == 'M' else fake.first_name_female()) if random.randint(0, 2) == 1 else ""
    last_name = fake.last_name()
    birth_date = fake.date_between(date(1960, 1, 1), date(2006, 1,1))

    user_type = "ADMIN" if random.randint(1, 10) == 1 else "CUSTOMER"
    username = fake.user_name()
    email = fake.email()
    password_hash = sha256(fake.password().encode('utf-8')).hexdigest()
    register_date = fake.date_between(date(2010, 1, 1), date(2022, 1, 7))
    last_login = fake.date_between(register_date, date(2022, 1, 7))

    contact_email = fake.email()
    phone_number = str(random.randint(300, 700)) + '-' + str(random.randint(200, 800)) + '-' + str(random.randint(100, 800))

    country_code = fake.country_code()
    city = fake.city()
    zip_code = fake.zipcode()
    street_name = fake.street_name()
    street_number = random.randint(1,300)
    apartment_number = random.randint(1, 100) if random.randint(1, 5) == 1 else None

    new_address = Address(
        country_code=country_code,
        city=city,
        zip_code=zip_code,
        street_name=street_name,
        street_number=street_number,
        apartment_number=apartment_number
    )

    new_contact = Contact(
        email=contact_email,
        phone_number=phone_number
    )

    new_user = User(
        user_type=user_type,
        username=username,
        email=email,
        password_hash=password_hash,
        registration_date=register_date,
        last_login=last_login
    )

    db.session.add(new_address)
    db.session.add(new_contact)
    db.session.add(new_user)

    db.session.commit()

    new_customer = Customer(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        sex=sex,
        birth_date=birth_date,
        address_id=new_address.address_id,
        contact_id=new_contact.contact_id,
        user_id=new_user.user_id
    )
    db.session.add(new_customer)
    db.session.commit()
        
