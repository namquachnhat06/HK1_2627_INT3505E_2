from flask import Blueprint, jsonify
from sqlalchemy.orm import selectinload
from ..extensions import db
from ..models.order import Order
from .schemas import OrderOut

orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")

@orders_bp.get("")
def list_orders():
    stmt = db.select(Order).options(selectinload(Order.items))
    orders = db.session.execute(stmt).scalars().all()
    return jsonify([OrderOut().dump(o) for o in orders]), 200