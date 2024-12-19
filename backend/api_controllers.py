from flask_restful import Resource, Api
from flask import request
from .models import *
from datetime import datetime

api=Api()


class ServiceApi(Resource):
    def get(self):
        services=Service.query.all()
        serv_json=[]
        for serv in services:
            serv_json.append({'service_id':serv.service_id,'service_name':serv.service_name,'base_price':serv.base_price})
        return serv_json

    def post(self):
        if not request.is_json:
            return {"message": "Request Content must be 'application/json'"}, 400
        service_name = request.json.get('service_name')
        base_price = request.json.get('base_price')
        
        exist_service = Service.query.filter_by(service_name=service_name).first()
        if exist_service:
            return {"message": "This Service already exists!"}, 400
        new_service=Service(service_name=service_name,base_price=base_price)
        db.session.add(new_service)
        db.session.commit()

    def put(self,service_id):
        if not request.is_json:
            return {"message": "Request Content must be 'application/json'"}, 400
        service=Service.query.filter_by(service_id=service_id).first()
        if service:
            service_name = request.json.get('service_name')
            base_price = request.json.get('base_price')
            service.service_name = service_name
            service.base_price = base_price
            db.session.commit()
            return {'message':'Service Updated Successfully !'},200
        return {'message':'Service not found ! '},404

    def delete(self,service_id):
        
        service=Service.query.filter_by(service_id=service_id).first()
        if service:
            db.session.delete(service)
            db.session.commit()
            return {'message':'Service deleted Successfully !'},200
        return {'message':'Service not Found!'},400
    
class ServiceReqApi(Resource):
    def get(self):
        reqs=Service_Request.query.all()
        req_json=[]
        for req in reqs:
            req_json.append({'service_id':req.service_id,'professional_username':req.professional_username,'offered_price':req.offered_price,'customer_username':req.customer_username,'requested_date':str(req.requested_date)})
        return req_json
    
    def post(self):
        if not request.is_json:
            return {"message": "Request Content must be 'application/json'"}, 400
        service_id=request.json.get('service_id')
        professional_username=request.json.get('professional_username')
        offered_price=request.json.get('offered_price')
        customer_username=request.json.get('customer_username')
        requested_date=request.json.get('requested_date')
        requested_date=datetime.strptime(requested_date,"%Y-%m-%d %H:%M:%S")
        service = Service.query.filter_by(service_id=service_id).first()
        if not service:
            return {"message": f"Service with ID {service_id} not found."}, 404

       
        existing_request = Service_Request.query.filter(
            Service_Request.customer_username == customer_username,
            Service_Request.professional_username == professional_username,
            Service_Request.service_id == service_id,
            Service_Request.offered_price == offered_price,
            Service_Request.status != "closed"
        ).first()

        if existing_request:
            return {
                "message": f"Service already requested for Professional '{professional_username}' at offered price {offered_price}."
            }, 400

        # Create a new service request
        new_request = Service_Request(
            customer_username=customer_username,
            professional_username=professional_username,
            offered_price=offered_price,
            requested_date=requested_date,
            service_id=service_id,
            status="pending"
        )
        
       
        db.session.add(new_request)
        db.session.commit()
        return {
            "message": "Service request created successfully!",
            "request_id": new_request.request_id
        }, 201
    
    def put(self,request_id):
        if not request.is_json:
            return {"message": "Request Content must be 'application/json'"}, 400
        sreq = Service_Request.query.filter_by(request_id=request_id).first()
        if sreq:
            customer_username=request.json.get('customer_username')
            professional_username=request.json.get('professional_username')
            requested_date=request.json.get('requested_date')
            offered_price=request.json.get('offered_price')
            service_id=request.json.get('service_id')
            status=request.json.get('status')

            sreq.customer_username=customer_username
            sreq.professional_username=professional_username
            sreq.requested_date=requested_date
            sreq.offered_price=offered_price
            sreq.service_id=service_id
            sreq.status=status
            db.session.commit()
            return {'message':'updated successfully'},200
        return {'message':'Request not found!'},200
            
    def delete(self, request_id):
        sreq = Service_Request.query.filter_by(request_id=request_id).first()
        if sreq:
            db.session.delete(sreq)
            db.session.commit()
            return {'message': 'Service request deleted successfully!'}, 200
        return {'message': 'Service request not found '}, 404
    

class ServicePropApi(Resource):
    def get(self):
        sps=Service_Proposal.query.all()
        sp_json=[]
        for sp in sps:
            sp_json.append({'professional_username':sp.professional_username,'experience':sp.experience,'password':sp.password,'name':sp.name,'pincode':sp.pincode,'service_name':sp.service_name,'pincode':sp.pincode,'phone':sp.phone,'sevice_id':sp.service_id,'status':sp.status})
    
        return sp_json
    
    def post(self):
        if not request.is_json:
            return {"message": "Request Content-Type must be 'application/json'"}, 400
        existing_proposal = Service_Proposal.query.filter_by(
        professional_username=data['professional_username']
        ).first()

        if existing_proposal:
            return {
                "message": "A proposal for this username already exists."},400

           

        data = request.get_json()
        new_proposal = Service_Proposal(professional_username=data['professional_username'],phone=data['phone'],status=data['status','pending'], password=data['password'], name=data['name'], experience=data['experience'], address=data['address'], pincode=data['pincode'], service_id=data['service_id'], service_name=data['service_name'])
        db.session.add(new_proposal)
        db.session.commit()
        return {"message": "Service Proposal Created successfully"}, 201
    
    def put(self,proposal_id):
        if not request.is_json:
            return {"message": "Request Content-Type must be 'application/json'"}, 400
        sp=Service_Proposal.query.filter_by(proposal_id=proposal_id).first()
        if sp:
            data = request.get_json()
            sp.professional_username=data['professional_username']
            sp.phone=data['phone']
            sp.status=data['status',sp.status]
            sp.password=data['password']
            sp.name=data['name']
            sp.experience=data['experience']
            sp.address=data['address']
            sp.pincode=data['pincode']
            sp.service_id=data['service_id']
            sp.service_name=data['service_name']
            db.session.commit()
            return {'message':'proposal updated successfully'},200
        return {'message':'proposal not found!'},400
    
    def delete(self,proposal_id):
        sp=Service_Proposal.query.filter_by(proposal_id=proposal_id).first()
        if sp:
            db.session.delete(sp)
            db.session.commit()
            return {'message':'Deleted successfully!'}
        return {'message':'proposal not found !'}
    
class CustsApi(Resource):
    def get(self):
        cust_json=[]
        custs=Customer.query.all()
        if custs:
            for cust in custs:
                cust_json.append({'username':cust.username,'name':cust.name,'phone':cust.phone,'address':cust.address,'block_status':cust.block_status,'pincode':cust.pincode})
            return cust_json
        
    def post(self):
        if not request.is_json:
            return {"message": "Request Content-Type must be 'application/json'"}, 400
        data=request.get_json()
        existing_customer = Customer.query.filter_by(
        username=data['username']
        ).first()

        if existing_customer:
            return {
                "message": "A Customer for this username already exists."},400
        new_cust=Customer(username=data['username'],name=data['name'],phone=data['phone'],address=data['address'],pincode=data['pincode'],status=data['block_status','active'])
        db.session.add(new_cust)
        db.session.commit()
        return {'message':'added successfully!'},200
    
    def put(self,username):
        if not request.is_json:
            return {"message": "Request Content-Type must be 'application/json'"}, 400
        data=request.get_json()
        ec = Customer.query.filter_by(
        username=username).first()
       
        if ec:
            ec.username=data['username']
            ec.phone=data['phone']
            ec.status=data['block_status',ec.status]
            ec.name=data['name']
            ec.address=data['address']
            ec.pincode=data['pincode']
           
            db.session.commit()
            return {'message':'customer updated successfully'},200
        return {'message':'customer not found!'},400
    
    def delete(self,username):
        
        ec = Customer.query.filter_by(
        username=username
        ).first()
        if ec:
            db.session.delete(ec)
            db.session.commit()
            return {'message':'Deleted successfully!'}
        return {'message':'customer not found!'} 
    
class ProfApi(Resource):
    def get(self):
        prof_json=[]
        profs=Professional.query.all()
        if profs:
            for prof in profs:
                prof_json.append({'username':prof.username,'name':prof.name,'phone':prof.phone,'address':prof.address,'block_status':prof.block_status,'pincode':prof.pincode,'service_name':prof.service_name,'experience':prof.experience})
            return prof_json
        
    def post(self):
        if not request.is_json:
            return {"message": "Request Content-Type must be 'application/json'"}, 400
        data = request.get_json()

        existing_professional = Professional.query.filter_by(
            username=data['username']
        ).first()

        
        if existing_professional:
            return {
                "message": "A Professional with this username already exists."
            }, 400

        
        new_professional = Professional(
            username=data['username'],
            name=data['name'],
            phone=data['phone'],
            address=data['address'],
            pincode=data['pincode'],
            experience=data['experience'],
            service_name=data['service_name'],
            status=data['block_status','active']
        )

        
        db.session.add(new_professional)
        db.session.commit()

        return {'message': 'Professional added successfully!'}, 200
    
    def put(self,username):
        if not request.is_json:
            return {"message": "Request Content-Type must be 'application/json'"}, 400
        
        data = request.get_json()

        ep = Professional.query.filter_by(username=username).first()

        if not ep:
            return {
                "message": "Professional with this username does not exist."
            }, 400
 
        ep.name = data.get('name')
        ep.phone = data.get('phone')
        ep.address = data.get('address')
        ep.pincode = data.get('pincode')
        ep.experience = data.get('experience')
        ep.service_name = data.get('service_name')
        ep.status = data.get('block_status', ep.status)

       
        db.session.commit()

        return {'message': 'Professional updated successfully!'}, 200
    
    def delete(self,username):
        

        ep = Professional.query.filter_by(username=username).first()

        if not ep:
            return {
                "message": "Professional with this username does not exist."
            }, 400
        db.session.delete(ep)
        db.session.commit()
        return {"message":"Deleted successfully!"}
    
class UserApi(Resource):
    def get(self):
        users_json = [] 
        users_list = User_Info.query.all() 
        
        for user in users_list:
            users_json.append({
                'username': user.username,
                'password': user.password,
                'role': user.role,
                'status': user.status})
            
        return users_json  
    
    def post(self):
        if not request.is_json:
            return {"message": "Request Content-Type must be 'application/json'"}, 400
        
        data = request.get_json()
        username = data.get('username')
        
        
        existing_user = User_Info.query.filter_by(username=username).first()
        if existing_user:
            return {"message": "User with this username  already exists."}, 400
        
       
        new_user = User_Info(
            username=username,
            password=data.get('password'),
            role=data.get('role'),
            status=data.get('status', "active")  
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully."}, 200
    
    def put(self, username):
        if not request.is_json:
            return {"message": "Request Content-Type must be 'application/json'"}, 400
        
        
        user = User_Info.query.filter_by(username=username).first()
        if not user:
            return {"message": "User with this username not found."}, 404

        data = request.get_json()

        
        user.password = data.get('password', user.password)
        user.role = data.get('role', user.role)
        user.status = data.get('status', user.status)

        db.session.commit()
        return {"message": " updated successfully."}, 200
    
    def delete(self,username):
        user = User_Info.query.filter_by(username=username).first()
        if not user:
            return {"message": "User with this username not found."}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message':'deleted succesfully!'}

 
api.add_resource(UserApi,'/api/user','/api/user/<string:username>')
api.add_resource(ServiceApi,'/api/serv','/api/serv/<int:service_id>')
api.add_resource(ServiceReqApi,'/api/req','/api/req/<int:request_id>')
api.add_resource(ServicePropApi,'/api/sp','/api/sp/<int:proposal_id>')
api.add_resource(CustsApi,'/api/cust','/api/cust/<string:username>')
api.add_resource(ProfApi,'/api/prof','/api/prof/<string:username>')

            
            


        



        

                



        






       







