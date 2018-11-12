from flask_restful import reqparse, Resource, fields, abort, marshal_with

from app import db
from app.models import SKU, Storage

storage_fields = {
    'id': fields.Integer,
    'quantity': fields.Integer(attribute=lambda x: x.stock),
    'sku': fields.String(attribute=lambda x: x.sku.name)
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('quantity', type=int, required=True, help='No stock amount provided (quantity)', location='json')
reqparse.add_argument('sku', type=str, required=True, help='No product provided', location='json')


class StorageList(Resource):

    @marshal_with(storage_fields)
    def get(self):
        return Storage.query.all()

    @marshal_with(storage_fields)
    def post(self):
        parsed_args = reqparse.parse_args()
        sku = SKU.query.filter_by(name=parsed_args['sku']).first()
        if not sku:
            abort(404, message="Product {} does not exists".format(parsed_args['sku']))
        storage = Storage(stock=parsed_args['quantity'], sku=sku)
        db.session.add(storage)
        db.session.commit()
        return storage, 201


class StorageItem(Resource):

    @staticmethod
    def get_or_404(id):
        storage = Storage.query.filter_by(id=id).first()
        if not storage:
            abort(404, message="Storage {} does not exists".format(id))
        return storage

    @marshal_with(storage_fields)
    def get(self, id):
        return self.get_or_404(id)

    @marshal_with(storage_fields)
    def put(self, id):
        parsed_args = reqparse.parse_args()
        sku = SKU.query.filter_by(name=parsed_args['sku']).first()
        if not sku:
            abort(404, message="Product {} does not exists".format(parsed_args['sku']))
        storage = Storage.query.filter_by(id=id).first()
        if not storage:
            storage = Storage(id=id)
        storage.stock = parsed_args['quantity']
        storage.sku = sku
        db.session.add(storage)
        db.session.commit()
        return storage, 201

    @marshal_with(storage_fields)
    def delete(self, id):
        storage = self.get_or_404(id)
        db.session.delete(storage)
        db.session.commit()
        return {}, 204

