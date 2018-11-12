from flask_restful import reqparse, Resource, fields, abort, marshal_with

from app import db
from app.models import SKU, OrderLine

order_line_fields = {
    'id': fields.Integer,
    'sku': fields.String(attribute=lambda x: x.sku.name),
    'quantity': fields.Integer(attribute=lambda x: x.quantity),
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('sku', type=str, required=True, help='No product provided', location='json')
reqparse.add_argument('quantity', type=int, required=True, help='No quantity provided', location='json')


class OrderLineList(Resource):

    @marshal_with(order_line_fields)
    def get(self):
        return OrderLine.query.all()

    @marshal_with(order_line_fields)
    def post(self):
        parsed_args = reqparse.parse_args()
        sku = SKU.query.filter_by(name=parsed_args['sku']).first()
        if not sku:
            abort(404, message="Product {} does not exists".format(parsed_args['sku']))
        order_line = OrderLine(quantity=parsed_args['quantity'], sku=sku)
        db.session.add(order_line)
        db.session.commit()
        return order_line, 201


class OrderLineItem(Resource):

    @staticmethod
    def get_or_404(id):
        order = OrderLine.query.filter_by(id=id).first()
        if not order:
            abort(404, message="Order Line {} does not exists".format(id))
        return order

    @marshal_with(order_line_fields)
    def get(self, id):
        return self.get_or_404(id)

    @marshal_with(order_line_fields)
    def put(self, id):
        parsed_args = reqparse.parse_args()
        sku = SKU.query.filter_by(name=parsed_args['sku']).first()
        if not sku:
            abort(404, message="Product {} does not exists".format(parsed_args['sku']))
        order_line = OrderLine.query.filter_by(id=id).first()
        if not order_line:
            order_line = OrderLine(id=id)
        order_line.quantity = parsed_args['quantity']
        order_line.sku = sku
        db.session.add(order_line)
        db.session.commit()
        return order_line, 201

    @marshal_with(order_line_fields)
    def delete(self, id):
        order_line = self.get_or_404(id)
        db.session.delete(order_line)
        db.session.commit()
        return {}, 204

