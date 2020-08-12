import json

from paystackapi.transaction import  Transaction
from apis.models import Order
from apis.usecases.checkout.checkout import create_unique_uuid_string
from apis.usecases.payment.payment_services import paystack_payment_service


class OrderService:

    def __init__(self, payment_service=None):
        self.payment_service = payment_service

    def create_order(self, checkout=None):
        if checkout is None:
            raise Exception("checkout cannot be null")
        response = Transaction.initialize(reference=str(checkout.reference), amount=checkout.total, email=checkout.customer.email)
        order = Order.objects.create(reference=create_unique_uuid_string(), checkout=checkout, access_code=response["data"]["access_code"])
        return order


order_service = OrderService(payment_service=paystack_payment_service)
