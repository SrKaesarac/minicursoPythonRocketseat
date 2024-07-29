from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # orm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  price = db.Column(db.Float, nullable=False)
  description = db.Column(db.Text, nullable=True)


@app.route('/api/products/add', methods=["POST"])
def add_product():
  data = request.json
  if 'name' in data and 'price' in data:
    product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))# os dois primeiros métodos resultam em erro ao não encontrar dados, o terceiro método printa vazio
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product Added Successfully"})  
  return jsonify({"message": "Invalid Product Data"}), 400  

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
  product = Product.query.get(product_id)
  if product:
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product Deleted Successfully"})  
  return jsonify({"message": "Product not Found"}), 404

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
  product = Product.query.get(product_id)
  if product:
    return jsonify({
      "id": product.id,
      "name": product.name,
      "price": product.price,
      "description": product.description
    })
  return jsonify({"message": "Product not Found"}), 404

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
  product = Product.query.get(product_id)
  if not product: # not: nega o que está a frente
    return jsonify({"message": "Product not Found"}), 404
  
  data = request.json
  if 'name' in data:
    product.name = data['name']
  if 'price' in data:
    product.price = data['price']
  if 'description' in data:
    product.description = data['description']

  db.session.commit()
  return jsonify({"message": "Product Updated Successfully"})

@app.route('/api/products', methods=['GET'])
def get_products():
  product_list = []
  products = Product.query.all() # todos os produtos armazenados em uma LISTA
  for product in products:
    product_data = {
      "id": product.id,
      "name": product.name,
      "price": product.price,
    }
    product_list.append(product_data)
  return jsonify(product_list)

@app.route('/')
def hello():
  return 'Hello World'

if __name__ == "__main__":
  app.run(debug=True)