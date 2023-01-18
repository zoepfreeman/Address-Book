from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, AddressForm
from app.models import User, Addres

@app.route('/')
def index():
    addresses = Addres.query.all()
    return render_template('index.html', addresses=addresses)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Create an instance of the SignUpForm
    form = SignUpForm()
    # Check if a POST request AND data is valid
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        # Get data from the form
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        #print(email, username, password)
        # Query our user table to see if there are any users with either username or email from form
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        # If the query comes back with any results
        if check_user:
            # Flash message saying that a user with email/username already exists
            flash('A user with that email and/or username already exists.', 'danger')
            return redirect(url_for('signup'))
        # If check_user is empty, create a new record in the user table
        new_user = User(firstname=firstname, lastname=lastname, email=email, username=username, password=password)
        # Flash a success message
        flash(f'Thank you {new_user.username} for signing up!', 'success')
        # Redirect back to Home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the username and password from the form
        username = form.username.data
        password = form.password.data
        print(username, password)
        # Query the user table to see if there is a user with that username
        user = User.query.filter_by(username=username).first()
        # Check if there is a user and that the password is correct
        if user is not None and user.check_password(password):
            # log the user in
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))

@app.route('/addaddress', methods=["GET", "POST"])
@login_required
def addaddress():
    form = AddressForm()
    if form.validate_on_submit():
        print('Form submitted and validated!')
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        address = form.address.data
        new_address = Addres(firstname=firstname, lastname=lastname, phone=phone, address=address, user_id=current_user.id)
        flash(f'{new_address.firstname} {new_address.lastname} has been added to the Address Book!', 'success')
        return redirect(url_for('index'))
    return render_template('addaddress.html',form=form)

@app.route('/address/<int:address_id>')
def get_address(address_id):
    address = Addres.query.get(address_id)
    if not address:
        flash(f"An address with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    if address.author != current_user:
        flash(f"You do not have permission to view this address", "danger")
        return redirect(url_for('index'))
    return render_template('address.html', address=address)

@app.route('/address/<address_id>/edit', methods=["GET", "POST"])
@login_required
def edit_address(address_id):
    addresss = Addres.query.get(address_id)
    if not addresss:
        flash(f"An address with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    # Make sure the post author is the current user
    if addresss.author != current_user:
        flash("You do not have permission to edit this address", "danger")
        return redirect(url_for('index'))
    form = AddressForm()
    if form.validate_on_submit():
        # Get the form data
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        address = form.address.data
        # update the post using the .update method
        addresss.update(firstname=firstname, lastname=lastname, phone=phone, address=address)
        flash(f"Information has been updated!", "success")
        return redirect(url_for('get_address', address_id=addresss.id))
    if request.method == 'GET':
        form.firstname.data = addresss.firstname
        form.lastname.data = addresss.lastname
        form.phone.data = addresss.phone
        form.address.data = addresss.address
    return render_template('edit_address.html', address=addresss, form=form)

@app.route('/address/<address_id>/delete')
@login_required
def delete_address(address_id):
    address = Addres.query.get(address_id)
    if not address:
        flash(f"An address with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    # Make sure the post author is the current user
    if address.author != current_user:
        flash("You do not have permission to delete this address", "danger")
        return redirect(url_for('index'))
    address.delete()
    flash(f"This address has been deleted", "info")
    return redirect(url_for('index'))