from flask import Blueprint, request, jsonify
from models import db, Book, Category
import base64, json

bp = Blueprint('books', __name__, url_prefix='/api/v1/books')

def encode_cursor(data):
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")

def decode_cursor(token):
    pad = "=" * (-len(token) % 4)
    return json.loads(base64.urlsafe_b64decode(token + pad))

@bp.get("")
def list_books():
    strategy = request.args.get("strategy", "offset")
    genre = request.args.get("genre") 
    sort_raw = request.args.get("sort", "-id")
    limit = min(request.args.get("limit", 5, type=int), 100)
    
    query = Book.query

    # JOIN bảng Category để filter theo slug (genre)
    if genre:
        query = query.join(Category).filter(Category.slug == genre)

    # SORT: Đổi giá tiền thành price_vnd cho khớp DB
    ALLOWED_SORT = {"id": Book.id, "price": Book.price_vnd, "title": Book.title}
    cols = []
    
    for s in sort_raw.split(","):
        desc = s.startswith("-")
        key = s.lstrip("-")
        if key in ALLOWED_SORT:
            col = ALLOWED_SORT[key]
            cols.append(col.desc() if desc else col.asc())
            
    cols.append(Book.id.desc()) # Tie-break luôn là ID
    query = query.order_by(*cols)

    if strategy == "offset":
        offset = request.args.get("offset", 0, type=int)
        rows = query.offset(offset).limit(limit).all()
        return jsonify({
            "data": [b.to_dict() for b in rows],
            "pagination": {"strategy": "offset", "offset": offset, "limit": limit}
        })
        
    elif strategy == "cursor":
        raw_cursor = request.args.get("cursor")
        if raw_cursor:
            c = decode_cursor(raw_cursor)
            query = query.filter(Book.id < c["i"])
            
        rows = query.limit(limit + 1).all()
        has_more = len(rows) > limit
        items = rows[:limit]
        
        next_cursor = encode_cursor({"i": items[-1].id}) if items and has_more else None
            
        return jsonify({
            "data": [b.to_dict() for b in items],
            "pagination": {"strategy": "cursor", "next_cursor": next_cursor, "has_more": has_more}
        })