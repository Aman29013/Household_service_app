from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy()
class User_Info(db.Model):
    __tablename__ = 'user_info'
    
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum('professional', 'customer', 'admin'), nullable=False)
    status=db.Column(db.Enum('active','blocked'),default='active')

    professional = db.relationship('Professional', uselist=False, backref='user_info', cascade="all,delete")
    customer = db.relationship('Customer', uselist=False, backref='user_info', cascade="all,delete")
    


class Customer(db.Model):
    __tablename__ = 'customer'
    
    username = db.Column(db.String, db.ForeignKey('user_info.username', ondelete='CASCADE'), primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String, nullable=False)
    block_status = db.Column(db.String, default='active')
    service_req = db.relationship("Service_Request", cascade="all,delete", backref="customer", lazy=True)
    

class Professional(db.Model):
    __tablename__ = 'professional'
    
    username = db.Column(db.String, db.ForeignKey('user_info.username'), primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    service_name=db.Column(db.String, db.ForeignKey('service.service_name') , nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String, nullable=False)
    block_status = db.Column(db.String, default='active')
    url=db.Column(db.String)
    rating=db.Column(db.Float)
    service_request = db.relationship("Service_Request", cascade="all,delete", backref="professional", lazy=True)

class Service(db.Model):
    __tablename__ = 'service'
    
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name = db.Column(db.String,unique=True,nullable=False)
    base_price = db.Column(db.Integer, nullable=False)
    
    proposal=db.relationship('Service_Proposal',cascade="all,delete", backref="service", lazy=True)
    assosiated_prof=db.relationship('Professional',cascade="all,delete",backref="service",lazy=True)
    service_Req=db.relationship('Service_Request',cascade="all,delete", backref="service", lazy=True)

class Service_Request(db.Model):
    __tablename__ = 'service_request'
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_username = db.Column(db.String, db.ForeignKey('customer.username'), nullable=False)
    offered_price=db.Column(db.Integer,nullable=False)
    professional_username = db.Column(db.String, db.ForeignKey('professional.username', ondelete='CASCADE'),default="No")
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    requested_date = db.Column(db.DateTime, nullable=False)
    rating=db.Column(db.Integer)
    status = db.Column(db.Enum('approved','pending', 'closed'), default="pending",nullable=False)

class Service_Proposal(db.Model):
    __tablename__ = 'service_proposal'
    
    proposal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    professional_username = db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    url=db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    service_name=db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    status = db.Column(db.Enum('rejected' ,'approved','pending'),default='pending', nullable=False)
