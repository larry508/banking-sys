from datetime import date, datetime, timedelta
from email.mime import base
import random
import string
from typing import List

from faker import Faker
from hashlib import sha256

from common.models import *
from common.app import create_app, db
from config import DB_URI


def generate_customers(app):
    gender_dict: dict = {
        0: 'M',
        1: 'F'
    }
    with app.app_context():
        fake = Faker()
        for _ in range(133):
            gender = gender_dict[random.randint(0, 1)]
            customer_id = ""
            for _ in range(11): customer_id += str(random.randint(0, 9))
            first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
            middle_name = (fake.first_name_male() if gender == 'M' else fake.first_name_female()) if random.randint(0, 2) == 1 else ""
            last_name = fake.last_name()
            birth_date = fake.date_between(date(1960, 1, 1), date(2006, 1,1))

            user_type = "ADM" if random.randint(1, 10) == 1 else "CST"
            username = fake.user_name()
            email = fake.email()
            password_hash = sha256(fake.password().encode('utf-8')).hexdigest()
            register_date = fake.date_between(date(2010, 1, 1), datetime.now().date())
            last_login = fake.date_between(register_date, datetime.now().date())

            contact_email = fake.email()
            phone_number = str(random.randint(300, 700)) + '-' + str(random.randint(200, 800)) + '-' + str(random.randint(100, 800))

            country_code = fake.country_code()
            city = fake.city()
            zip_code = fake.zipcode()
            street_name = fake.street_name()
            street_number = random.randint(1,300)
            apartment_number = random.randint(1, 100) if random.randint(1, 5) == 1 else None

            new_user = User(
                user_type=user_type,
                username=username,
                email=email,
                password_hash=password_hash,
                registration_date=register_date,
                last_login=last_login
            )
            db.session.add(new_user)
            db.session.commit()


            new_customer = Customer(
                customer_id=customer_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                gender=gender,
                birth_date=birth_date,
                user_id=new_user.user_id
            )
            db.session.add(new_customer)
            db.session.commit()

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


            db.session.add(new_address)
            db.session.add(new_contact)
            db.session.commit()
            new_customer.address_id = new_address.address_id
            new_customer.contact_id = new_contact.contact_id
            db.session.commit()


def generate_account_types(app):
    with app.app_context():
        yng = AccountType(
            code='YNG',
            description='For people under 18 years old',
            interest_rate=float(0.20),
            monthly_fee=0
        )
        db.session.add(yng)

        basic = AccountType(
            code='BSC',
            description='Basic account with small fee',
            interest_rate=float(0),
            monthly_fee=float(2.59)
        )
        db.session.add(basic)

        savings = AccountType(
            code='SVG',
            description='Savings account',
            interest_rate=float(1.98),
            monthly_fee=0
        )
        db.session.add(savings)

        db.session.commit()


def generate_user_types(app):
    with app.app_context():
        customer = UserType(code='CST', description='Customer')
        admin = UserType(code='ADM', description='admin')
        db.session.add(customer)
        db.session.add(admin)
        db.session.commit()


def generate_accounts(app):
    account_types_dict = {
        0: 'BSC',
        1: 'SVG',
        2: 'YNG'
    }   

    with app.app_context():
        customers = Customer.query.all()
        fake = Faker()
        for customer in customers:
            customer_id = customer.customer_id
            account_type = 'YNG' if datetime.now() - datetime(customer.birth_date.year, customer.birth_date.month, customer.birth_date.day) < timedelta(weeks=864) else account_types_dict[random.randint(0, 1)]
            account_number = "".join(random.choice(string.digits) for _ in range(26))
            balance = float(random.randint(0,10000))
            opened_date = fake.date_between(User.query.filter_by(user_id=customer.user_id).first().registration_date, datetime.now().date())

            account = Account(
                account_number=account_number,
                customer_id=customer_id,
                account_type=account_type,
                balance=balance,
                opened_date=opened_date
            )
            db.session.add(account)
            db.session.commit()

def generate_incomes(app):
    with app.app_context():
        customers = Customer.query.all()
        fake = Faker()
        for customer in customers:
            customer_id = customer.customer_id
            company_name = fake.company()
            yearly_salary = random.randint(40000, 300000)
            paycheck_day = random.randint(1,15)

            income = Income(
                customer_id=customer_id,
                company_name=company_name,
                yearly_salary=yearly_salary,
                paycheck_day=paycheck_day
            )

            db.session.add(income)

        db.session.commit()


def generate_card_types(app):
    with app.app_context():
        debit = CardType(
            code='DBT',
            description='Debit card',
            monthly_fee=4,
        )
        credit = CardType(
            code='CRD',
            description='Credit card',
            monthly_fee=1
        )
        db.session.add(debit)
        db.session.add(credit)
        db.session.commit()
                
def generate_cards(app):
    card_types: dict = {
        0: 'DBT',
        1: 'CRD'
    }

    with app.app_context():
        accounts = Account.query.all()
        fake = Faker()
        for account in accounts:
            account: Account
            account_number = account.account_number
            card_type = card_types[random.randint(0,1)]
            card_number = ""
            for _ in range(16): card_number += str(random.randint(0, 9))
            activation_date = fake.date_between(date(year=1980, month=1, day=1), datetime.now(timezone.utc).date())
            expire_date = activation_date + timedelta(weeks=192)
            cvv_hash = sha256(str(random.randint(100,999)).encode('utf-8')).hexdigest()
            
            card = Card(
                account_number=account_number,
                card_type=card_type,
                card_number=card_number,
                activation_date=activation_date,
                expire_date=expire_date,
                cvv_hash=cvv_hash
            )
            db.session.add(card)
        db.session.commit()

def generate_student_loans(app):
    with app.app_context():
        customers: List[Customer] = Customer.query.all()
        customers_amount = len(customers)
        fake = Faker()
        for _ in range(30):
            customer_id = customers[random.randint(0, customers_amount - 1)].customer_id
            starting_date = fake.date_between(date(year=1980, month=1, day=1), datetime.now(timezone.utc).date())
            ending_date = starting_date + timedelta(weeks=random.randint(1,5)*12*4)
            next_payment = datetime.now(timezone.utc).date().replace(day=random.randint(1, 28))
            payed_off = random.randint(0, 1)

            loan = Loan(
                customer_id=customer_id,
                starting_date=starting_date,
                ending_date=ending_date,
                next_payment=next_payment,
                payed_off=payed_off
            )
            db.session.add(loan)
            db.session.commit()

            interest_rate = random.uniform(0, 5)
            total_owed = random.randint(2000, 30000)
            installment = total_owed / ((ending_date.year - starting_date.year) * 12 + ending_date.month - starting_date.month) * interest_rate / 100
            paid_amount = random.randint(0, total_owed)

            student_loan = StudentLoan(
                loan_id = loan.loan_id,
                interest_rate = interest_rate,
                total_owed = total_owed,
                installment = installment,
                paid_amount = paid_amount
            )
            db.session.add(student_loan)
            db.session.commit()

def generate_mortgages(app):
    with app.app_context():
        customers: List[Customer] = Customer.query.all()
        customers_amount = len(customers)
        fake = Faker()
        for _ in range(30):
            customer_id = customers[random.randint(0, customers_amount - 1)].customer_id
            starting_date = fake.date_between(date(year=1980, month=1, day=1), datetime.now(timezone.utc).date())
            ending_date = starting_date + timedelta(weeks=random.randint(5,30)*12*4)
            next_payment = datetime.now(timezone.utc).date().replace(day=random.randint(1, 28))
            payed_off = random.randint(0, 1)

            loan = Loan(
                customer_id=customer_id,
                starting_date=starting_date,
                ending_date=ending_date,
                next_payment=next_payment,
                payed_off=payed_off
            )
            db.session.add(loan)
            db.session.commit()

            interest_rate = random.uniform(0, 5)
            total_owed = random.randint(100000, 600000)
            installment = total_owed / ((ending_date.year - starting_date.year) * 12 + ending_date.month - starting_date.month) * interest_rate / 100
            paid_amount = random.randint(0, total_owed)

            mortgage = Mortgage(
                loan_id = loan.loan_id,
                interest_rate = interest_rate,
                total_owed = total_owed,
                installment = installment,
                paid_amount = paid_amount
            )
            db.session.add(mortgage)
            db.session.commit()


def generate_deposits(app):
    with app.app_context():
        customers: List[Customer] = Customer.query.all()
        customers_amount = len(customers)
        fake = Faker()
        for _ in range(30):
            customer_id = customers[random.randint(0, customers_amount - 1)].customer_id
            interest_rate = random.uniform(0, 5)
            base_money = random.randint(10000, 150000)
            starting_date = fake.date_between(date(year=1980, month=1, day=1), datetime.now(timezone.utc).date())
            ending_date = starting_date + timedelta(weeks=random.randint(2,30)*12*4)

            deposit = Deposit(
                customer_id=customer_id,
                interest_rate=interest_rate,
                base_money=base_money,
                starting_date=starting_date,
                ending_date=ending_date
            )
            db.session.add(deposit)
        db.session.commit()

def generate_transfers(app):
    with app.app_context():
        accounts: List[Account] = Account.query.all()
        accounts_amount = len(accounts)
        fake = Faker()
        for _ in range(accounts_amount * 5):
            account_from = accounts[random.randint(0, accounts_amount - 1)].account_number
            account_to = accounts[random.randint(0, accounts_amount - 1)].account_number
            amount = random.randint(6, 39999)
            transfer_date = fake.date_between(date(year=1980, month=1, day=1), datetime.now(timezone.utc).date())
            transfer = Transfer(
                account_from=account_from,
                account_to=account_to,
                amount=amount,
                transfer_date=transfer_date
            )
            db.session.add(transfer)
        db.session.commit()

def generate_transactions(app):
    with app.app_context():
        accounts: List[Account] = Account.query.all()
        accounts_amount = len(accounts)
        fake = Faker()
        for _ in range(accounts_amount * 5):
            account_number= accounts[random.randint(0, accounts_amount - 1)].account_number
            amount = random.randint(-1000, 1000)
            transaction_date = fake.date_between(date(year=1980, month=1, day=1), datetime.now(timezone.utc).date())
            transaction = Transaction(
                account_number=account_number,
                amount=amount,
                transaction_date=transaction_date,
            )
            db.session.add(transaction)
        db.session.commit()


def generate_all(app):
    generate_user_types(app)
    generate_account_types(app)
    generate_card_types(app)
    generate_customers(app)
    generate_accounts(app)
    generate_incomes(app)
    generate_cards(app)
    generate_student_loans(app)
    generate_mortgages(app)
    generate_deposits(app)
    generate_transfers(app)
    generate_transactions(app)

if __name__ == '__main__':
    app = create_app(DB_URI)

    print('COMMANDS: ')
    print('0 - generate whole database')
    print('1 - generate 133 users, customers, addresses and contacts (in case of empty db, run it first)')
    print('2 - generate account for every customer (if one already exists)')
    print('3 - generate account types (empty table advised)')
    print('4 - generate user types (empty table advised)')
    print('5 - generate incomes (if one already exists)')
    print('6 - generate card types (empty table advised)')
    print('7 - generate cards for each customer')
    print('8 - generate 30 student loans')
    print('9 - generate 30 mortgages')
    print('10 - generate deposits')
    print('11 - generate transfers')
    print('12 - generate transactions')
    print('999 - exit')

    while (cmd := int(input("enter cmd: "))) != 999:
        print('please stand by...', end='')
        if cmd == 0:
            generate_all(app)
        if cmd == 1:
            generate_customers(app)
        if cmd == 2:
            generate_accounts(app)
        if cmd == 3:
            generate_account_types(app)
        if cmd == 4:
            generate_user_types(app)
        if cmd == 5:
            generate_incomes(app)
        if cmd == 6:
            generate_card_types(app)
        if cmd == 7:
            generate_cards(app)
        if cmd == 8:
            generate_student_loans(app)
        if cmd == 9:
            generate_mortgages(app)
        if cmd == 10:
            generate_deposits(app)
        if cmd == 11:
            generate_transfers(app)
        if cmd == 12:
            generate_transactions(app)

        print('success.')


    


