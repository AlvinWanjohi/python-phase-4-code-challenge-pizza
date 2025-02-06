import pytest
from server.app import create_app, db
from server.models import Restaurant, Pizza, RestaurantPizza

@pytest.fixture(scope="module")
def test_app():
    """Create and configure a new app instance for testing."""
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory DB for testing
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True

    # Ensure the app context is available for DB operations
    with app.app_context():
        db.create_all()  # Create tables
        yield app  # Yield the app instance for tests

        # Clean up after tests
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="module")
def client(test_app):
    """Creates a test client for making requests."""
    return test_app.test_client()

@pytest.fixture(scope="module")
def init_database(test_app):
    """Sets up test data in the database."""
    with test_app.app_context():
        # Create some test data
        r1 = Restaurant(name="Pasta Palace", address="123 Pasta St.")
        r2 = Restaurant(name="Pizza Haven", address="456 Pizza Ave.")
        db.session.add_all([r1, r2])
        db.session.commit()

        p1 = Pizza(name="Margherita", ingredients="Tomato, Mozzarella, Basil")
        p2 = Pizza(name="Pepperoni", ingredients="Tomato, Mozzarella, Pepperoni")
        db.session.add_all([p1, p2])
        db.session.commit()

        rp1 = RestaurantPizza(restaurant_id=r1.id, pizza_id=p1.id, price=12)
        rp2 = RestaurantPizza(restaurant_id=r2.id, pizza_id=p2.id, price=15)
        db.session.add_all([rp1, rp2])
        db.session.commit()

        yield  # Yield for the tests to use the database

        # Cleanup after tests
        with test_app.app_context():
            db.session.remove()
            db.drop_all()
