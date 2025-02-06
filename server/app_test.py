import pytest
from faker import Faker
from server.app import create_app, db
from server.models import Restaurant, RestaurantPizza, Pizza

fake = Faker()

# 🔥 Setup Test App with SQLite Memory Database
@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for testing."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory DB
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    """Provides a test client to make requests to the app."""
    return app.test_client()

@pytest.fixture(autouse=True)
def db_setup(app):
    """Ensures database is clean before each test."""
    with app.app_context():
        db.session.query(RestaurantPizza).delete()
        db.session.query(Restaurant).delete()
        db.session.query(Pizza).delete()
        db.session.commit()

class TestApp:
    """Flask API tests for restaurants, pizzas, and restaurant-pizzas"""

    def test_get_restaurants(self, client, app):
        """Test retrieving all restaurants"""
        with app.app_context():
            restaurant1 = Restaurant(name=fake.company(), address=fake.address())
            restaurant2 = Restaurant(name=fake.company(), address=fake.address())
            db.session.add_all([restaurant1, restaurant2])
            db.session.commit()

            response = client.get('/restaurants')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            data = response.json

            assert len(data) == 2
            assert data[0]['id'] == restaurant1.id
            assert data[1]['id'] == restaurant2.id

    def test_get_restaurant_by_id(self, client, app):
        """Test retrieving a single restaurant by its ID"""
        with app.app_context():
            restaurant = Restaurant(name=fake.company(), address=fake.address())
            db.session.add(restaurant)
            db.session.commit()

            response = client.get(f'/restaurants/{restaurant.id}')
            assert response.status_code == 200
            assert response.json['id'] == restaurant.id

    def test_restaurant_not_found(self, client):
        """Test retrieving a non-existent restaurant"""
        response = client.get('/restaurants/999')
        assert response.status_code == 404
        assert response.json.get('error') == "Restaurant not found"

    def test_delete_restaurant(self, client, app):
        """Test deleting a restaurant"""
        with app.app_context():
            restaurant = Restaurant(name=fake.company(), address=fake.address())
            db.session.add(restaurant)
            db.session.commit()

            response = client.delete(f'/restaurants/{restaurant.id}')
            assert response.status_code == 204

            # Ensure restaurant is deleted
            assert Restaurant.query.get(restaurant.id) is None

    def test_get_pizzas(self, client, app):
        """Test retrieving all pizzas"""
        with app.app_context():
            pizza1 = Pizza(name=fake.word(), ingredients=fake.sentence())
            pizza2 = Pizza(name=fake.word(), ingredients=fake.sentence())
            db.session.add_all([pizza1, pizza2])
            db.session.commit()

            response = client.get('/pizzas')
            assert response.status_code == 200
            assert len(response.json) == 2

    def test_create_restaurant_pizza(self, client, app):
        """Test adding a pizza to a restaurant"""
        with app.app_context():
            pizza = Pizza(name=fake.word(), ingredients=fake.sentence())
            restaurant = Restaurant(name=fake.company(), address=fake.address())
            db.session.add_all([pizza, restaurant])
            db.session.commit()

            response = client.post('/restaurant_pizzas', json={
                "price": 10,
                "pizza_id": pizza.id,
                "restaurant_id": restaurant.id,
            })
            assert response.status_code == 201
            assert response.json['price'] == 10

    def test_create_restaurant_pizza_validation(self, client, app):
        """Test validation errors for adding a pizza"""
        with app.app_context():
            pizza = Pizza(name=fake.word(), ingredients=fake.sentence())
            restaurant = Restaurant(name=fake.company(), address=fake.address())
            db.session.add_all([pizza, restaurant])
            db.session.commit()

            invalid_prices = [0, 50]
            for price in invalid_prices:
                response = client.post('/restaurant_pizzas', json={
                    "price": price,
                    "pizza_id": pizza.id,
                    "restaurant_id": restaurant.id,
                })
                assert response.status_code == 400
                assert response.json['errors'] == ["Price must be between 1 and 30"]

    def test_create_restaurant_pizza_missing_data(self, client, app):
        """Test missing data for creating a restaurant pizza"""
        with app.app_context():
            pizza = Pizza(name=fake.word(), ingredients=fake.sentence())
            restaurant = Restaurant(name=fake.company(), address=fake.address())
            db.session.add_all([pizza, restaurant])
            db.session.commit()

            # Missing price
            response = client.post('/restaurant_pizzas', json={
                "pizza_id": pizza.id,
                "restaurant_id": restaurant.id,
            })
            assert response.status_code == 400
            assert response.json['errors'] == ["Missing required field: price"]
