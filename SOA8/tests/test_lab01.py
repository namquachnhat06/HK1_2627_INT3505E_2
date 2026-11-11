"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""
def test_list_books_empty(client):
    r = client.get("/books")
    assert r.status_code == 200
    assert r.content_type == "application/json"
    assert r.get_json() == []  

def test_get_book_not_found(client):
    r = client.get("/books/9999")
    assert r.status_code == 404
    body = r.get_json()
    assert body.get("code") == "NOT_FOUND"

def test_post_missing_title(client):
    r = client.post("/books", json={"author": "Kleppmann"})
    assert r.status_code == 400
    body = r.get_json()
    fields = {e.get("field") for e in body.get("errors", [])}
    assert "title" in fields 

def test_delete_then_get_404(client):
    # Tạo nhanh 1 cuốn sách để lấy ID
    res = client.post("/books", json={"title": "Test Delete", "author": "Author"})
    bid = res.get_json()["id"]

    del_res = client.delete(f"/books/{bid}")
    assert del_res.status_code == 204

    get_res = client.get(f"/books/{bid}")
    assert get_res.status_code == 404

def test_response_extra_field_blocked(client):
    import pytest
    from jsonschema import validate, ValidationError
    from tools import get_book_schema

    res = client.post("/books", json={
        "title": "API Design", 
        "author": "Geewax", 
        "year": 2021, 
        "isbn": "9781617295850"
    })
    bid = res.get_json()["id"]

    book_data = client.get(f"/books/{bid}").get_json()
    book_copy = book_data.copy()
    
    book_copy["unknown_field"] = "hack"

    schema = get_book_schema()
    with pytest.raises(ValidationError):
        validate(book_copy, schema)