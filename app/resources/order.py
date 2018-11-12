from flask_restful import reqparse, Resource, fields, abort, marshal_with

from app import db
from app.models import Order
from app.resources import non_empty_string
from app.utils import normalizer

order_fields = {
    'id': fields.Integer,
    'customer': fields.String
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('customer', type=non_empty_string, required=True, help='No customer name provided',
                      location='json')


class OrderList(Resource):

    @marshal_with(order_fields)
    def get(self):
        return Order.query.all()

    @marshal_with(order_fields)
    def post(self):
        parsed_args = reqparse.parse_args()
        order = Order(customer=parsed_args['customer'])
        order.normalized = normalizer(order.customer)
        db.session.add(order)
        db.session.commit()
        return order, 201


class OrderItem(Resource):

    @staticmethod
    def get_or_404(id):
        order = Order.query.filter_by(id=id).first()
        if not order:
            abort(404, message="Order {} does not exists".format(id))
        return order

    @marshal_with(order_fields)
    def get(self, id):
        return self.get_or_404(id)

    @marshal_with(order_fields)
    def put(self, id):
        parsed_args = reqparse.parse_args()
        order = Order.query.filter_by(id=id).first()
        if not order:
            order = Order(id=id)
        order.customer = parsed_args['customer']
        order.normalized = normalizer(order.customer)
        db.session.add(order)
        db.session.commit()
        return order, 201

    @marshal_with(order_fields)
    def delete(self, id):
        order = self.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return {}, 204

