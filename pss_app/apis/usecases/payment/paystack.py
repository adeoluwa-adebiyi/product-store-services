def generate_order_access_code(order=None):

    if order is None:
        raise Exception("Order cannot be null")

    assert(isinstance(order,Order))

    pass
