from apis.models import Checkout, User, Product, CheckoutProductsInfo
import uuid
from apis.usecases.payment.payment_services import PaystackPaymentService
import os


def create_unique_uuid_string():
    _id = uuid.uuid4()
    if Checkout.objects.filter(reference=_id).exists():
        create_unique_uuid_string()
    else:
        return _id


class CheckoutService:
    def __init__(self, payment_service=None):
        self.payment_service = payment_service
        pass

    def create_unique_uuid(self):
        return create_unique_uuid_string()

    def get_total_price_of_checkout(self, checkout=None):
        if checkout is None:
            return 0
        else:
            sum = 0
            for item in checkout:
                sum += Product.objects.get(id=item["id"]).price * item["quantity"]

        return sum

    def create_checkout(self, data=None, user=None):
        if data is None:
            raise Exception("Checkout data cannot be null")

        if user is None:
            raise Exception("User data cannot be null")

        checkout = Checkout.objects.create(reference=self.create_unique_uuid(), customer=user, payment_service=self.payment_service.get_tag(), total=self.get_total_price_of_checkout(checkout=data["data"]["checkout"]))
        for item in data["data"]["checkout"]:
            product = Product.objects.get(id=item["id"])
            checkout_product_info = CheckoutProductsInfo.objects.create(checkout=checkout, product=product, quantity=item["quantity"], sub_total=product.price * item["quantity"])
        return checkout


checkout_service = CheckoutService(payment_service=PaystackPaymentService(api_key=os.getenv("PAYSTACK_SECRET_KEY")))