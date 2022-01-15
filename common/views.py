from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from common.app import db

class CustomerDetails(db.Model):
    __tablename__="CustomerDetails"

    customer_id = Column("CustomerID", Integer, primary_key=True)
    first_name = Column("FirstName", String(35), nullable=False)
    last_name = Column("LastName", String(35), nullable=False)
    country_code = Column("CountryCOde", String(3), nullable=False)
    city = Column("City", String(50), nullable=False)
    zip_code = Column("ZipCode", String(9), nullable=False)
    street_name = Column("StreetName", String(50), nullable=False)
    street_number = Column("StreetNumber", String(10), nullable=False)
    apartment_number = Column("ApartmentNumber", String(10))
    email = Column("Email", String(255))
    phone_number = Column("PhoneNumber", String(15))


    def __repr__(self):
        return f"CustomerDetails: <customer_id: {self.customer_id}, first_name: {self.first_name}, last_name: {self.last_name}, country_code: {self.country_code}, city: {self.city}, zip_code: {self.zip_code}, street_name: {self.street_name}, street_number: {self.street_number}, apartment_number: {self.apartment_number}, email: {self.email}, phone_number: {self.phone_number}>"
