import os
MOCK_ACCESS_CODE = "HHYJHDH#S234"


class PaymentService:

    def create_order(self):
        pass

    def pay(self, purchasable=None):
        pass

    def get_tag(self):
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


paystack_payment_service = PaystackPaymentService(api_key=os.getenv("PAYSTACK_SECRET_KEY"))
