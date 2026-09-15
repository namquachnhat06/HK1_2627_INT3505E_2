from flask import Flask, jsonify
app = Flask(__name__)
ORDERS = [
    {"id": "1", "status": "pending"},
    {"id": "2", "status": "shipped"},
    {"id": "3", "status": "delivered"},
] # giả lập DB
def get(order_id):
    for order in ORDERS:
        if order["id"] == order_id:
            return order
    return None

# DELETE /orders/<id>
@app.route("/orders/<order_id>", methods=["DELETE"])  
def delete_order(order_id):
    order = get(order_id)
    # 404 — không tìm thấy
    if order is None:
        return {"error": "Order not found"}, 404
    # 409 — business rule
    if order["status"] in ("shipped", "delivered"):
        return {"error":"cannot delete"}, 409
    ORDERS.remove(order)
    # 204 — success, no body
    return "", 204
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)