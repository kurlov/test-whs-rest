from flask_restful import reqparse, Resource, fields, abort, marshal_with

from app import db
from app.models import SKU
from app.resources import non_empty_string

sku_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('name', type=non_empty_string, required=True, help='No product name provided', location='json')


class SKUList(Resource):

    @marshal_with(sku_fields)
    def get(self):
        return SKU.query.all()

    @marshal_with(sku_fields)
    def post(self):
        parsed_args = reqparse.parse_args()
        sku = SKU(name=parsed_args['name'])
        db.session.add(sku)
        db.session.commit()
        return sku, 201


class SKUItem(Resource):

    @staticmethod
    def get_or_404(id):
        sku = SKU.query.filter_by(id=id).first()
        if not sku:
            abort(404, message="Product {} does not exists".format(id))
        return sku

    @marshal_with(sku_fields)
    def get(self, id):
        return self.get_or_404(id)

    @marshal_with(sku_fields)
    def put(self, id):
        parsed_args = reqparse.parse_args()
        sku = SKU.query.filter_by(id=id).first()
        if not sku:
            sku = SKU(id=id, name=parsed_args['name'])
        else:
            sku.name = parsed_args['name']
        db.session.add(sku)
        db.session.commit()
        return sku, 201

    @marshal_with(sku_fields)
    def delete(self, id):
        sku = self.get_or_404(id)
        db.session.delete(sku)
        db.session.commit()
        return {}, 204

