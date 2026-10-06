import uuid
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

class ApiProblem(Exception):
    def __init__(self, status, title, detail=None, type_path=None, **extra):
        self.status = status
        self.title = title
        self.detail = detail
        self.type = f"https://api.example.com/probs/{type_path}" if type_path else "about:blank"
        self.extra = extra

@app.errorhandler(ApiProblem)
def handle_api_problem(e):
    body = {
        "type": e.type, 
        "title": e.title, 
        "status": e.status,
        "instance": request.path, 
        "trace_id": str(uuid.uuid4())
    }
    if e.detail: 
        body["detail"] = e.detail
    body.update(e.extra)
    
    resp = jsonify(body)
    resp.status_code = e.status
    resp.headers["Content-Type"] = "application/problem+json"
    return resp

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return handle_api_problem(ApiProblem(e.code, e.name, e.description, "http-error"))

@app.route('/api/v1/users/<int:id>', methods=['GET'])
def get_user(id):
    raise ApiProblem(
        status=404, 
        title="User not found", 
        detail=f"Không tìm thấy người dùng có ID {id} trong hệ thống.", 
        type_path="user-not-found", 
        resource_id=id
    )

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)