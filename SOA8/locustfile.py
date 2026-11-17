import time
from locust import HttpUser, task, between, events
import random

class BooksUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def get_books(self):
        self.client.get("/books")

    @task(2)
    def create_book(self):
        self.client.post("/books", json={
            "title": f"Book Test {random.randint(1, 10000)}",
            "author": "Nam Quach"
        })

    @task(1)
    def search_by_year(self):
        # Giả lập thêm tham số year và tạo 1% fail rate (mã lỗi 500)
        year = random.randint(2010, 2026)
        response = self.client.get(f"/books?year={year}")

        if random.random() < 0.01:
            pass