import pytest
from app import create_app, db
from models import Restaurant, RestaurantPizza, Pizza

# Fixture to set up the test app with the appropriate configurations
@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # Use a test database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking
    app.config["TESTING"] = True  # Enable testing mode

    # Initialize the database within the app context
    with app.app_context():
        db.create_all()  # Create all tables
        yield app  # Yield the app for the test
        db.session.remove()  # Close the session after tests
        db.drop_all()  # Drop the tables after tests

# Fixture to create the test client using the test app
@pytest.fixture(scope="module")
def client(test_app):
    return test_app.test_client()

# Fixture to initialize the database with sample data
@pytest.fixture(scope="module")
def init_database(test_app):
    """Fixture to create sample data."""
    with test_app.app_context():
        # Create sample restaurants
        r1 = Restaurant(name="Pasta Palace", address="123 Pasta St.")
        r2 = Restaurant(name="Pizza Haven", address="456 Pizza Ave.")
        
        db.session.add_all([r1, r2])
        db.session.commit()

        # Create pizzas
        p1 = Pizza(name="Margherita", price=12.00, ingredients="Tomato, Mozzarella, Basil")
        p2 = Pizza(name="Pepperoni", price=15.00, ingredients="Tomato, Mozzarella, Pepperoni")
        
        db.session.add_all([p1, p2])
        db.session.commit()

        # Create RestaurantPizza associations (many-to-many relationship)
        rp1 = RestaurantPizza(restaurant_id=r1.id, pizza_id=p1.id, price=12)
        rp2 = RestaurantPizza(restaurant_id=r2.id, pizza_id=p2.id, price=15)
        
        db.session.add_all([rp1, rp2])
        db.session.commit()

        yield db  # Yield the database session to the test functions

        db.session.remove()  # Remove the session after tests
        db.drop_all()  # Clean up the database after tests

# Test for retrieving all restaurants
def test_get_restaurants(client, init_database):
    """Test to check if all restaurants are retrieved correctly."""
    response = client.get('/api/restaurants')
    assert response.status_code == 200
    assert len(response.json) == 2  # We have two restaurants
    assert "Pasta Palace" in str(response.data)  # Check if Pasta Palace is in the response
    assert "Pizza Haven" in str(response.data)  # Check if Pizza Haven is in the response

# Test for retrieving all pizzas
def test_get_pizzas(client, init_database):
    """Test to check if all pizzas are retrieved correctly."""
    response = client.get('/api/pizzas')
    assert response.status_code == 200
    assert len(response.json) == 2  # We have two pizzas
    assert "Margherita" in str(response.data)  # Check if Margherita is in the response
    assert "Pepperoni" in str(response.data)  # Check if Pepperoni is in the response

# Test for retrieving the menu of a specific restaurant
def test_get_restaurant_menu(client, init_database):
    """Test to check if the restaurant's menu is retrieved correctly."""
    response = client.get('/api/restaurants/1/menu')
    assert response.status_code == 200
    assert "Margherita" in str(response.data)  # Check if the Margherita pizza is in the menu

# Test for handling a non-existent restaurant
def test_get_non_existent_restaurant(client, init_database):
    """Test to check the behavior when a non-existent restaurant is requested."""
    response = client.get('/api/restaurants/999/menu')  # Non-existent restaurant ID
    assert response.status_code == 404  # Should return 404 Not Found
    assert "Not Found" in str(response.data)  # Check if "Not Found" is in the response
