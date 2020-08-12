from graphene import Mutation, String, Field, Float, Int, ObjectType
from apis.usecases.checkout.checkout import checkout_service
from apis.usecases.orders.orders import order_service
from apis.models import User

import json


class OrderObject(ObjectType):
    access_code = String()
    reference = String()


class CheckoutShopping(Mutation):

    class Arguments:
        data = String()

    order = Field(OrderObject)

    def mutate(root, info, data):
        with open("debug.txt", "w") as _file:
            _file.write(data)
        _data = json.loads(data)
        checkout = checkout_service.create_checkout(data=_data, user=User.objects.all().first())
        order = order_service.create_order(checkout=checkout)
        return CheckoutShopping(order=OrderObject(access_code=order.access_code, reference=order.reference))


class RootMutation(ObjectType):

    checkout = CheckoutShopping.Field()
