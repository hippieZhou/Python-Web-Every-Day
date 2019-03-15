from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    __tablename = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

    def __repr__(self):
        return '<Product %r>' % self.name


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'hello world'})


@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(
        name=name, description=description, price=price, qty=qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    result = product_schema.dump(product)
    return jsonify(result)


@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    product.name = request.json['name']
    product.description = request.json['description']
    product.price = request.json['price']
    product.qty = request.json['qty']

    db.session.commit()

    return product_schema.jsonify(product)


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
