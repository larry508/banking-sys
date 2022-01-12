

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from common.service import db




class Customer(db.Model):
    __tablename__ = 'Customers'

    customer_id = Column("CustomerID", Integer, primary_key=True, autoincrement=True)
    first_name = Column("FirstName", String(35), nullable=False)
    middle_name = Column("MiddleName", String(35))
    last_name = Column("LastName", String(35), nullable=False)
    sex = Column("Sex", String(1), nullable=False)
    birth_date = Column("BirthDate", Date, nullable=False)
    address_id = Column("AddressID", Integer, ForeignKey("Addresses.AddressID"), nullable=True)
    contact_id = Column("ContactID", Integer, ForeignKey("Contacts.ContactID"), nullable=True)
    user_id = Column("UserID", Integer, ForeignKey("Users.UserID"), nullable=True)

    address = relationship("Address", back_populates="customer")
    contact = relationship("Contact", back_populates="customer")
    user = relationship("User", back_populates="customer")

    def __repr__(self):
        return f"Customer: <customer_id: {self.customer_id}. first_name: {self.first_name}, last_name: {self.last_name}, sex: {self.sex}, birth_date: {self.birth_date}, address_id: {self.address_id}, contact_id: {self.contact_id}, user_id: {self.user_id}>"


class Address(db.Model):
    __tablename__ = 'Addresses'

    address_id = Column("AddressID", Integer, primary_key=True, autoincrement=True)
    country_code = Column("CountryCode", String(3), nullable=False)
    city = Column("City", String(50), nullable=False)
    zip_code = Column("ZipCode", String(9), nullable=False)
    street_name = Column("StreetName", String(50), nullable=False)
    street_number = Column("StreetNumber", String(10), nullable=False)
    apartment_number = Column("ApartmentNumber", String(10))

    customer = relationship("Customer", back_populates="address", uselist=False)


class Contact(db.Model):
    __tablename__ = 'Contacts'

    contact_id = Column("ContactID", Integer, primary_key=True, autoincrement=True)
    email = Column("Email", String(255))
    phone_number = Column("PhoneNumber", String(15))

    customer = relationship("Customer", back_populates="contact", uselist=False)



class User(db.Model):
    __tablename__ = "Users"

    user_id = Column("UserID", Integer, primary_key=True, autoincrement=True)
    user_type = Column("UserType", String(8))
    username = Column("Username", String(25), unique=True)
    email = Column("Email", String(255))
    password_hash = Column("PasswordHash", String(256))
    registration_date = Column("RegistrationDate", DateTime)
    last_login = Column("LastLogin", DateTime)

    customer = relationship("Customer", back_populates="user", uselist=False)
