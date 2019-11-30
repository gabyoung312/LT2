from flask import Flask, redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import logging
import ordermanagement as om

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)


@app.route('/orderhistory')
def orderhistory():
    user_ = session["user"]
    username = user_["username"]
    confirmed_order = om.check_user(username)

    if confirmed_order:
        past_orders = db.get_orders(username)

        return render_template('orderhistory.html', past_orders=past_orders)

    else:
        return render_template("noorders.html")


@app.route('/checkout', methods=['POST', ])
def checkout():
    location = request.form.get('location')
    print('location', location)
    # clear cart in session memory upon checkout
    om.create_order_from_cart(location)
    session.pop("cart", None)
    return redirect('/ordercomplete')


@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')


@app.route('/addtocart', methods=['POST', ])
def addtocart():
    code = request.form.get('code')
    quantity = int(request.form.get('quantity'))
    product = db.get_product(int(code))
    item = dict()
    # A click to add a product translates to a
    # quantity of 1 for now

    stall = db.get_stall(product["stall_id"])

    item["qty"] = quantity
    item["code"] = code
    item["stall"] = stall["name"]
    item["name"] = product["name"]
    item["subtotal"] = product["price"] * item["qty"]

    if (session.get("cart") is None):
        session["cart"] = {}

    cart = session["cart"]
    cart[code] = item
    session["cart"] = cart
    return redirect('/cart')


@app.route('/updatecart', methods=['POST'])
def updatecart():
    request_type = request.form.get('submit')
    code = request.form.get('code')
    product = db.get_product(int(code))
    cart = session["cart"]

    # Update quantity of item in cart
    if request_type == "Update":
        quantity = int(request.form.get("quantity"))
        cart[code]["qty"] = quantity
        cart[code]["subtotal"] = quantity * product["price"]

    # Remove item from cart
    elif request_type == 'Remove':
        del cart[code]

    session["cart"] = cart

    return redirect('/cart')


@app.route('/cart')
def cart():
    location_list = db.get_location()
    return render_template('cart.html', location_list=location_list)


@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("cart", None)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if (is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return redirect('/loginerror')


@app.route('/')
def index():
    return render_template('index.html', page="Index")


@app.route('/loginerror')
def loginerror():
    return render_template('loginerror.html', page="Loginerror")


@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    return render_template('productdetails.html', code=code,
                           product=product)


@app.route('/stalls')
def stalls():
    stall_list = db.get_stalls()
    return render_template('stalls.html', page="Stalls", stall_list=stall_list)


@app.route('/stalldetails')
def stalldetails():
    code = int(request.args.get('code', '0'))
    stall = db.get_stall(code)
    products = db.get_products(code)
    return render_template('stalldetails.html', code=code, products=products, stall=stall)


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")


@app.route('/change_page')
def change_page():
    return render_template('change_password.html')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    pw = request.form.get("old")
    new1 = request.form.get("new1")
    new2 = request.form.get("new2")
    user = session["user"]
    username = user["username"]
    user_pass = db.password(username)

    print('pw', pw)
    print('user_passw', user_pass)

    if pw == user_pass:
        if new1 == new2:
            db.change_pw(username, new1)
            error = "Password Change Successs"
            return render_template('/change_password.html', error=error)
        else:
            error = "Passwords do not match"
            return render_template('/change_password.html', error=error)
    else:
        error = "Invalid Password"
        return render_template('/change_password.html', error=error, pw=pw)
