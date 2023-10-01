from app import app 
from models import Restaurant, RestaurantPizza, Pizza,db
from datetime import datetime

def seed_data():
    
    restaurant1 = Restaurant(name='Dominion Pizza', address='Good Italian, Ngong Road, 5th Avenue')
    restaurant2 = Restaurant(name='Pizza Hut', address='Westgate Mall, Mwanzi Road, Nrb 100')

    
    pizza1 = Pizza(name='Cheese', ingredients='Dough, Tomato Sauce, Cheese', created_at=datetime.now(), updated_at=datetime.now())
    pizza2 = Pizza(name='Pepperoni', ingredients='Dough, Tomato Sauce, Cheese, Pepperoni', created_at=datetime.now(), updated_at=datetime.now())

    
    restaurant_pizza1 = RestaurantPizza(price=10.99, pizza=pizza1.id, restaurant=restaurant1.id)
    restaurant_pizza2 = RestaurantPizza(price=12.99, pizza=pizza2.id, restaurant=restaurant1.id)
    restaurant_pizza3 = RestaurantPizza(price=11.99, pizza=pizza1.id, restaurant=restaurant2.id)

    
    db.session.add_all([restaurant1, restaurant2, pizza1, pizza2, restaurant_pizza1, restaurant_pizza2, restaurant_pizza3])
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        seed_data()
        print('Data seeded successfully.')