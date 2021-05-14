from flask import Flask, render_template,url_for,flash,redirect,request
from forms import registerForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('food.id'))

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),unique=True,nullable=False)
    desc = db.Column(db.Text,nullable=True)
    price = db.Column(db.Integer)
    order_items = db.relationship('Order', backref='food_id', lazy=True)



@app.route("/",methods=["GET"])
@app.route("/home",methods=["GET"])
def hello():
    return render_template('home.html')

@app.route("/about",methods=["GET"])
def about():
    return render_template('about.html')

@app.route("/menu",methods=["GET" , "POST"])
def menu():
    if request.method == 'POST':
        order_id = request.form.get('add')
        print(order_id)
        product = Food.query.get(order_id)
        print(product)
        cart_item = Order(order_id=product.id)
        db.session.add(cart_item)
        db.session.commit()

    food_items = Food.query.all()
    return render_template('menu.html',Food=food_items)

@app.route("/order",methods=["GET" , "POST"])
def order():
    if request.method == 'POST':
        del_id = request.form.get('remove')
        print(del_id)
        obj = db.session.query(Order).filter(Order.order_id==del_id).first()
        print(obj)
        if(obj!=None):
            db.session.delete(obj)
            db.session.commit()

    order_items = Order.query.all()
    dic = {}

    for x in order_items:
        item = Food.query.filter_by(id = x.order_id).first()
        if(item.name not in dic):
            dic[item.name] = [item.id,1,item.price]
        else:
            dic[item.name] = [item.id,dic[item.name][1]+1,item.price]

    return render_template('order.html',food=dic)

@app.route("/cart",methods=["GET" , "POST"])
def cart():
    if request.method == 'POST':
        del_id = request.form.get('remove')
        print(del_id)
        obj = db.session.query(Order).filter(Order.order_id==del_id).first()
        print(obj)
        if(obj!=None):
            db.session.delete(obj)
            db.session.commit()

    order_items = Order.query.all()
    dic = {}


    for x in order_items:
        item = Food.query.filter_by(id = x.order_id).first()
        if(item.name not in dic):
            dic[item.name] = [item.id,1,item.price]
        else:
            dic[item.name] = [item.id,dic[item.name][1]+1,item.price]
    print(dic)
    return render_template('cart.html',food=dic)
if __name__ == '__main__':
    app.run(debug=True)