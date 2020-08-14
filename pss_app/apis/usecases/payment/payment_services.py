import json
import os

from apis.models import Order
from rest_framework import status
from rest_framework.response import Response

from apis.models import PaymentDetails

MOCK_ACCESS_CODE = "HHYJHDH#S234"


class PaymentService:

    def create_order(self):
        pass

    def pay(self, purchasable=None):
        pass

    def get_tag(self):
        pass

    def handle_webhook(self, json_data=None):
        pass


class PaystackPaymentService(PaymentService):

    def __init__(self, api_key=None):
        self._api_key = api_key

    def create_order(self, checkout=None):
        pass

    def pay(self, purchasable=None):
        pass

    def get_tag(self):
        return "PAYSTACK"

    def get_access_code(self):
        return MOCK_ACCESS_CODE

    def handle_webhook(self, json_data=None):
        order = Order.objects.get(checkout__reference=json_data["data"]["reference"])
        order.payment_status = True if json_data["event"] == "charge.success" else False
        if order.payment_status:
            order.payment_details = PaymentDetails.objects.create(transaction_id=json_data["data"]["id"], reference=json_data["data"]["reference"], payment_gateway=self.get_tag(), json_dump=json.dumps(json_data))
        else:
            order.payment_details = PaymentDetails.objects.create(json_dump=json.dumps(json_data))

        order.save()


paystack_payment_service = PaystackPaymentService(api_key=os.getenv("PAYSTACK_SECRET_KEY"))
