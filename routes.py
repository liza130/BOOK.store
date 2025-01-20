from os import path
from flask import render_template, redirect
from ext import app, db
from forms import RegisterForm, ProductForm, LoginForm
from models import Product, User
from flask_login import login_user, logout_user, login_required, current_user

profiles = []


@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products, role="Administrator")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        new_user.create()
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")





@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)

        image = form.img.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)

        new_product.img = image.filename

        db.session.add(new_product)
        db.session.commit()

    return render_template("create_product.html", form=form)


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price, img=product.img)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        db.session.commit()

        return redirect("/register")

    return render_template("create_product.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()

    return redirect("/")


@app.route("/product_detail/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    return render_template("product_details.html", product=product)
