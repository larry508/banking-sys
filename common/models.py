from datetime import datetime, timezone
from enum import auto

from turtle import back
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from common.app import db

class Customer(db.Model):
    __tablename__ = 'Customers'

    customer_id = Column("CustomerID", String(13), primary_key=True)
    first_name = Column("FirstName", String(35), nullable=False)
    middle_name = Column("MiddleName", String(35))
    last_name = Column("LastName", String(35), nullable=False)
    gender = Column("Gender", String(1), nullable=False)
    birth_date = Column("BirthDate", Date, nullable=False)
    address_id = Column("AddressID", Integer, ForeignKey("Addresses.AddressID"))
    contact_id = Column("ContactID", Integer, ForeignKey("Contacts.ContactID"))
    user_id = Column("UserID", Integer, ForeignKey("Users.UserID"))

    address = relationship("Address", back_populates="customer", uselist=False)
    account = relationship("Account", back_populates="customer", uselist=False)
    contact = relationship("Contact", back_populates="customer", uselist=False)
    user = relationship("User", back_populates="customer", uselist=False)
    income = relationship("Income", back_populates="customer", uselist=False)
    loan = relationship("Loan", back_populates="customer", uselist=False)
    deposit = relationship("Deposit", back_populates="customer", uselist=False)

    def __repr__(self):
        return f"Customer: <customer_id: {self.customer_id}, first_name: {self.first_name}, last_name: {self.last_name}, gender: {self.gender}, birth_date: {self.birth_date}, user_id: {self.user_id}>"


class Address(db.Model):
    __tablename__ = 'Addresses'
    address_id = Column("AddressID", Integer, primary_key=True, autoincrement=True)
    country_code = Column("CountryCode", String(3), nullable=False)
    city = Column("City", String(50), nullable=False)
    zip_code = Column("ZipCode", String(9), nullable=False)
    street_name = Column("StreetName", String(50), nullable=False)
    street_number = Column("StreetNumber", String(10), nullable=False)
    apartment_number = Column("ApartmentNumber", String(10))

    customer = relationship("Customer", back_populates="address")


class Contact(db.Model):
    __tablename__ = 'Contacts'
    contact_id = Column("ContactID", Integer, primary_key=True, autoincrement=True)
    email = Column("Email", String(255))
    phone_number = Column("PhoneNumber", String(15))

    customer = relationship("Customer", back_populates="contact")



class UserType(db.Model):
    __tablename__="UserTypes"

    code = Column("Code", String(3), primary_key=True, nullable=False)
    description = Column("Description", String(25), nullable=False)
    user = relationship("User", back_populates="user", uselist=False)

class User(db.Model):
    __tablename__ = "Users"

    user_id = Column("UserID", Integer, primary_key=True, autoincrement=True)
    user_type = Column("UserType", String(8), ForeignKey("UserTypes.Code"), nullable=False)
    username = Column("Username", String(25), unique=True)
    email = Column("Email", String(255))
    password_hash = Column("PasswordHash", String(256))
    registration_date = Column("RegistrationDate", DateTime)
    last_login = Column("LastLogin", DateTime)

    customer = relationship("Customer", back_populates="user", uselist=False)
    user = relationship("UserType", back_populates="user", uselist=False)


class AccountType(db.Model):
    __tablename__ = "AccountTypes"

    code = Column("Code", String(3), primary_key=True, nullable=False)
    description = Column("Description", String(50), nullable=False)
    interest_rate = Column("InterestRate", Numeric(precision=10))
    monthly_fee = Column("MonthlyFee", Numeric(precision=10), default=0, nullable=False)

    account = relationship("Account", back_populates="acc_type", uselist=False)



class Account(db.Model):
    __tablename__ = "Accounts"

    account_number = Column("AccountNumber", String(26), nullable=False, primary_key=True)
    customer_id = Column("CustomerID", Integer, ForeignKey("Customers.CustomerID"), nullable=False)
    account_type = Column("AccountType", String(3), ForeignKey("AccountTypes.Code"), nullable=False)
    balance = Column("Balance", Numeric(precision=2), default=0)
    opened_date = Column("OpenedDate", Date)

    acc_type = relationship("AccountType", back_populates="account")
    customer = relationship("Customer", back_populates="account")
    card = relationship('Card', back_populates='account')
    # transfer = relationship("Transfer", back_populates="account", uselist=False)
    transaction = relationship("Transaction", back_populates="customer", uselist=False)



class Income(db.Model):
    __tablename__ = "Incomes"
    income_id = Column("IncomeID", Integer, nullable=False, primary_key=True)
    customer_id = Column("CustomerID", String(13), ForeignKey("Customers.CustomerID"))
    company_name = Column("CompanyName", String(50), nullable=False)
    yearly_salary = Column("YearlySalary", Numeric(precision=2), nullable=False)
    paycheck_day = Column("PaycheckDay", Integer, nullable=False)

    customer = relationship("Customer", back_populates="income")


class CardType(db.Model):
    __tablename__ = "CardTypes"

    code = Column("Code", String(3), nullable=False, primary_key=True)
    description = Column("Description", String(30), nullable=False)
    monthly_fee = Column("MonthlyFee", Numeric(precision=2), nullable=False)

    card = relationship("Card", back_populates="cardtype", uselist=False)

class Card(db.Model):
    __tablename__ = "Cards"

    card_id = Column('CardID', Integer, nullable=False, primary_key=True, autoincrement=True)
    account_number = Column('AccountNumber', String(30), ForeignKey("Accounts.AccountNumber"), nullable=False)
    card_type = Column("CardType", String(3), ForeignKey("CardTypes.Code"), nullable=False)
    card_number = Column('CardNumber', String(19), nullable=False)
    activation_date = Column('ActivationDate', Date)
    expire_date = Column('ExpireDate', Date, nullable=False)
    cvv_hash = Column('CVVHash', String(256), nullable=False)

    account = relationship('Account', back_populates='card')
    cardtype = relationship('CardType', back_populates='card')


class Loan(db.Model):
    __tablename__ = "Loans"

    loan_id = Column('LoanID', Integer, nullable=False, primary_key=True, autoincrement=True)
    customer_id = Column('CustomerID', String(30), ForeignKey("Customers.CustomerID"), nullable=False)
    starting_date = Column('StartingDate', Date, nullable=False)
    ending_date = Column('EndingDate', Date, nullable=False)
    next_payment = Column('NextPayment', Date, nullable=False)
    payed_off = Column('PayedOff', Boolean, default=0)

    customer = relationship('Customer', back_populates='loan')
    student_loan = relationship('StudentLoan', back_populates='loan')
    mortgage = relationship('Mortgage', back_populates='loan')


class StudentLoan(db.Model):
    __tablename__ = "StudentLoans"

    student_loan_id = Column('StudentLoanId', Integer, nullable=False, primary_key=True)
    loan_id = Column("LoanID", Integer, ForeignKey("Loans.LoanID"), nullable=False)
    interest_rate = Column("InterestRate", Numeric(precision=2), nullable=False)
    total_owed = Column("TotalOwed", Numeric(precision=2), nullable=False)
    installment = Column("Installment", Numeric(precision=2), nullable=False)
    paid_amount = Column("PaidAmount", Numeric(precision=2), nullable=False)

    loan = relationship("Loan", back_populates='student_loan')

class Mortgage(db.Model):
    __tablename__ = "Mortgages"

    mortgage_id = Column('MortgageID', Integer, nullable=False, primary_key=True)
    loan_id = Column("LoanID", Integer, ForeignKey("Loans.LoanID"), nullable=False)
    interest_rate = Column("InterestRate", Numeric(precision=2), nullable=False)
    total_owed = Column("TotalOwed", Numeric(precision=2), nullable=False)
    installment = Column("Installment", Numeric(precision=2), nullable=False)
    paid_amount = Column("PaidAmount", Numeric(precision=2), nullable=False)

    loan = relationship("Loan", back_populates='mortgage')


class Deposit(db.Model):
    __tablename__ = "Deposits"
    
    deposit_id = Column('DepositID', Integer, nullable=False, primary_key=True, autoincrement=True)
    customer_id = Column('CustomerID', String(30), ForeignKey("Customers.CustomerID"), nullable=False)
    interest_rate = Column('InterestRate', Numeric(precision=2), nullable=False)
    base_money = Column('BaseMoney', Numeric(precision=2), nullable=False)
    starting_date = Column('StartingDate', Date, nullable=False)
    ending_date = Column('EndingDate', Date, nullable=False)

    customer = relationship("Customer", back_populates="deposit")


class Transfer(db.Model):
    __tablename__ = "Transfers"

    transfer_id = Column('TransferID', Integer, nullable=False, primary_key=True, autoincrement=True)
    account_from = Column('AccountFrom', String(30), ForeignKey("Accounts.AccountNumber"), nullable=False)
    account_to = Column('AccountTo', String(30), ForeignKey("Accounts.AccountNumber"), nullable=False)
    amount = Column('Amount', Numeric(precision=2), nullable=False)
    transfer_date = Column('TransferDate', Date, default=datetime.now(timezone.utc))

    # account = relationship("Account", back_populates='transfer')


class Transaction(db.Model):
    __tablename__ = "Transactions"

    transaction_id = Column('TransactionID', Integer, nullable=False, primary_key=True, autoincrement=True)
    account_number = Column('AccountNumber', String(30), ForeignKey("Accounts.AccountNumber"), nullable=False)
    amount = Column('Amount', Numeric(precision=2), nullable=False)
    transaction_date = Column('TransactionDate', Date, default=datetime.now(timezone.utc))

    customer = relationship("Account", back_populates='transaction')

