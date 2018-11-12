from flask_restful import reqparse, Resource, fields, marshal_with, abort

from app.models import SKU, Storage

fulfil_fields = {
    'id': fields.Integer,
    'quantity': fields.Integer
}

fulfil_parser = reqparse.RequestParser()
fulfil_parser.add_argument('lines', type=dict, required=True, help='No orders provided', location='json',
                           action='append')


class Fulfillment(Resource):
    @marshal_with(fulfil_fields)
    def post(self):
        parsed_args = fulfil_parser.parse_args()
        lines = parsed_args['lines']
        result = []
        # explicit validation
        for order in lines:
            if "sku" not in order or not isinstance(order["sku"], str):
                abort(400, message="No product provided")
            if "quantity" not in order or not isinstance(order["quantity"], int):
                abort(400, message="No quantity provided")
            sku = SKU.query.filter_by(name=order["sku"]).first()
            if not sku:
                abort(404, message="Product {} does not exists".format(order['sku']))
            quantity = order["quantity"]
            storages = sku.storages
            storages.sort(key=lambda x: x.stock)
            for stor in storages:
                if quantity != 0:
                    # how many items to collect from this storage
                    amount = min(stor.stock, quantity)
                    quantity -= amount
                    result.append({"id": stor.id, "quantity": amount})
            if quantity > 0:
                abort(400, message="Not enough product in storages")
        return result

