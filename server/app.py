from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Import db and models
from server.models import db, Restaurant, Pizza, RestaurantPizza

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Update to appropriate URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True  # Enable testing mode

    # Initialize database and extensions
    db.init_app(app)
    migrate = Migrate(app, db)  # Flask-Migrate for database migrations
    CORS(app)  # Enable CORS for API calls

    # Initialize the API
    api = Api(app)

    # Define all API routes within the app context
    with app.app_context():
        db.create_all()  # Create tables only within the app context

    # 🏪 Get all restaurants
    class RestaurantList(Resource):
        def get(self):
            """Retrieve all restaurants."""
            restaurants = Restaurant.query.all()
            return [{"id": r.id, "name": r.name, "location": r.location} for r in restaurants], 200

    # 🍕 Get all pizzas
    class PizzaList(Resource):
        def get(self):
            """Retrieve all pizzas."""
            pizzas = Pizza.query.all()
            return [{"id": p.id, "name": p.name, "ingredients": p.ingredients} for p in pizzas], 200

    # 🍽️ Get menu for a specific restaurant
    class RestaurantMenu(Resource):
        def get(self, restaurant_id):
            """Retrieve a specific restaurant and its pizzas."""
            restaurant = Restaurant.query.get_or_404(restaurant_id)
            menu = [
                {
                    "id": rp.pizza.id,
                    "name": rp.pizza.name,
                    "ingredients": rp.pizza.ingredients,
                    "price": rp.price,
                }
                for rp in restaurant.restaurant_pizzas
            ]
            return {
                "id": restaurant.id,
                "name": restaurant.name,
                "pizzas": menu if menu else "No pizzas available for this restaurant"
            }, 200

    # ➕ Add a pizza to a restaurant (POST)
    class AddPizzaToRestaurant(Resource):
        def post(self):
            """Add a pizza to a restaurant with a price."""
            parser = reqparse.RequestParser()
            parser.add_argument("restaurant_id", type=int, required=True, help="Restaurant ID is required")
            parser.add_argument("pizza_id", type=int, required=True, help="Pizza ID is required")
            parser.add_argument("price", type=float, required=True, help="Price is required")
            args = parser.parse_args()

            # Validate restaurant and pizza
            restaurant = Restaurant.query.get(args["restaurant_id"])
            pizza = Pizza.query.get(args["pizza_id"])

            if not restaurant:
                return {"error": "Restaurant not found"}, 404
            if not pizza:
                return {"error": "Pizza not found"}, 404

            # Create new RestaurantPizza entry
            new_entry = RestaurantPizza(
                restaurant_id=args["restaurant_id"], pizza_id=args["pizza_id"], price=args["price"]
            )

            # Perform database operations within app context
            with app.app_context():
                db.session.add(new_entry)
                db.session.commit()

            return {"message": "Pizza added to restaurant menu successfully"}, 201

    # 🌍 Register API routes
    api.add_resource(RestaurantList, "/api/restaurants")
    api.add_resource(PizzaList, "/api/pizzas")
    api.add_resource(RestaurantMenu, "/api/restaurants/<int:restaurant_id>/menu")
    api.add_resource(AddPizzaToRestaurant, "/api/restaurant_pizzas")

    # 🔥 Root route
    @app.route("/")
    def index():
        return "<h1>🍕 Pizza API is Running! 🚀</h1>"

    return app  # ✅ Return the app instance

# 🏁 Run the app only when executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
