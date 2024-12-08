from firebase_admin import firestore
from datetime import datetime

class Product:
    def __init__(self, id=None, name=None, category=None, price=None):
        self.id = id
        self.name = name
        self.category = category
        self.price = price

    @staticmethod
    def get_all():
        db = firestore.client()
        products = db.collection('products').stream()
        return [Product(
            id=product.id,
            name=product.to_dict().get('name'),
            category=product.to_dict().get('category'),
            price=product.to_dict().get('price')
        ) for product in products]

class Purchase:
    def __init__(self, id=None, category=None, customer_id=None, date=None, 
                 item_name=None, quantity=None, timestamp=None, total=None, unit_price=None):
        self.id = id
        self.category = category
        self.customer_id = customer_id
        self.date = date
        self.item_name = item_name
        self.quantity = quantity
        self.timestamp = timestamp
        self.total = total
        self.unit_price = unit_price

    @staticmethod
    def get_all():
        db = firestore.client()
        purchases = db.collection('purchases').stream()
        return [Purchase(
            id=purchase.id,
            category=purchase.to_dict().get('category'),
            customer_id=purchase.to_dict().get('customer_id'),
            date=purchase.to_dict().get('date'),
            item_name=purchase.to_dict().get('item_name'),
            quantity=purchase.to_dict().get('quantity'),
            timestamp=purchase.to_dict().get('timestamp'),
            total=purchase.to_dict().get('total'),
            unit_price=purchase.to_dict().get('unit_price')
        ) for purchase in purchases]

    @staticmethod
    def create(data):
        db = firestore.client()
        doc_ref = db.collection('purchases').document()
        # Add timestamp
        data['timestamp'] = datetime.now().strftime("%B %d, %Y at %I:%M:%S %p UTC+8")
        doc_ref.set(data)
        return Purchase(id=doc_ref.id, **data)

