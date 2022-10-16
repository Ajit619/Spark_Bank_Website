import random
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///customer.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
@app.before_first_request
def create_tables():
    db.create_all()
class Cust(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    bank = db.Column(db.String(80))
    transfers = db.Column(db.Integer)
    Money = db.Column(db.Integer)

    def __repr__(self):
        return '<%r>' % self.name

def createlistofcustomers():
    if(Cust.query.all()==[]):
        print(Cust.query.all())
        list_of_names=['Ramesh','Abhinav','Virat','Shrikant','Kaushik','Vaibhav','Ajit','Tushar','Sakshi','Vinod','Viraj']
        for i in range(10):
            value=Cust(name=f'{list_of_names[i]}',email=f'{list_of_names[i]}@gmail.com',bank=f'bank{i+1}',transfers=random.randint(1,100),Money=random.randint(1000,10000))
            db.session.add(value)
            db.session.commit()
@app.route('/')
def bankingsystem():
    return render_template('homepage.html')
@app.route('/transfer',methods=['POST'])
def transfer():
    lst=list()
    for i in Cust.query.all():
        lst.append(i)
    return render_template('alltransfers.html',store=lst)
@app.route('/customers',methods=['POST','GET'])
def customers():
    createlistofcustomers()
    if(request.form.get('sender',False)):
        sender_id=request.form['sender']
        receiver_id=request.form['receiver']
        money=int(request.form['rupetext'])
        sendname=Cust.query.filter_by(id=sender_id).first()
        receivename=Cust.query.filter_by(id=receiver_id).first()
        tra=sendname.transfers
        if(sendname.Money<money):
            if(sendname.Money<0):
                sendname.Money=0
                db.session.commit()
        else:
            sendname.transfers+=1
            db.session.commit()
            sendname.Money-=money
            db.session.commit()
            receivename.Money+=money
            db.session.commit()
    lst=list()
    for i in Cust.query.all():
        lst.append(i)
    return render_template('viewallcust.html',store=lst)
@app.route('/details',methods=['GET','POST'])
def details():
    dct=dict()
    if(request.form.get('persdetail',False)):
        u_id=int(request.form.get('persdetail'))
        nameofperson=Cust.query.filter_by(id=u_id).first()
        dct.update({'name':nameofperson.name, 'Money':nameofperson.Money,'transfers':nameofperson.transfers,'Bank':nameofperson.bank,'server':nameofperson.email.split('@')[1]})
    return render_template('details.html',store=dct)
if __name__ == "__main__":
    # app.run(debug=True,ssl_context='adhoc')
    app.run(debug=True)

