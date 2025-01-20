
from os import path
from flask import render_template, redirect

from sqlalchemy.testing.pickleable import User

from flask_login import login_user, logout_user , login_required

from ext import app, db
from forms import RegisterForm, ProductForm, LoginForm
from models import  Product , User


profiles =[]


products = [
    {"name":"შაგრენის ტყავი", "price":"16.95","img":"http://elibrary.sou.edu.ge/files/books/book-311/cover-311.jpg","id":0},
    {"name":"მარტინ იდენი", "price":"16.95","img":"https://apiv1.biblusi.ge/storage/book/AffxK8uD3nE7q2WPDt1QyRkvXtz2BcS5sdHuXmdr.png","id":1},
    {"name": "ვეფხისტყაოსანი", "price": "16.95",
     "img": "https://apiv1.biblusi.ge/storage/book/TZNmwIag098BYyrIgiSYuEBF5xTFFyegNWdBWpgi.jpg","id":2},
    {"name": "ილია ჭავჭავაძე-მოთხრობები", "price": "16.95",
     "img": "https://apiv1.biblusi.ge/storage/book/xNySA3fdJ51VhtqA5wEhpdRJb38CZlXdRAcED9pS.jpg","id":3},
    {"name": "დორიან გრეის პორტრეტი", "price": "16.95",
     "img": "https://apiv1.biblusi.ge/storage/book/C2VeAp1Em6CzqqJTUA55hhHoeb264LTvz5P48EkP.png","id":4},
    {"name": "უჰამლეტი", "price": "16.95",
     "img": "https://apiv1.biblusi.ge/storage/book/MrxpYA8bRIbajthIy6qX6atox0Tz7BxtpVUbzh5P.jpg","id":5},
    {"name": "ვაჟა-ფშაველა პოემები", "price": "16.95",
     "img": "https://api.palitral.ge/storage/upload/image-png/2022-02-06/33_%E1%83%95%E1%83%90%E1%83%9F%E1%83%90-%E1%83%A4%E1%83%A8%E1%83%90%E1%83%95%E1%83%94%E1%83%9A%E1%83%90_-_%E1%83%9E%E1%83%9D%E1%83%94%E1%83%9B%E1%83%94%E1%83%91%E1%83%98_(1)_5d59d4412b6f37ad9eb2bac44f4c3ce8.png.webp","id":6},
    {"name": " დიდოსტატის მარჯვენა", "price": "16.95",
     "img": "https://apiv1.biblusi.ge/storage/book/OsE65lBJ9gI06ma9y4fMGEpP1Ws89iGBUbdSvci3.jpg","id":7},
    {"name": " ტომ სოიერის თავგადასავალი", "price": "16.95",
     "img": "https://apiv1.biblusi.ge/storage/book/B6Zivf3KOEb8F6a7iyWZRbtTZOLGThnH7qbki45k.jpg","id":8},
    {"name": "  სამი მუშკეტერი", "price": "16.95",
     "img": "https://apiv1.biblusi.ge/storage/book/sMUZhTnHfYIGMHOh4Lju7UORu3Z0tD08cdiEhf7A.jpg","id":9}

]

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("home.html" , products=products, role="administrator")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        new_user.create()
    return render_template("register.html", form=form)


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

            return redirect("/")

        return render_template("create_product.html", form=form)
@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])

def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price, img=product.img)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        product.update()

        return redirect("/")

    return render_template("create_product.html", form=form)

@app.route("/delete_product/<int:product_id>" )
def delete_product(product_id):
    product = Product.query.get(product_id)
    product.delete()
    return redirect("/")




@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
     user = User.query.filter_by(User.username == form.username.data).first()
    if user and user.check_password(form.password.data):
           login_user(user)