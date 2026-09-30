from flask import Flask, jsonify, request

app = Flask(__name__)

POSTS = []
_next_post_id = 1

@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    return jsonify({
        "data": POSTS,
        "total": len(POSTS)
    }), 200

@app.route('/api/v1/posts', methods=['POST'])
def create_post():
    global _next_post_id
    if not request.is_json:
        return jsonify({"error": "Định dạng phải là JSON"}), 415       
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    if not title or not content:
        return jsonify({"error": "Tiêu đề và nội dung là bắt buộc"}), 422      
    new_post = {
        "id": _next_post_id,
        "title": title,
        "content": content,
        "author_id": data.get("author_id")
    }  
    POSTS.append(new_post)
    _next_post_id += 1
    return jsonify(new_post), 201

@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_single_post(post_id):
    """Lấy chi tiết một bài viết cụ thể (Item)"""
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": "Không tìm thấy bài viết"}), 404
    return jsonify(post), 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)