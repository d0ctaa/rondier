from flask import Flask, render_template, flash, redirect, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, DateField, EmailField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin
#from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


app = Flask(__name__)
app.secret_key='435dbd03cd03'

#Encryption management

bcrypt = Bcrypt(app)

## Login Manager Configuration

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "welcome"



##------------------------------------------------------------------
## Database URI configuration
##------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://sqladmin:pwd0000!@rondiersql.postgres.database.azure.com:5432/rondier-db-01'
db = SQLAlchemy(app)
migrate = Migrate(app,db)


## User Loader Function
@login_manager.user_loader
def user_loader(employee_id):

    with Session(db.engine) as session:
        return session.get(EmployeeDetail, int(employee_id))


##########################-----------------------------------------------
######### Model Configurations
#########-----------------------------------------------------------------


#Model for the transformer category
class Transformers(db.Model):
    __tablename__ = 'Transformers'
    __table_args__ = {'schema': 'r-schema-01'}
    id = db.Column(db.Integer, primary_key=True) #Serial Number because it will be unique to each device
    manufacturer = db.Column(db.String(32))
    model = db.Column(db.String(32))
    type = db.Column(db.String(32))
    rated_voltage_1 = db.Column(db.String(32))
    rated_voltage_2 = db.Column(db.String(32)) 
    rated_power =  db.Column(db.String(32)) #Rated Power (kVA or MVA)
    rated_frequency = db.Column(db.String(32))
    winding_Conf = db.Column (db.String(32)) #Winding Configuration
    impedance_voltage = db.Column(db.String(32)) #(%Z)
    insulation_class = db.Column(db.String(32))
    standard = db.Column(db.String(32))


#Model for the transformer category
class CircuitBraker(db.Model):
    __tablename__ = 'CircuitBraker'
    __table_args__ = {'schema': 'r-schema-01'}
    id = db.Column(db.Integer, primary_key=True) #Serial Number because it will be unique to each device
    manufacturer = db.Column(db.String(32))
    model = db.Column(db.String(32))
    type = db.Column(db.String(32))
    rated_voltage = db.Column(db.String(32)) #Maximum voltage of safe operation
    rated_current = db.Column(db.String(32)) #Maximum safe continious current carrying capacity
    pole_conf = db.Column(db.String(32)) #Number of pole configuration
    trip_unit_type = db.Column(db.String(32)) #Type of trip unit used for for overcurrent protection
    trip_current_rating = db.Column(db.String(32)) #current value at the breaker wil trip
    operating_vol = db.Column(db.String(32)) #Operating Voltage
    standard = db.Column(db.String(32))



#model for the different categories of devices found in a energy center
class Categories(db.Model):
    __tablename__ = 'Categories'
    __table_args__ = {'schema': 'r-schema-01'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    code = db.Column(db.String(32))
    description = db.Column(db.String(255))


class roles(RoleMixin, db.Model):
    __tablename__ = 'Roles'
    __table_args__ = {'schema': 'r-schema-01'}
    r_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(255))
#override the get ID function of the class
    
    def get_it(self):
        return str(self.r_id) 

## Associated role table
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('r-schema-01.Employees.employee_id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('r-schema-01.Roles.r_id')),
        schema = 'r-schema-01')




class EmployeeDetail(UserMixin, db.Model):
    __tablename__ = 'Employees'
    __table_args__ = {'schema': 'r-schema-01'}
    employee_id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100), nullable=False)
    LastName = db.Column(db.String(100), nullable=False)
    Birthdate = db.Column(db.Date)
    JobTitle = db.Column(db.String(100), nullable=False)
    UserName = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    pwhash = db.Column(db.String(128))
    fs_uniquifier = db.Column(db.String(255), unique=True)
    metricsRelation = db.relationship('DeviceMetrics', backref='entered_by')
    roles = db.relationship('roles', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

# override the get ID function of the class
    def get_id(self):
        return str(self.employee_id)



class Inventory(db.Model):
    __tablename__ = 'DeviceInventory'
    __table_args__ = {'schema': 'r-schema-01'}
    machine_id = db.Column(db.Integer, primary_key=True)
    Make = db.Column(db.String(100), nullable=False)
    Model = db.Column(db.String(100), nullable=False)
    Year = db.Column(db.Integer)
    SerialNumber = db.Column(db.String(100), nullable=False)
    Purpose = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    readings = db.relationship('DeviceMetrics', backref='machine')


class DeviceMetrics(db.Model):
    __tablename__ = 'Metrics'
    __table_args__ = {'schema': 'r-schema-01'}
    item_id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('r-schema-01.DeviceInventory.machine_id'))
    Value1 = db.Column(db.String(100), nullable=False)
    Value2 = db.Column(db.String(100), nullable=False)
    Value3 = db.Column(db.String(100), nullable=False)
    Value4 = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime)
    EmpID = db.Column(db.Integer, db.ForeignKey('r-schema-01.Employees.employee_id'))


## Flask Security configuration
user_datastore = SQLAlchemyUserDatastore(db, EmployeeDetail, roles)
security = Security(app, user_datastore)

##--------------------------------------------------------
## Forms Field configuration
## -------------------------------------------------------

class CircuitBrakerForm(FlaskForm):
    id = StringField('Serial Number') #Serial Number because it will be unique to each device
    manufacturer = StringField('Manufacturer')
    model = StringField('Model')
    type = StringField('Type')
    rated_voltage = StringField('Rated Voltage') #Maximum voltage of safe operation
    rated_current = StringField('Rated Current') #Maximum safe continious current carrying capacity
    pole_conf = IntegerField('Pole Configuration') #Number of pole configuration
    trip_unit_type = StringField('Trip Unit Type') #Type of trip unit used for for overcurrent protection
    trip_current_rating = IntegerField('Trip Current Rating') #current value at the breaker wil trip
    operating_vol = IntegerField('Operating Voltage') #Operating Voltage
    standard = StringField('Standard/Certification')
    submit = SubmitField('Submit')

class TransformersForm(FlaskForm):
    id = StringField('Serial Number') #Serial Number because it will be unique to each device
    manufacturer = StringField('Manufacturer')
    model = StringField('Model')
    type = StringField('Type')
    rated_voltage_1 = StringField('Rated Voltage I')
    rated_voltage_2 = StringField('Rated Voltage II')
    rated_power =  StringField('Rated Power') #Rated Power (kVA or MVA)
    rated_frequency = StringField('Rated Frequency')
    winding_Conf = StringField('Winding Configuration') #Winding Configuration
    impedance_voltage = StringField('Impedence Voltage') #(%Z)
    insulation_class = StringField('Insulation Class')
    standard = StringField('Standard/Certification')
    submit = SubmitField('Submit')

class RolesForm(FlaskForm):
    r_id = StringField('Role Code')
    r_name = StringField('Role Name')
    r_description = StringField('Role Description')
    submit = SubmitField('Submit')

class EmployeeForm(FlaskForm):
    fname = StringField('First Name')
    lname = StringField('Last Name')
    birthdate = DateField('Birth Date')
    title = StringField('Job Title')
    email = EmailField('E-Mail')
    password = PasswordField('Password')
    username = StringField('User Name')
    submit = SubmitField('Submit')

class MachineForm(FlaskForm):
    make = StringField('Make')
    model = StringField('Model')
    year = IntegerField('Year')
    serialNumber = StringField('Serial Number')
    purpose = StringField('Purpose')
    location = StringField('Location')
    img = StringField('Image Path')
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')


## -------------------------------------------------------
## Various Functions
## -------------------------------------------------------

#def user_auth(username, password):

   

## Route Configuration
    
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/table")
def hello_world():
    return render_template("table.html")
    #return 'Welcome'



@app.route("/admin", methods=['GET', 'POST'])
#@login_required
def admin():

    #Display form to add Transformer
    formT = TransformersForm()
    if formT.validate_on_submit():
        trsf = Transformers(
            id = formT.id.data,
            manufacturer = formT.manufacturer.data,
            model = formT.model.data,
            type = formT.type.data,
            rated_voltage_1 = formT.rated_voltage_1.data,
            rated_voltage_2 = formT.rated_voltage_2.data,
            rated_power = formT.rated_power.data,
            rated_frequency = formT.rated_frequency.data,
            winding_Conf = formT.winding_Conf.data,
            impedance_voltage = formT.impedance_voltage.data,
            insulation_class = formT.insulation_class.data,
            standard = formT.standard.data 
        )
        db.session.add(trsf)
        db.session.commit()

    #Display Circuit Braker Form 
    formC = CircuitBrakerForm()
    if formC.validate_on_submit():
        cbkr = CircuitBraker(

            id = formC.id.data, #Serial Number because it will be unique to each device
            manufacturer = formC.manufacturer.data,
            model = formC.model.data,
            type = formC.type.data,
            rated_voltage = formC.rated_voltage.data, #Maximum voltage of safe operation
            rated_current = formC.rated_current.data, #Maximum safe continious current carrying capacity
            pole_conf = formC.pole_conf.data, #Number of pole configuration
            trip_unit_type = formC.trip_unit_type.data, #Type of trip unit used for for overcurrent protection
            trip_current_rating = formC.trip_current_rating.data, #current value at the breaker wil trip
            operating_vol = formC.operating_vol.data, #Operating Voltage
            standard = formC.standard.data
        )
        db.session.add(cbkr)
        db.session.commit()



    #display employees list
    employee_list = EmployeeDetail.query.with_entities(EmployeeDetail.FirstName, EmployeeDetail.LastName, EmployeeDetail.email).all()

    #Display Categories
    categories_list = Categories.query.with_entities(Categories.name, Categories.description).all()

    # Display user roles creation form
    formR = RolesForm()
    if formR.validate_on_submit():
        role = roles(
            r_id = formR.r_id.data,
            name = formR.r_name.data,
            description = formR.description.data)

        db.session.add(role)
        db.session.commit()


    # Display employee registration form
    form = EmployeeForm()
    if form.validate_on_submit():
        #hashed_pw = bcrypt.hashpw(form.password.data.encode, bcrypt.gensalt())
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        employee=EmployeeDetail(
            FirstName = form.fname.data,
            LastName = form.lname.data,
            Birthdate = form.birthdate.data,
            JobTitle = form.title.data,
            email = form.email.data,
            pwhash = hashed_pw,
            UserName = form.username.data)
        
        db.session.add(employee)
        db.session.commit()
        flash('New Employee added successfully')
        return redirect(url_for('admin'))
    return render_template('admindash.html', form=form, employee_list=employee_list, formR=formR, categories_list=categories_list)


@app.route("/new_machine", methods=['GET', 'POST'])
#@login_required
def new_device():
    form = MachineForm()
    if form.validate_on_submit():
        machine=Inventory(
            Make = form.make.data,
            Model = form.model.data,
            Year = form.year.data,
            SerialNumber = form.serialNumber.data,
            Purpose = form.purpose.data,
            location = form.location.data,
            img = form.img.data)
        db.session.add(machine)
        db.session.commit()
        flash('New Machine added successfully')
        return redirect(url_for('index'))
    return render_template('add_device.html', tittle='Add Machine', form=form)

@app.route("/new_emp", methods=['GET', 'POST'])
#@login_required
def new_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        #hashed_pw = bcrypt.hashpw(form.password.data.encode, bcrypt.gensalt())
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(hashed_pw)
        employee=EmployeeDetail(
            FirstName = form.fname.data,
            LastName = form.lname.data,
            Birthdate = form.birthdate.data,
            JobTitle = form.title.data,
            email = form.email.data,
            pwhash = hashed_pw,
            UserName = form.username.data)
        
        db.session.add(employee)
        db.session.commit()
        flash('New Employee added successfully')
        return redirect(url_for('index'))
    return render_template('new_emp.html', tittle='Add Employee', form=form)

#Route for the home page that is also the login page.
@app.route('/welcome', methods=['GET','POST'])
def welcome():
    form = LoginForm()
    if form.validate_on_submit():
        user = EmployeeDetail.query.filter_by(UserName=form.username.data).first()
        if user and bcrypt.check_password_hash( user.pwhash, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin'))  # Redirect to a different page, e.g., 'home'
        else:
            print('User not found or password incorrect')
            flash('Invalid username or password', 'error')
    return render_template('landing.html', form=form)

if __name__=="__main__":
    app.run(debug = True)