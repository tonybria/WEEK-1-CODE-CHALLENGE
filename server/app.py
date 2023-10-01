# Import necessary modules and classes from Flask and related extensions
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import custom models from the 'models' module
from models import db, Restaurant, RestaurantPizza, Pizza

# Create a Flask application instance
app = Flask(__name__)

# Configure the Flask app to use a SQLite database named 'app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Disable Flask-SQLAlchemy's modification tracking for better performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a migration object associated with the Flask app
migrate = Migrate(app, db)

# Initialize the database with the Flask app
db.init_app(app)

# Define a route for the root URL, returning a welcome message
@app.route('/')
def index():
    return 'Welcome to the best pizza'

# Define a route for retrieving a list of all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    # Query the Restaurant model to get all restaurants
    restaurants = Restaurant.query.all()

    # Create a list of dictionaries representing restaurant data
    restaurant_list = [
        {
            'id': r.id,
            'name': r.name,
            'address': r.address
        }
        for r in restaurants
    ]

    # Return the restaurant data as JSON
    return jsonify(restaurant_list)

# Define a route for retrieving details of a specific restaurant by ID
@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    # Query the Restaurant model to get the restaurant with the specified ID
    r = Restaurant.query.get(restaurant_id)

    if r:
        # Create a dictionary representing restaurant data
        restaurant_data = {
            'id': r.id,
            'name': r.name,
            'address': r.address
        }

        # Return the restaurant data as JSON
        return jsonify(restaurant_data)
    else:
        # Return a 404 error response if the restaurant is not found
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)

# Define a route for deleting a restaurant and its associated pizzas by ID
@app.route('/restaurants/<int:restaurant_id>/pizzas', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    # Query the Restaurant model to get the restaurant with the specified ID
    r = Restaurant.query.get(restaurant_id)

    if r:
        # Delete associated records from RestaurantPizza model (assuming foreign key relationship)
        RestaurantPizza.query.filter_by(restaurant_id=restaurant_id).delete()

        # Delete the restaurant from the database and commit the transaction
        db.session.delete(r)
        db.session.commit()

        # Return a success message as JSON
        return jsonify({'message': 'Restaurant deleted'}), 200
    else:
        # Return a 404 error response if the restaurant is not found
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)

# Define a route for retrieving a list of all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    # Query the Pizza model to get all pizzas
    pizzas = Pizza.query.all()

    # Create a list of dictionaries representing pizza data
    pizza_list = [
        {
            'id': p.id,
            'name': p.name,
            'ingredients': p.ingredients
        }
        for p in pizzas
    ]

    # Return the pizza data as JSON
    return jsonify(pizza_list)

# Define a route for creating a new restaurant-pizza association
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    # Retrieve JSON data from the request
    data = request.get_json()
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    price = data.get('price')

    

    # Check if both pizza_id and restaurant_id are valid
    if not (Pizza.query.get(pizza_id) and Restaurant.query.get(restaurant_id)):
        # Return a 400 error response with validation errors
        return make_response(jsonify({'errors': ['Invalid pizza_id or restaurant_id']}), 400)

    # Create a new RestaurantPizza record
    new_restaurant_pizza = RestaurantPizza(pizza_id=pizza_id, restaurant_id=restaurant_id, price=price)

    try:
        # Add the new record to the database and commit the transaction
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        # Retrieve associated pizza data
        pizza = Pizza.query.get(pizza_id)
        pizza_data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }

        # Return the pizza data as JSON with a 201 (Created) status
        return jsonify(pizza_data), 201
    except Exception as e:
        # Rollback the transaction in case of validation errors and return a 400 error response
        db.session.rollback()
        return make_response(jsonify({'errors': ['Validation errors']}), 400)

# Run the Flask app in debug mode if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)