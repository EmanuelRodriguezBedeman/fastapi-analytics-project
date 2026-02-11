import os
import random
import sys
from datetime import datetime
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.review import Review

fake = Faker()
Faker.seed(12345)
random.seed(12345)

# ============================================================
# CONSTANTS
# ============================================================

CATEGORY_PRODUCTS = {
    "Electronics": ["Laptop", "Smartphone", "Headphones", "Tablet", "Monitor"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress"],
    "Books": ["Novel", "Textbook", "Cookbook", "Biography", "Guide"],
    "Home": ["Coffee Maker", "Blender", "Lamp", "Chair", "Rug"],
    "Sports": ["Running Shoes", "Yoga Mat", "Basketball", "Dumbbells", "Bicycle"],
}

PRODUCT_DESCRIPTIONS = {
    "Electronics": [
        "High-performance device with latest technology and sleek design.",
        "Advanced features with user-friendly interface and long battery life.",
        "Premium quality electronics with excellent durability and warranty.",
    ],
    "Clothing": [
        "Comfortable and stylish apparel made from premium materials.",
        "Durable fabric with modern fit and trendy design.",
        "High-quality clothing perfect for everyday wear.",
    ],
    "Books": [
        "Engaging and informative read with comprehensive coverage.",
        "Well-written content with clear explanations and examples.",
        "Must-read book offering valuable insights and knowledge.",
    ],
    "Home": [
        "Practical home essential with durable construction and modern design.",
        "High-quality household item combining functionality with style.",
        "Reliable home product built to last with easy maintenance.",
    ],
    "Sports": [
        "Professional-grade equipment designed for optimal performance.",
        "Durable sports gear built for intensive training.",
        "Ergonomic design providing comfort during extended use.",
    ],
}

REVIEW_TEMPLATES = {
    5: ["Excellent product! Highly recommend.", "Amazing quality!", "Best purchase ever!"],
    4: ["Great product, minor issues.", "Good quality.", "Very satisfied."],
    3: ["It's okay.", "Average product.", "Does the job."],
    2: ["Disappointed.", "Poor quality.", "Not as described."],
    1: ["Terrible!", "Waste of money.", "Do not buy!"],
}

COUNTRIES = [
    "USA",
    "Brazil",
    "Japan",
    "Germany",
    "UK",
    "Canada",
    "France",
    "Australia",
    "Spain",
    "Italy",
    "Mexico",
    "India",
]

# ============================================================
# SEEDING FUNCTIONS
# ============================================================


def create_customers(db: Session, num: int = 200):
    """Create customers"""
    print(f"Creating {num} customers...")
    customers = db.query(Customer).all()

    if len(customers) >= num:
        print(f"✅ Found {len(customers)} existing customers")
        return customers

    to_create = num - len(customers)
    print(f"Adding {to_create} new customers...")

    for _ in range(to_create):
        try:
            customer = Customer(
                email=fake.unique.email(),
                name=fake.name(),
                country=random.choice(COUNTRIES),
                city=fake.city(),
                signup_date=fake.date_between(start_date="-2y", end_date="today"),
            )
            db.add(customer)
        except:
            db.rollback()
            continue

    db.commit()
    customers = db.query(Customer).all()
    print(f"✅ Total customers: {len(customers)}")
    return customers


def create_products(db: Session, num: int = 100):
    """Create products with realistic descriptions"""
    print(f"Creating {num} products...")
    products = db.query(Product).all()

    if len(products) >= num:
        print(f"✅ Found {len(products)} existing products")
        return products

    to_create = num - len(products)
    print(f"Adding {to_create} new products...")

    for _ in range(to_create):
        category = random.choice(list(CATEGORY_PRODUCTS.keys()))
        product_type = random.choice(CATEGORY_PRODUCTS[category])
        brand = fake.company()

        product = Product(
            name=f"{brand} {product_type}",
            description=random.choice(PRODUCT_DESCRIPTIONS[category]),
            price=round(random.uniform(9.99, 499.99), 2),
            stock=random.randint(0, 500),
            category=category,
        )
        db.add(product)

    db.commit()
    products = db.query(Product).all()
    print(f"✅ Total products: {len(products)}")
    return products


def create_orders(db: Session, customers: list[Customer], products: list[Product], num: int = 3000):
    """Create orders with order_items"""
    print(f"Creating {num} orders...")

    if not customers or not products:
        print("❌ Cannot create orders: Missing customers or products")
        return

    existing_orders = db.query(Order).count()
    print(f"Existing orders: {existing_orders}")

    for i in range(num):
        customer = random.choice(customers)

        # Get status enum
        status_enum = random.choices(
            list(OrderStatus),
            weights=[5, 8, 10, 72, 5],  # pending, processing, shipped, delivered, cancelled
        )[0]

        order_date = fake.date_time_between(start_date="-1y")

        order = Order(
            customer_id=customer.id,
            total_amount=0.0,
            status=status_enum.value,
            shipping_address=fake.address(),
            created_at=order_date,
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # Create order items
        num_items = random.choices([1, 2, 3, 4], weights=[40, 35, 20, 5])[0]
        selected_products = random.sample(products, min(num_items, len(products)))

        total_amount = 0.0

        for product in selected_products:
            quantity = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
            price = product.price

            try:
                item = OrderItem(
                    order_id=order.id, product_id=product.id, quantity=quantity, price=price
                )
                db.add(item)
                total_amount += price * quantity
            except Exception as e:
                print(f"❌ Error creating order_item: {e}")
                db.rollback()
                continue

        # Update order total
        order.total_amount = round(total_amount, 2)
        db.add(order)

        # Commit batch
        if (i + 1) % 100 == 0 or (i + 1) == num:
            db.commit()

            # Verify order_items are being created
            item_count = db.query(OrderItem).count()
            print(f"  Progress: {i + 1}/{num} orders | Order_items total: {item_count}")

    final_count = db.query(OrderItem).count()
    print(f"✅ Created {num} orders with {final_count} order_items")


def create_reviews(db: Session, customers: list[Customer], products: list[Product], num: int = 500):
    """Create reviews"""
    print(f"Creating {num} reviews...")

    if not customers or not products:
        print("❌ Skipping reviews")
        return

    used_pairs = set()
    created = 0

    for i in range(num * 3):
        if created >= num:
            break

        customer = random.choice(customers)
        product = random.choice(products)
        pair = (customer.id, product.id)

        if pair in used_pairs:
            continue

        used_pairs.add(pair)
        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]

        review = Review(
            customer_id=customer.id,
            product_id=product.id,
            rating=rating,
            comment=random.choice(REVIEW_TEMPLATES[rating]),
            created_at=fake.date_time_between(start_date="-1y"),
        )
        db.add(review)
        created += 1

        if created % 100 == 0:
            db.commit()

    db.commit()
    print(f"✅ Created {created} reviews")


def verify_seeding(db: Session):
    """Verify all tables have data"""
    print("\n" + "=" * 60)
    print("📊 DATABASE SUMMARY")
    print("=" * 60)
    print(f"Customers:   {db.query(Customer).count()}")
    print(f"Products:    {db.query(Product).count()}")
    print(f"Orders:      {db.query(Order).count()}")
    print(f"Order Items: {db.query(OrderItem).count()}")  # ← Should show ~7,500
    print(f"Reviews:     {db.query(Review).count()}")
    print("=" * 60 + "\n")


def seed():
    """Main seeding function"""
    print("\n" + "=" * 60)
    print("🌱 ECOMMERCE DATABASE SEEDING")
    print("=" * 60 + "\n")

    db = SessionLocal()

    try:
        print(f"📡 Database: {engine.url.database} @ {engine.url.host}\n")

        customers = create_customers(db, num=200)
        products = create_products(db, num=100)
        create_orders(db, customers, products, num=3000)
        create_reviews(db, customers, products, num=500)

        verify_seeding(db)  # ← Check order_items count!

        print("✅ SEEDING COMPLETE!\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
