from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e8ab7c3d28ef5d1a4f6d2e3b0c5a7b8f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100))  #
    email = db.Column(db.String(120)) #

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class CartProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship('Product', secondary=CartProduct.__table__) 
    # Use the actual table name


# Cart Routes
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user_cart = Cart.query.filter_by(user_id=user_id).first()
        if user_cart is None:
            user_cart = Cart(user_id=user_id)
            db.session.add(user_cart)

        cart_product = CartProduct.query.filter_by(cart_id=user_cart.id, product_id=product_id).first()
        if cart_product:
            cart_product.quantity += 1
        else:
            cart_product = CartProduct(cart_id=user_cart.id, product_id=product_id)
            db.session.add(cart_product)

        db.session.commit()
        flash('Product added to cart', 'success')
    else:
        flash('Please log in to add products to your cart', 'warning')

    return redirect(url_for('products'))

@app.route('/view_cart')
def view_cart():
    if 'user_id' in session:
        user_id = session['user_id']
        user_cart = Cart.query.filter_by(user_id=user_id).first()
        return render_template('cart.html', user_cart=user_cart)
    else:
        flash('Please log in to view your cart', 'warning')
        return redirect(url_for('login'))

@app.route('/checkout')
def checkout():
    if 'user_id' in session:
        user_id = session['user_id']
        user_cart = Cart.query.filter_by(user_id=user_id).first()
        return render_template('checkout.html', user_cart=user_cart)
    else:
        flash('Please log in to proceed to checkout', 'warning')
        return redirect(url_for('login'))



@app.route('/')
def home():
    registration_url = '/register'
    login_url = '/login'  # Update this with the actual login route URL
    return render_template('home.html', registration_url=registration_url, login_url=login_url)

@app.route('/about')
def about():
    return render_template('about.html')  

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Username already taken'
            return render_template('register.html', error=error)
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password)

            # Save the new user to the database
            db.session.add(new_user)
            db.session.commit()

            return redirect('/login')
    return render_template('register.html')
        


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'  # Set the error message
            return render_template('login.html', error=error)
    
    return render_template('login.html')


#routes for product listing
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)


#routes for product details
@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    return render_template('product_details.html', product=product)



# Route for user profile
@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

# Route for updating user profile
@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if request.method == 'POST':
            user.name = request.form['name']
            user.email = request.form['email']
            db.session.commit()
            return redirect(url_for('profile'))
        return render_template('update_profile.html', user=user)
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return render_template('logout.html')


if __name__ == '__main__':
    with app.app_context():
        # Create the database tables
        db.create_all()

        # Check if the sample user already exists
        existing_user = User.query.filter_by(username='sample_user').first()

        if not existing_user:
            # Create the sample user
            user = User(username='sample_user', password_hash='hashed_password')
            db.session.add(user)
            
            # Create sample products associated with the user
            product1 = Product(name='Toy Car', description='A fun toy car for kids.', price=9.99, image_url='toy_car.jpg', user_id=user.id)
            product2 = Product(name='Stuffed Animal', description='Soft and cuddly stuffed animal.', price=14.99, image_url='stuffed_animal.jpg', user_id=user.id)
            db.session.add_all([product1, product2])
            
            # Commit the changes to the database
            db.session.commit()

    # Start the Flask app
    app.run(debug=True)
