from flask import Flask,request,redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    date_joined = db.Column(db.DateTime)

    orders = db.relationship("Order",back_populates = "user")

order_product = db.Table("order_product",
    db.Column("order_id",db.ForeignKey("order.id"),primary_key = True),                         
    db.Column("product_id",db.ForeignKey("product.id"),primary_key = True)
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    total = db.Column(db.Integer)
    user_id = db.Column(db.ForeignKey("user.id"))


    user = db.relationship("User",back_populates = "orders")
    products = db.relationship("Product",secondary= order_product,back_populates ="orders")

class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))

    orders = db.relationship("Order",secondary = order_product, back_populates = "products")
@app.route("/")
def index():
    return render_template("index.html",page_name = "home page", page_num = "2")


@app.route("/home")
def home():
    return render_template("home.html",number = 10, data = [{"key":"value1"},{"key":"value2"},{"key":"value3"}])


@app.post("/json")
def json():
    return {"key":"JSON VALUE","my_list":[1,2,3,4,5,6]}

@app.route("/dynamic",defaults= {"user_input": "default"})
@app.route("/dynamic/<user_input>")
def dynamic(user_input):
     return f"<h1>the user entered: {user_input}</h1>"

@app.route("/query")
def query():
    first = request.args.get("first")
    second = request.args.get("second")
    return f"<h1>The query strings contains {first} and {second}</h1>"

@app.route("/form",methods=["GET","POST"])
def form():
    if request.method == "POST":
        user_input = request.form["user_input"]
        print(user_input)
        return redirect(url_for("home"))
    return '<form method=POST><input type = "text" name = "user_input"/><input type = "submit"/></form>'

@app.route("/acceptjson")
def acceptjson():
    json_data = request.get_json()
    api_input = json_data["api_input"]
    my_list = json_data["my_list"]
    return {"api_input": api_input, "my_list": my_list}  

@app.route("/error")
def error():
    a = 4/0
    return "Error"

def insert_data():
    from datetime import datetime
    python_user = User(name = "Python User",date_joined = datetime.now())
    flask_user = User(name = "Flask User",date_joined = datetime.now())
    javasript_user = User(name = "JavaScript User",date_joined = datetime.now())
    db.session.add_all([python_user,flask_user,javasript_user]) 
    
    first_order = Order(total = 99, user=python_user)
    second_user = Order(total = 100, user = python_user)
    third_user = Order(total = 101, user = flask_user)
    db.session.add_all([first_order,second_user,third_user])
    
    db.session.commit()

def update_first_user():
    user = User.query.first()
    user.name = "Flask User"
    db.session.commit()

def delete_first_user():
    user = User.query.first()
    db.session.delete(user)
    db.session.commit()

def query_tables():
    first_user = User.query.first()
    print("First User")
    for order in first_user.orders:
        print(f"Order ID: {order.id} Total: {order.total}")

    second_user = User.query.filter_by(id=2).first()
    print("Second User")
    for order in second_user.orders:
        print(f"Order ID: {order.id} Total: {order.total}")



def add_products_to_orders():
    fist_product = Product(name = "First")
    second_product = Product(name = "Second")
    third_product = Product(name = "Third")

    db.session.add_all([fist_product,second_product,third_product])

    first_order = Order.query.first()
    first_order.products.append(fist_product)
    first_order.products.append(second_product)

    db.session.commit()
