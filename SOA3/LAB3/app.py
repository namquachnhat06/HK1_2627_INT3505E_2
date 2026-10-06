import base64
import json
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# Giả lập Database Orders
ORDERS = [
    {"id": 1, "total": 150.0, "status": "paid", "customer_id": 10},
    {"id": 2, "total": 200.0, "status": "pending", "customer_id": 11},
    {"id": 3, "total": 50.0, "status": "paid", "customer_id": 10},
    {"id": 4, "total": 300.0, "status": "refunded", "customer_id": 12},
    {"id": 5, "total": 120.0, "status": "paid", "customer_id": 11},
]

class ApiProblem(Exception):
    def __init__(self, status, title, detail=None, type_path=None):
        self.status = status
        self.title = title
        self.detail = detail
        self.type = f"https://api.example.com/probs/{type_path}" if type_path else "about:blank"

@app.errorhandler(ApiProblem)
def handle_api_problem(e):
    body = {"type": e.type, "title": e.title, "status": e.status, "instance": request.path, "trace_id": str(uuid.uuid4())}
    if e.detail: body["detail"] = e.detail
    resp = jsonify(body)
    resp.status_code = e.status
    resp.headers["Content-Type"] = "application/problem+json"
    return resp

@app.route('/api/v1/orders', methods=['GET'])
def get_orders(): 
    filtered = ORDERS.copy()
    
    if status := request.args.get('status'):
        filtered = [o for o in filtered if o['status'] == status]
    if customer_id := request.args.get('customer_id'):
        try:
            filtered = [o for o in filtered if o['customer_id'] == int(customer_id)]
        except ValueError:
            raise ApiProblem(400, "Invalid Parameter", "customer_id phải là số", "invalid-param")

    filtered.sort(key=lambda x: x['id'])

    limit = int(request.args.get('limit', 2)) # Mặc định lấy 2 bản ghi
    start_idx = 0
    if cursor_str := request.args.get('cursor'):
        try:
            cursor_data = json.loads(base64.b64decode(cursor_str).decode('utf-8'))
            last_id = cursor_data.get('last_id', 0)
            start_idx = next((i for i, o in enumerate(filtered) if o['id'] > last_id), len(filtered))
        except Exception:
            raise ApiProblem(400, "Invalid Cursor", "Cursor không hợp lệ.", "invalid-cursor")

    paginated = filtered[start_idx : start_idx + limit]

    if fields_str := request.args.get('fields'):
        fields = set(fields_str.split(','))
        results = [{k: v for k, v in o.items() if k in fields} for o in paginated]
    else:
        results = paginated

    next_cursor = None
    if start_idx + limit < len(filtered):
        next_cursor = base64.b64encode(json.dumps({"last_id": paginated[-1]['id']}).encode('utf-8')).decode('utf-8')

    return jsonify({
        "data": results, 
        "next_cursor": next_cursor
    }), 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)