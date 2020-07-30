class PaymentService:

    def create_order(self):
        pass

    def pay(self, purchasable=None):
        pass


class PaystackPaymentService(PaymentService):

    def __init__(self, api_key=None):
        self._api_key = api_key

    def create_order(self):
        pass

    def pay(self, purchasable=None):
        pass
