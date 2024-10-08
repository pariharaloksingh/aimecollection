from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key='secret key'

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), unique=True)
    password=db.Column(db.String(100))
    
    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        
    def check_password(self, password):
       return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    

with app.app_context():
    db.create_all()

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        
        user=User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['name']=user.name
            session['email']=user.email
            session['password']=user.password
            return redirect('/home')
        else:
            return render_template('login.html',error='Invalid user')
        
    return render_template('login.html')


@app.route('/register',methods=['GET','POST'])
def register():
   if request.method=='POST':
       name = request.form['name']
       email = request.form['email']
       password = request.form['password']
       
       new_user=User(name=name,email=email,password=password)
       db.session.add(new_user)
       db.session.commit()
       return redirect('/')
       
   return render_template('register.html')



@app.route('/home')
def home():
    if session['name']:
        return render_template('home.html')
    return redirect('/')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    return "the email is {} and password is {}".format(email,password)


if __name__=='__main__':
    app.run(debug=True)
    