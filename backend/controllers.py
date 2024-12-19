from flask import Flask,render_template,request,redirect,url_for
from flask import current_app as app
from backend.models import *
from datetime import datetime
from werkzeug.utils import secure_filename
import random
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')



@app.route("/",methods=["GET","POST"])
def login():
    message=""
    
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=User_Info.query.filter_by(username=username,password=password).first()
        if user and (user.role=="admin" and user.status=="active"):
            return redirect(url_for('show_admin', admin_username=username))
            # return redirect('/show_admin')
            
        elif user and (user.role=="customer" and user.status=="active"):
            return redirect(url_for(
                        'customer_dashboard', 
                        cust_username=username
                          ))
            
           
        elif user and (user.role=="professional" and user.status=="active"):
            prof=Professional.query.filter_by(username=username).first()
            if prof:
                serv_name=prof.service_name
                servs=Service.query.filter_by(service_name=serv_name).first()
                serv_id=servs.service_id
                base_price=servs.base_price
                print(base_price)
                return redirect(url_for(
                        'professional_dashboard', 
                        serv_id=serv_id,
                        prof_username=username,
                         base_price=base_price ))
        elif user and user.status=="blocked":
            message="You can't Login , you are BLOCKED !"
        else:
            message="No USER found, Please fill the Correct Crendentials"
    return render_template("login.html",message=message)

@app.route("/customerR" , methods=["GET","POST"])
def customerR():
    message=""
    
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        name=request.form.get("full_name")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        phone=request.form.get("phone")
        cstr=Customer.query.filter_by(username=username).first()
        user=User_Info.query.filter_by(username=username).first()
        
        
        # print(new_user)
        if  not cstr and not user :
            new_user1=User_Info(username=username,password=password,role="customer")
            new_user2=Customer(username=username,name=name,address=address,pincode=pincode,phone=phone)
            db.session.add(new_user1)
            db.session.add(new_user2)
            db.session.commit()
            message="Registered Successfully"
        else:
            message="Registation already done either as Customer or Professional,Please go for Login"
    return render_template("customerR.html",message=message)


@app.route("/professionalR", methods=["GET", "POST"])
def professionalR():
    message = ""
    
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("full_name")
        address = request.form.get("address")
        service_name = request.form.get("service")
        pincode = request.form.get("pincode")
        phone = request.form.get("phone")
        file=request.files['file']
        url=""
        if file.filename:
            file_name=secure_filename(file.filename)
            url='./static/uploaded_files/'+username+'.png'
            file.save(url)
        experience = request.form.get("experience")
        
        service_p = Service_Proposal.query.filter_by(professional_username=username).first()
        usr = User_Info.query.filter_by(username=username).first()
        if not  usr:
            if not service_p :
                
                service = Service.query.filter_by(service_name=service_name).first()
                
                if service:
                    service_id = service.service_id
                    
                    
                    new_ser = Service_Proposal(
                        professional_username=username,
                        name=name,
                        password=password,
                        url=url,
                        service_name=service_name,
                        address=address,
                        pincode=pincode,
                        phone=phone,
                        experience=experience,
                        service_id=service_id,
                        status="pending"  # Initial status is pending until admin approval
                    )
                    db.session.add(new_ser)
                    db.session.commit()
                    
                    message = "Service proposal submitted successfully, awaiting admin approval."
                    
            
                    
                elif service_p.status == "pending":
                    message = "Your service proposal is still pending approval. Please wait for admin approval."
                
        else:
            message="Registration has already been completed either as Customer or Professional. Please log in."
    
    return render_template("professionalR.html",message=message)

            
            
        
       
        
    

@app.route("/new_service/<string:admin_username>" ,methods=["Get","POST"])
def new_service(admin_username):
    message=""
    if request.method == "POST":
        service_name = request.form.get("service_name")
        base_price = request.form.get("base_price")
        
        # Create a new service and add it to the database
        serv=Service.query.filter_by(service_name=service_name).first()
        if not serv:
            new_service1 = Service(service_name=service_name, base_price=base_price)
            db.session.add(new_service1)
            db.session.commit()
            message="Service Added Successfully"
        else:
            message="Service already exists"
        services = Service.query.all()
        render_template("admin_dashboard.html", services=services,admin_username=admin_username)
        # return render_template("new_service.html")
    return render_template("new_service.html",message=message,admin_username=admin_username)

    
    
    # Fetch all services from the database
    

    

@app.route("/prof_search/<int:serv_id>/<string:prof_username>")
def professional_search(serv_id,prof_username):
    return render_template("professional_search.html",serv_id=serv_id,prof_username=prof_username)

# @app.route("/admin_home/<string:admin_username>")
# def admin_home(admin_username):
#     print(admin_username)
#     return redirect(url_for('show_admin', admin_username=admin_username))


@app.route('/delete/<string:admin_username>/<int:service_id>')
def delete(service_id,admin_username):
    dlt=Service.query.filter_by(service_id=service_id).first()
    db.session.delete(dlt)
    db.session.commit()
    return redirect(url_for('show_admin', admin_username=admin_username))

@app.route('/update/<string:admin_username>/<int:service_id>',methods=["GET","POST"])
def edit(admin_username,service_id):
    upt=Service.query.filter_by(service_id=service_id).first()
    # admin_username = request.args.get('admin_username')
    if request.method=="POST":
        upt.service_name=request.form.get("service_name")
        upt.base_price=request.form.get("base_price")
        print(request.form.get("service_name"))
        db.session.commit()
        return redirect(url_for('show_admin', admin_username=admin_username))
    return render_template("update.html",service=upt,admin_username=admin_username)

@app.route('/show_admin/<string:admin_username>', endpoint='show_admin')
def admin_dashboard(admin_username):
    
    requests = Service_Request.query.all()
    services = Service.query.all()
    professionals = Professional.query.all()
    proposals = Service_Proposal.query.all()
    customers=Customer.query.all()
    # print(requests)
    return render_template(
        "admin_dashboard.html", 
        services=services, 
        professionals=professionals, 
        proposals=proposals, 
        requests=requests, 
        admin_username=admin_username,
        customers=customers
    )


@app.route('/admin_search/<string:admin_username>',methods=["GET","POST"])
def admin_search(admin_username):
    professional_results = []
    customer_results = []
        
    if request.method == "POST":
        search = request.form.get("search")
        
        user_query = User_Info.query.filter(
            (User_Info.username.ilike(f"%{search}%")) |
            (User_Info.role.ilike(f"%{search}%")) |
            (User_Info.status.ilike(f"%{search}%"))
        ).all()

        for user in user_query:
            if user.role == "professional":
                prof = Professional.query.filter_by(username=user.username).first()
                if prof:
                    professional_results.append(prof)
            elif user.role == "customer":
                cust = Customer.query.filter_by(username=user.username).first()
                if cust:
                    customer_results.append(cust)

    return render_template(
        "admin_search.html", 
        professional_results=professional_results, 
        customer_results=customer_results,admin_username=admin_username
    )


@app.route('/blockP/<string:admin_username>/<string:username>')
def blockP(admin_username,username):
    professional = Professional.query.filter_by(username=username).first()
    user=User_Info.query.filter_by(username=username).first()
    if professional:
        professional.block_status="blocked"
        db.session.commit()
    if user :
        user.status="blocked"
        db.session.commit()
    return redirect(request.referrer)

@app.route('/unblockP/<string:admin_username>/<string:username>')
def unblockP(admin_username,username):
    user=User_Info.query.filter_by(username=username).first()
    professional = Professional.query.filter_by(username=username).first()
    if professional :
        professional.block_status="active"
        db.session.commit()
    if user :
        user.status="active"
        db.session.commit()
    return redirect(request.referrer)

@app.route('/blockC/<string:admin_username>/<string:username>')
def blockC(admin_username,username):
    customer = Customer.query.filter_by(username=username).first()
    user=User_Info.query.filter_by(username=username).first()
    if customer:
        customer.block_status="blocked"
        db.session.commit()
    if user :
        user.status="blocked"
        db.session.commit()
    return redirect(request.referrer)

@app.route('/unblockC/<string:admin_username>/<string:username>')
def unblockC(admin_username,username):
    customer = Customer.query.filter_by(username=username).first()
    user=User_Info.query.filter_by(username=username).first()
    if customer:
        customer.block_status="active"
        db.session.commit()
    if user :
        user.status="active"
        db.session.commit()
    return redirect(request.referrer)

@app.route('/acceptP/<string:admin_username>/<string:professional_username>')
def acceptP(admin_username,professional_username):

    service = Service_Proposal.query.filter_by(professional_username=professional_username).first()
   
    if service and service.status == "pending":
        service.status = "approved"
        db.session.commit()

       
        usr = User_Info.query.filter_by(username=professional_username).first()
        prf = Professional.query.filter_by(username=professional_username).first()

       
        if not usr:
            new_user = User_Info(username=professional_username, password=service.password, role="professional")
            db.session.add(new_user)
        
        if not prf:
            proposal = service
            new_professional = Professional(
                username=professional_username,
                name=proposal.name,
                url=proposal.url,
                service_name=proposal.service_name,
                address=proposal.address,
                pincode=proposal.pincode,
                phone=proposal.phone,
                experience=proposal.experience)
            
            db.session.add(new_professional)
        
        db.session.commit()
        db.session.delete(service)
        db.session.commit()
    return redirect(request.referrer)

    

@app.route('/rejectP/<string:admin_username>/<string:professional_username>')
def rejectP(admin_username,professional_username):
    service = Service_Proposal.query.filter_by(professional_username=professional_username).first()

    db.session.delete(service)
    db.session.commit()
    
    return redirect(request.referrer)


@app.route('/customer_dashboard/<string:cust_username>')
def customer_dashboard(cust_username):
    message = request.args.get('message')
    services=Service.query.all()
    requests = Service_Request.query.filter_by(customer_username=cust_username).all()
    
    return render_template("customer_dashboard.html",services=services,cust_username=cust_username,requests=requests,message=message)


@app.route('/deleteP/<string:admin_username>/<string:username>')
def delP(admin_username,username):
    prof=Professional.query.filter_by(username=username).first()
    user=User_Info.query.filter_by(username=username).first()
    if prof:
        db.session.delete(prof)
    if user:
        db.session.delete(user)
    db.session.commit()
    return redirect(request.referrer)

@app.route('/deleteC/<string:admin_username>/<string:username>')
def delC(admin_username,username):
    cust=Customer.query.filter_by(username=username).first()
    user=User_Info.query.filter_by(username=username).first()
    if cust:
        db.session.delete(cust)
    if user:
        db.session.delete(user)
    db.session.commit()
    return redirect(request.referrer)




@app.route('/go/<string:cust_username>/<int:service_id>')
def go(cust_username,service_id):
    
    service=Service.query.filter_by(service_id=service_id).first()
    services = Service.query.all()
    requests = Service_Request.query.filter_by(customer_username=cust_username).all()

    return render_template("request.html",service=service,cust_username=cust_username,services=services,requests=requests, service_id=service_id)
   


@app.route('/request/<string:cust_username>/<int:service_id>', methods=["GET", "POST"])
def book(cust_username, service_id):
    message = ""
    if request.method == "POST":
        offered_price = int(request.form.get("base_price"))
       
        service_n = Service.query.filter_by(service_id=service_id).first()
        if service_n:
            serv_name = service_n.service_name
       
        requested_date = datetime.now().replace(microsecond=0)
       
        reqs = Service_Request.query.filter(
        Service_Request.customer_username==cust_username,
        Service_Request.service_id == service_id,
        Service_Request.offered_price == offered_price,
        Service_Request.status != "closed" 
        ).first()
        if not reqs:
            new_req = Service_Request(
                customer_username=cust_username,
                
                offered_price=offered_price,
                requested_date=requested_date,
                service_id=service_id,
                status="pending"
            )
            db.session.add(new_req)
            db.session.commit()
            message="Your request has been Noted! "  
        else: 
            message=f'This Service is already requested at {offered_price}'
        return redirect(url_for(
                        'customer_dashboard', 
                        cust_username=cust_username,
                          message=message))    
    return redirect(url_for(
                        'customer_dashboard', 
                        cust_username=cust_username,
                          message=message))
   
@app.route('/professional_dashboard/<int:serv_id>/<string:prof_username>', methods=['GET', 'POST'])
def professional_dashboard(prof_username, serv_id):
    servs=Service.query.filter_by(service_id=serv_id).first()
    query=servs.base_price
    serv_name=servs.service_name
    
    requests = Service_Request.query.filter_by(service_id=serv_id).all()
    return render_template("professional_dashboard.html", 
                           prof_username=prof_username, 
                           serv_id=serv_id, 
                           requests=requests,base_price=query,serv_name=serv_name)



    # You can now use these variables to process the data for the professional's dashboard
    # return render_template("professional_dashboard.html", prof_username=prof_username, serv_id=serv_id,requests=requests)

@app.route('/acceptR/<int:serv_id>/<string:prof_username>/<int:request_id>')
def acceptR(serv_id,prof_username,request_id):
    # acceptReq=Service_Request.query.filter_by(customer_username=customer_username,service_id=serv_id,offered_price=offered_price).all()
    acceptReq=Service_Request.query.filter_by(request_id=request_id).first()
    if acceptReq:
        acceptReq.professional_username=prof_username
        
        
        if acceptReq.status=="pending":
            acceptReq.status="approved"
        db.session.commit()
    return redirect(request.referrer)

@app.route('/rejectR/<int:serv_id>/<string:prof_username>/<int:request_id>')
def rejectR(serv_id,prof_username,request_id):
    # acceptReq=Service_Request.query.filter_by(customer_username=customer_username,service_id=serv_id,offered_price=offered_price).all()
    rejectReq=Service_Request.query.filter_by(request_id=request_id).first()
    if rejectReq:
        if rejectReq.status=="approved":
            rejectReq.status="pending"
            rejectReq.professional_username="No"
            db.session.commit()
    return redirect(request.referrer)


@app.route("/close/<string:username>/<int:request_id>")
def close(username,request_id):
    user=User_Info.query.filter_by(username=username).first()
    closeReq=Service_Request.query.filter_by(request_id=request_id).first()
    if user and user.role=="professional":
        if closeReq:
            if closeReq.status=="approved":
                closeReq.status="closed"
                db.session.commit()
        return redirect(request.referrer)
    elif user and user.role=="customer":
        return redirect(url_for(
                        'rating', 
                          cust_username=username,
                          request_id=request_id))
    
@app.route('/rate_professional/<string:cust_username>/<int:request_id>',methods=["GET","POST"])
def rating(cust_username,request_id):

    if request.method=="POST":
        rating=request.form.get("rating")
        req=Service_Request.query.filter_by(request_id=request_id).first()
        req.status='closed'
        req.rating=rating
        db.session.commit()
        reqs=Service_Request.query.filter_by(professional_username=req.professional_username).all()
        
        count=0
        value=0
        for re in reqs:
            rate=re.rating
            if rate:
                value+=int(rate)
            count+=1
        prf_rating=value/count
        prf=Professional.query.filter_by(username=req.professional_username).first()
        prf.rating=float(prf_rating)
        db.session.commit()
        return redirect(url_for(
                        'customer_dashboard', 
                        cust_username=cust_username,
                          ))
    return render_template('rating.html', cust_username=cust_username, request_id=request_id)


@app.route('/c_search/<string:cust_username>',methods=["GET","POST"])
def customer_search(cust_username):
    if request.method=="POST":
        search=request.form.get("search")
        results = Professional.query.filter(
            (Professional.pincode.ilike(f"%{search}%")) |
            (Professional.username.ilike(f"%{search}%")) |
            (Professional.address.ilike(f"%{search}%")) |
            (Professional.pincode.ilike(f"%{search}%")) |
            (Professional.service_name.ilike(f"%{search}%"))).all()
        
        # print(results)
        return render_template("customer_search.html", cust_username=cust_username,results=results)
    return render_template("customer_search.html", cust_username=cust_username)

@app.route("/book_S/<string:cust_username>/<string:username>",methods=["GET","POST"])   
def book_S(cust_username,username):
    message=""
    serv_name=Professional.query.filter_by(username=username).first()
    service_name=serv_name.service_name
    name=serv_name.name
    services=Service.query.filter_by(service_name=service_name).first()
    service_id=services.service_id
    base_price=services.base_price
    requested_date = datetime.now().replace(microsecond=0)
    print(requested_date)
    reqs = Service_Request.query.filter(
    Service_Request.professional_username == username,
    Service_Request.service_id == service_id,
    Service_Request.offered_price == base_price,
    Service_Request.status != "closed" 
    ).first()
    
    if not reqs:
        req=Service_Request(customer_username=cust_username,offered_price=base_price,professional_username=username,service_id=service_id,requested_date=requested_date)
        db.session.add(req)
        db.session.commit()
        message="Your request has been Noted! "
        return redirect(f"{request.referrer}?message={message}")
    message = f"{name} is already requested for {service_name} at {base_price} !"
    return redirect(f"{request.referrer}?message={message}")


@app.route('/prof_search/<int:serv_id>/<string:prof_username>',methods=["GET","POST"])
def prof_search(serv_id,prof_username):
    if request.method=="POST":
        search=request.form.get("search")
        print(search)
        results = Service_Request.query.filter((Service_Request.professional_username == prof_username) &  
                ((Service_Request.requested_date.ilike(f"%{search}%")) |
                (Service_Request.status.ilike(f"%{search}%")) |
                (Service_Request.offered_price.ilike(f"%{search}%")) )).all()
        
        print(results)
        return render_template("professional_search.html", prof_username=prof_username,results=results,serv_id=serv_id)
    return render_template("professional_search.html", prof_username=prof_username,serv_id=serv_id)


@app.route('/customer_profile/<string:customer_username>')
def customer_profile(customer_username):
    message = ""
    previous_page = request.referrer
    
    # Fetch customer details
    customer = Customer.query.filter_by(username=customer_username).first()
    if not customer:
        message = "Customer not found!"
        return render_template(
            "profile.html", user=None, user_type="customer", message=message, previous_page=previous_page
        )
    
    user = {
        "username": customer.username,
        "name": customer.name,
        "address": customer.address,
        "pincode": customer.pincode,
        "phone": customer.phone,
        "block_status": customer.block_status,
    }
    return render_template(
        "profile.html", user=user, user_type="customer", message=message, previous_page=previous_page
    )




@app.route('/professional_profile/<string:professional_username>')
def professional_profile(professional_username):
    message = ""
    approved=True
    previous_page = request.referrer
    
    # Fetch professional details
    professional = Professional.query.filter_by(username=professional_username).first()
    if not professional:
        message = "Not accepted yet!"
        return render_template(
            "profile.html", user=None, user_type="professional", message=message, previous_page=previous_page
        )
    
    user = {
        "username": professional.username,
        "name": professional.name,
        "address": professional.address,
        "pincode": professional.pincode,
        "phone": professional.phone,
        "service_name": professional.service_name,
        "experience": professional.experience,
        "block_status": professional.block_status,
        "url":professional.url,
        "rating":professional.rating
    }
    return render_template(
        "profile.html", user=user, user_type="professional", message=message, previous_page=previous_page,approved=approved
    )

@app.route('/proposed_professional_profile/<string:professional_username>')
def proposed_professional_profile(professional_username):
    message = ""
    approved=False
    previous_page = request.referrer
    
    # Fetch professional details
    professional = Service_Proposal.query.filter_by(professional_username=professional_username).first()
    if not professional:
        message = "Not accepted yet!"
        return render_template(
            "profile.html", user=None, user_type="professional", message=message, previous_page=previous_page
        )
    
    user = {
        "username": professional.professional_username,
        "name": professional.name,
        "address": professional.address,
        "pincode": professional.pincode,
        "phone": professional.phone,
        "service_name": professional.service_name,
        "experience": professional.experience,
        "block_status":professional.status,
        "url":professional.url
    }
    return render_template(
        "profile.html", user=user, user_type="professional", message=message, previous_page=previous_page,approved=approved
    )

@app.route('/deleteR/<string:admin_username>/<int:request_id>')
def delete_req(admin_username,request_id):
    req=Service_Request.query.filter_by(request_id=request_id).first()
    if req:
        db.session.delete(req)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/admin_summary/<string:admin_username>')
def admin_summary(admin_username):
    data={}
    state={}
    prof={}
    user={}
    
    usrs=User_Info.query.all()
    if usrs:
        for usr in usrs:
            if usr.role not in user:
                user[usr.role]=0
            user[usr.role]+=1
               

    prfs=Professional.query.all()
    if prfs:
        for prf in prfs:
            service_name=prf.service_name
            if service_name not in prof:
                prof[service_name]=0
            prof[service_name]+=1

    reqs=Service_Request.query.all()
    if reqs:
        for req in reqs:
            status=req.status
            if status not in state:
                state[status]=0
            state[status]+=1

            serv=Service.query.filter_by(service_id=req.service_id).first()
            if serv:
                service_name=serv.service_name
                if service_name not in data:
                    data[service_name]=0
                data[service_name]+=1
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'brown', 'lime']
    xlabels=["Service-Name","Request-Status","Service-Name","Role"]
    ylabels=["No of Requests","Service-Name","Numbers of Professional","Number Of Users"]
    title=["Service Distribution","Request Status Distribution","Professional Distribution","User-Distribution"]
    info=[data,state,prof,user]
    for i in range(len(info)):
        
        if i == 1 :  
            labels= list(info[i].keys())
            sizes = list(info[i].values())
            plt.figure(figsize=(10, 6))
            plt.pie(sizes, labels=labels, colors=random.sample(colors, len(labels)), autopct='%1.1f%%', startangle=140)
            plt.title(title[i])
            plt.tight_layout()
            plt.savefig(f"./static/images/admin_summary_{i+1}.jpeg")
            plt.clf()
        else :

            x=list(info[i].keys())
            y=list(info[i].values())
            plt.figure(figsize=(10, 6))
            bar_colors = [random.choice(colors) for _ in range(len(x))]
            plt.bar(x,y,color=bar_colors)
            plt.title(title[i])
          
            plt.xlabel(xlabels[i])
            plt.ylabel(ylabels[i])
            y_max = max(y) if y else 1 
            plt.yticks(range(0, y_max + 1))
            plt.savefig(f"./static/images/admin_summary_{i+1}.jpeg")
            plt.clf()

       

    return render_template("admin_summary.html",admin_username=admin_username)

@app.route("/customer_summary/<string:cust_username>")
def customer_summary(cust_username):
    state={}
    request={}
    reqs=Service_Request.query.filter_by(customer_username=cust_username).all()
    if reqs:
        for req in reqs:
            status=req.status
            if status not in state:
                state[status]=0
            state[status]+=1

            serv=Service.query.filter_by(service_id=req.service_id).first()
            service_name=serv.service_name
            if service_name not in request:
                request[service_name]=0
            request[service_name]+=1


        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'brown', 'lime']
        xlabels=["Service-Name","Request-Status"]
        ylabels=["No of Requests","Service-Name"]
        title=["Request Distribution","Request Status Distribution"]
        info=[request,state]
        for i in range(2):
            if i == 1:  
                labels= list(info[i].keys())
                sizes = list(info[i].values())
                plt.figure(figsize=(10, 6))
                plt.pie(sizes, labels=labels, colors=random.sample(colors, len(labels)), autopct='%1.1f%%', startangle=140)
                plt.title(title[i])
                plt.tight_layout()
                plt.savefig(f"./static/images/customer_summary_{i+1}.jpeg")
                plt.clf()
            else:
                x=list(info[i].keys())
                y=list(info[i].values())
                plt.figure(figsize=(10, 6))
                bar_colors = [random.choice(colors) for _ in range(len(x))]
                plt.bar(x,y,color=bar_colors)
                plt.title(title[i])
            
                plt.xlabel(xlabels[i])
                plt.ylabel(ylabels[i])
                y_max = max(y) if y else 1 
                plt.yticks(range(0, y_max + 1))
                plt.savefig(f"./static/images/customer_summary_{i+1}.jpeg")
                plt.clf()

    return render_template("customer_summary.html",cust_username=cust_username)

@app.route('/prof_summary/<int:serv_id>/<string:prof_username>')
def prof_summary(serv_id,prof_username):
    state={}
    
    reqs=Service_Request.query.filter_by(professional_username=prof_username).all()
    if reqs:
        for req in reqs:
            status=req.status
            if status not in state:
                state[status]=0
            state[status]+=1

        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'brown', 'lime']
        x=list(state.keys())
        y=list(state.values())
        plt.figure(figsize=(10, 6))
        bar_colors = [random.choice(colors) for _ in range(len(x))]
        plt.bar(x,y,color=bar_colors)
        plt.title("Request-Distribution") 
        plt.xlabel("Status")
        plt.ylabel("Number Of Requests")
        y_max = max(y) if y else 1 
        plt.yticks(range(0, y_max + 1))
        plt.savefig(f"./static/images/professional_summary_1.jpeg")
        plt.clf()

        labels= list(state.keys())
        sizes = list(state.values())
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, colors=random.sample(colors, len(labels)), autopct='%1.1f%%', startangle=140)
        plt.title("Request-Status")
        plt.tight_layout()
        plt.savefig(f"./static/images/professional_summary_2.jpeg")
        plt.clf()
    return render_template("professional_summary.html",serv_id=serv_id,prof_username=prof_username)


        
        



