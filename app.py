from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os,dbConfig

# Init App
app = Flask(__name__)

# Simple Route
# @app.route('/', methods=['GET'])
# def get():
#     return jsonify({ 'msg': 'Hello from Flask' })

basedir = os.path.abspath(os.path.dirname(__file__))

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = dbConfig.dbURI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Init DB
db = SQLAlchemy(app)

# INIT Marshmallow
ma = Marshmallow(app)

# Product Class / Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')
    
# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create A Product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Fetch All Products
@app.route('/product', methods=['GET'])
def fetch_products():
    all_products = Product.query.all()

    return jsonify(products_schema.dump(all_products))

# Fetch Single Product
@app.route('/product/<id>', methods=['GET'])
def fetch_product(id):
    single_product = Product.query.get(id)

    return product_schema.jsonify(single_product)

# Update the Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    update_product = Product.query.get(id)

    if 'name' in request.json:
        name = request.json['name']
    else:
        name = update_product.name
    if 'description' in request.json:
        description = request.json['description']
    else:
        description = update_product.description
    if 'price' in request.json:
        price = request.json['price']
    else:
        price = update_product.price
    if 'qty' in request.json:
        qty = request.json['qty']
    else:
        qty = update_product.qty

    update_product.name = name
    update_product.description = description
    update_product.price = price
    update_product.qty = qty

    db.session.commit()

    return product_schema.jsonify(update_product)

# Delete The Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    delete_product = Product.query.get(id)

    db.session.delete(delete_product)
    db.session.commit()

    return product_schema.jsonify(delete_product)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)