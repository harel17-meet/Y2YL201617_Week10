from flask import Flask, url_for, flash, redirect, request, render_template, g
from model import *
from flask import session as login_session
app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

engine = create_engine('sqlite:///fizzBuzz.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

@app.route('/')
@app.route('/inventory')
def inventory():
	productInventory=session.query(Product).all()
	return render_template('inventory.html', productInventory=productInventory )


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password= request.form['password']
		if email is None or password is None:
			flash('Missing Arguements')
			return redirect(url_for(login))
		if verify_password(email,password):
			customer = session.query(Customer).filter_by(email=email).one()
			flash('Login Successful, Welcome, %s' % customer.name)
			login_session['name'] = customer.name
			login_session['email'] = customer.email
			login_session['id'] = customer.id
			return redirect(url_for('inventory'))
		else:
			flash('Incorrect username/password combination')
			return redirect(url_for('login'))
def verify_password(email,password):
	customer = session.query(Customer).filter_by(email = email).first()
	if not customer or not customer.verify_password(password):
		return False
	g.customer = customer
	return True
	
@app.route('/newCustomer', methods = ['GET','POST'])
def newCustomer():
	if request.method == 'POST':	
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		address = request.form['address']
		if name == '' or email == '' or password == '':
			flash("Your form is missing arguments")
			return redirect(url_for('newCustomer'))
		if session.query(Customer).filter_by(email = email).first() is not None:
			flash("A user with this email address already exists")
			return redirect(url_for('newCustomer'))
		customer = Customer(name = name, email=email, address = address)
		customer.hash_password(password)
		session.add(customer)
		shoppingCart = ShoppingCart(customer=customer)
		session.add(shoppingCart)
		session.commit()
		flash("User Created Successfully!")
		return redirect(url_for('inventory'))
	else:
		return render_template('newCustomer.html')
@app.route("/product/<int:product_id>")
def product(product_id):
	product = session.query(Product).filter_by(id=product_id).one()
	return render_template('product.html', product=product)
@app.route("/product/<int:product_id>/addToCart", methods = ['POST'])
def addToCart(product_id):
	if 'id' not in login_session:
		flash("You must be logged in to perform this action")
		return redirect(url_for('login'))

@app.route("/shoppingCart")
def shoppingCart():
	
	return render_template('shoppingCart.html', name=name)
@app.route("/removeFromCart/<int:product_id>", methods = ['POST'])
def removeFromCart(product_id):
	return "To be implmented"

@app.route("/updateQuantity/<int:product_id>", methods = ['POST'])
def updateQuantity(product_id):
	return "To be implemented"

@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
	return "To be implmented"

@app.route("/confirmation/<confirmation>")
def confirmation(confirmation):
	
	return render_template('confirmation.html')
@app.route('/logout', methods = ['POST'])
def logout():
	return "To be implmented"

if __name__ == '__main__':
    app.run(debug=True)
