from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'buildmanage'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitestock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Material(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    quantity=db.Column(db.Float,default=0)
    unit=db.Column(db.String(20),default='pcs')
    price=db.Column(db.Float,default=0)
    category=db.Column(db.String(50),default='General')
    min_stock=db.Column(db.Float,default=10)

class Truck(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    truck_number=db.Column(db.String(100),nullable=False)
    driver_name=db.Column(db.String(100),nullable=False)
    capacity=db.Column(db.Float,default=0)
    phone=db.Column(db.String(20))
    status=db.Column(db.String(20),default='Available')

class Project(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    location=db.Column(db.String(100))
    budget=db.Column(db.Float,default=0)
    status=db.Column(db.String(20),default='Ongoing')

with app.app_context():
    db.create_all()

@app.route('/')
def index(): return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    mats=Material.query.all()
    trucks=Truck.query.all()
    projs=Project.query.all()
    total=sum(m.quantity*m.price for m in mats)
    return render_template('dashboard.html', materials=mats, trucks=trucks, projects=projs, total_value=total)

@app.route('/add', methods=['POST'])
def add_material():
    m=Material(name=request.form['name'],quantity=float(request.form.get('quantity',0) or 0),unit=request.form.get('unit','pcs'),price=float(request.form.get('price',0) or 0),category=request.form.get('category','General'),min_stock=float(request.form.get('min_stock',10) or 10))
    db.session.add(m);db.session.commit();return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_material(id):
    db.session.delete(Material.query.get_or_404(id));db.session.commit();return redirect('/dashboard')

@app.route('/add_truck', methods=['POST'])
def add_truck():
    t=Truck(truck_number=request.form['truck_number'],driver_name=request.form['driver_name'],capacity=float(request.form.get('capacity',0) or 0),phone=request.form.get('phone'),status=request.form.get('status','Available'))
    db.session.add(t);db.session.commit();return redirect('/dashboard')

@app.route('/delete_truck/<int:id>')
def delete_truck(id):
    db.session.delete(Truck.query.get_or_404(id));db.session.commit();return redirect('/dashboard')

@app.route('/add_project', methods=['POST'])
def add_project():
    p=Project(name=request.form['project_name'],location=request.form.get('location'),budget=float(request.form.get('budget',0) or 0),status=request.form.get('status','Ongoing'))
    db.session.add(p);db.session.commit();return redirect('/dashboard')

@app.route('/delete_project/<int:id>')
def delete_project(id):
    db.session.delete(Project.query.get_or_404(id));db.session.commit();return redirect('/dashboard')

if __name__=='__main__':
    app.run(debug=True, port=5000)   