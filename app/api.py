from flask import Blueprint, request
from flask.json import jsonify
from flask_restful import Api

from app.models import Order
from app.resources.fulfil import Fulfillment
from app.resources.order import OrderItem, OrderList
from app.resources.order_line import OrderLineItem, OrderLineList
from app.resources.sku import SKUList, SKUItem
from app.resources.storage import StorageList, StorageItem

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(SKUList, '/skus')
api.add_resource(SKUItem, '/skus/<int:id>')
api.add_resource(StorageList, '/storages')
api.add_resource(StorageItem, '/storages/<int:id>')
api.add_resource(OrderList, '/orders')
api.add_resource(OrderItem, '/orders/<int:id>')
api.add_resource(OrderLineList, '/order_lines')
api.add_resource(OrderLineItem, '/order_lines/<int:id>')
api.add_resource(Fulfillment, '/fulfil')


@api_bp.route('/search')
def search_order():
    """
    Search endpoint for an order

    :return: JSON
    """
    q = request.args.get('q').lower()
    order = Order.search(q)
    if not order:
        return jsonify({"message": "no orders for {}".format(q)})
    else:
        return jsonify({"result": order.customer})
