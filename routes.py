from flask_restful import Resource
from app import db
from models import Restaurant, Pizza, RestaurantPizza

class RestaurantList(Resource):
    def get(self):
        """Retrieve all restaurants."""
        restaurants = Restaurant.query.all()
        
        # Return a list of restaurants in JSON format
        return [
            {"id": r.id, "name": r.name, "location": r.location} for r in restaurants
        ], 200

class PizzaList(Resource):
    def get(self):
        """Retrieve all pizzas."""
        pizzas = Pizza.query.all()

        # Return a list of pizzas in JSON format
        return [
            {"id": p.id, "name": p.name, "price": p.price, "ingredients": p.ingredients}
            for p in pizzas
        ], 200

class RestaurantMenu(Resource):
    def get(self, restaurant_id):
        """Retrieve the menu for a specific restaurant."""
        # Retrieve the restaurant by ID, or return a 404 error if not found
        restaurant = Restaurant.query.get_or_404(restaurant_id)

        # Retrieve the pizzas related to the specific restaurant via the RestaurantPizza relationship
        menu = []
        for rp in restaurant.restaurant_pizzas:
            pizza = rp.pizza  # Accessing the associated Pizza object via the relationship
            menu.append({
                "id": pizza.id,
                "name": pizza.name,
                "price": rp.price  # Get the price for this restaurant-specific pizza
            })

        if not menu:  # If no pizzas are available
            return {
                "error": "No pizzas available for this restaurant."
            }, 404
        
        return {
            "id": restaurant.id,
            "name": restaurant.name,
            "location": restaurant.location,
            "menu": menu
        }, 200
