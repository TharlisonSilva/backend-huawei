# app/infra/providers/customer_provider.py
from app import db
from app.infra.entities.customerEntity import CustomerEntity

class CustomerProvider:
    def get_all_customers(self):
        return CustomerEntity.query.all()

    def get_customer_by_id(self, customer_id):
        return CustomerEntity.query.filter_by(id=customer_id).first()

    def create_customer(self, data: dict):
        customer = CustomerEntity(**data)
        db.session.add(customer)
        db.session.commit()
        return customer

    def update_customer(self, customer_id, data: dict):
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return None
        for key, value in data.items():
            setattr(customer, key, value)
        db.session.commit()
        return customer

    def delete_customer(self, customer_id):
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False
        db.session.delete(customer)
        db.session.commit()
        return True
