from app import app, db
from models import Restaurant, Pizza, RestaurantPizza
from faker import Faker

fake = Faker()

# Using app context to interact with the database
with app.app_context():
    # Ensure tables are created
    db.create_all()

    # Create sample restaurants
    r1 = Restaurant(name="Pasta Palace", location="Downtown")
    r2 = Restaurant(name="Pizza Haven", location="Uptown")
    r3 = Restaurant(name="Sushi Spot", location="Midtown")
    r4 = Restaurant(name="Burger King", location="Eastside")

    # Create sample pizzas with valid price range (1-30)
    p1 = Pizza(name="Margherita", price=12, ingredients="Tomato, Mozzarella, Basil")
    p2 = Pizza(name="Pepperoni", price=15, ingredients="Tomato, Mozzarella, Pepperoni")
    p3 = Pizza(name="Hawaiian", price=18, ingredients="Tomato, Mozzarella, Ham, Pineapple")
    p4 = Pizza(name="BBQ Chicken", price=22, ingredients="BBQ Sauce, Chicken, Red Onion")
    p5 = Pizza(name="Vegetarian", price=10, ingredients="Tomato, Mozzarella, Bell Pepper, Olives")

    # Add restaurants and pizzas to the session
    db.session.add_all([r1, r2, r3, r4, p1, p2, p3, p4, p5])
    db.session.commit()  # Commit after adding the restaurants and pizzas

    # Associate restaurants with pizzas via RestaurantPizza with price validation (between 1 and 30)
    rp1 = RestaurantPizza(restaurant_id=r1.id, pizza_id=p1.id, price=12)  # Valid price
    rp2 = RestaurantPizza(restaurant_id=r2.id, pizza_id=p2.id, price=15)  # Valid price
    rp3 = RestaurantPizza(restaurant_id=r3.id, pizza_id=p3.id, price=18)  # Valid price
    rp4 = RestaurantPizza(restaurant_id=r4.id, pizza_id=p4.id, price=22)  # Valid price
    rp5 = RestaurantPizza(restaurant_id=r1.id, pizza_id=p5.id, price=10)  # Valid price

    # Add the relationships to the session
    db.session.add_all([rp1, rp2, rp3, rp4, rp5])
    db.session.commit()  # Final commit to save all changes

    print("Database seeded successfully!")
