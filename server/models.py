# Import necessary modules and classes
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy_serializer import SerializerMixin
from flask_migrate import Migrate

# Create a SQLAlchemy instance
db = SQLAlchemy()

# Define the Restaurant model with associated table and relationships
class Restaurant(db.Model, SerializerMixin):
    # Specify the table name
    __tablename__ = 'restaurants'

    # Define columns for the restaurant table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(120), nullable=False)

    # Define a relationship to RestaurantPizza (one-to-many)
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', lazy=True)

    # Add a UniqueConstraint with a name for the name column
    __table_args__ = (
        UniqueConstraint('name', name='unique_name_constraint'),
    )

    def __repr__(self):
        return '<restaurant %r>' % self.name

# Define the RestaurantPizza model with associated table and relationships
class RestaurantPizza(db.Model):
    # Specify the table name
    __tablename__ = 'restaurant_pizzas'

    # Define columns for the restaurant_pizzas table
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    # Define relationships to Pizza and Restaurant (many-to-one)
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas', lazy=True)
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas', lazy=True)  
    
    # Add a CheckConstraint with a name for the price column
    __table_args__ = (
        CheckConstraint('price BETWEEN 1 AND 30', name='check_price_range_constraint'),
    )

    def __repr__(self):
        return '<restaurant_pizza %r>' % self.price

# Define the Pizza model with associated table and relationships
class Pizza(db.Model, SerializerMixin):
    # Specify the table name
    __tablename__ = 'pizzas'

    # Define columns for the pizzas table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ingredients = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # Define a relationship to RestaurantPizza (one-to-many)
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza', lazy=True)

    def __repr__(self):
        return '<pizza %r>' % self.name