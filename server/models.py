from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Restaurant Model: Represents a restaurant
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)  # Address field added

    # Relationship for many-to-many via 'RestaurantPizza' table
    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')

    def __repr__(self):
        return f"<Restaurant {self.name}, {self.address}>"

    # Validation for name field
    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 1:
            raise ValueError("Restaurant name cannot be empty.")
        return name


# Pizza Model: Represents a pizza
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(255), nullable=True)

    # Relationship for many-to-many via 'RestaurantPizza' table
    restaurants = db.relationship('RestaurantPizza', back_populates='pizza')

    def __repr__(self):
        return f"<Pizza {self.name}>"

    # Validation for name field
    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 1:
            raise ValueError("Pizza name cannot be empty.")
        return name


# RestaurantPizza Model: Intermediate table for the many-to-many relationship between Restaurant and Pizza
class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)

    # Relationships to link with 'Restaurant' and 'Pizza'
    restaurant = db.relationship('Restaurant', back_populates='pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurants')

    def __repr__(self):
        return f"<RestaurantPizza {self.restaurant.name} - {self.pizza.name}, Price: {self.price}>"

    # Constructor to set price with validation
    def __init__(self, restaurant_id, pizza_id, price):
        self.restaurant_id = restaurant_id
        self.pizza_id = pizza_id
        self.price = price  # Using the setter method for validation

    # Use @validates decorator to validate price before setting it
    @validates('price')
    def validate_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError("Price must be between 1 and 30")
        return price

# Example of how to use these models:

# Create a restaurant and a pizza
restaurant = Restaurant(name="Pasta Palace", address="123 Pasta St.")
pizza = Pizza(name="Margherita", ingredients="Tomato, Mozzarella, Basil")

# Add restaurant and pizza to the database
db.session.add(restaurant)
db.session.add(pizza)
db.session.commit()

# Create a RestaurantPizza entry with price
restaurant_pizza = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=15.00)

# Add the restaurant_pizza to the session and commit
db.session.add(restaurant_pizza)
db.session.commit()

# Retrieve and check the saved data
retrieved_restaurant_pizza = RestaurantPizza.query.first()
print(retrieved_restaurant_pizza)
