def test_create_product(client):
    payload = {"sku": "TEST-123", "name": "Bút bi", "price_cents": 5000, "qty_in_stock": 100}
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 201
    assert response.json["sku"] == "TEST-123"

def test_list_orders_eager_loading(client):
    response = client.get("/api/v1/orders")
    assert response.status_code == 200