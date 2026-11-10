from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models.product import Product
from .errors import Conflict, NotFound
from .schemas import ProductOut, ProductIn, ProductPatch, ReserveIn

products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")

@products_bp.get("")
def list_products():
    page = max(1, int(request.args.get("page", 1)))
    size = min(100, max(1, int(request.args.get("size", 20))))
    
    base = db.select(Product).where(Product.archived.is_(False))
    rows = db.session.execute(base.order_by(Product.id).offset((page-1) * size).limit(size)).scalars().all()
    total = db.session.scalar(db.select(db.func.count()).select_from(Product).where(Product.archived.is_(False)))
    
    return jsonify({
        "items": [ProductOut().dump(p) for p in rows],
        "page": page, "size": size, "total": total
    }), 200

@products_bp.get("/<int:id>")
def get_product(id):
    p = db.session.get(Product, id)
    if not p or p.archived: raise NotFound("Product not found")
    return jsonify(ProductOut().dump(p)), 200

@products_bp.post("")
def create_product():
    body = ProductIn().load(request.json)
    p = Product(**body)
    try:
        db.session.add(p)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Conflict(message="sku already exists")
    return jsonify(ProductOut().dump(p)), 201

@products_bp.patch("/<int:id>")
def patch_product(id):
    body = ProductPatch().load(request.json, partial=True)
    p = db.session.get(Product, id)
    if not p or p.archived: raise NotFound("Product not found")
    
    for k, v in body.items(): setattr(p, k, v)
    db.session.commit()
    return jsonify(ProductOut().dump(p)), 200

@products_bp.delete("/<int:id>")
def delete_product(id):
    p = db.session.get(Product, id)
    if not p or p.archived: raise NotFound("Product not found")
    
    p.archived = True
    db.session.commit()
    return "", 204

@products_bp.post("/<int:id>/reserve")
def reserve_product(id):
    body = ReserveIn().load(request.json)
    p = db.session.get(Product, id)
    if not p or p.archived: raise NotFound("Product not found")
    
    if p.qty_in_stock < body["qty"]: raise Conflict(message="Out of stock")
    p.qty_in_stock -= body["qty"]
    db.session.commit()
    return jsonify(ProductOut().dump(p)), 200