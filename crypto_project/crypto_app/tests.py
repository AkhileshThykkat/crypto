import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv 
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings
from crypto_app.models import Organisation, CryptoPrice

load_dotenv()

class APITests(APITestCase):
    @classmethod
    def setUpClass(cls):
        """Ensure the test database is reset before running tests"""
        super().setUpClass()
        load_dotenv()

        db_url = os.getenv("DATABASE_URL", "postgres://user:password@localhost:5432/test_db")
        tmpPostgres = urlparse(db_url)
        connection = psycopg2.connect(
            dbname="postgres",
            user=tmpPostgres.username or "",
            password=tmpPostgres.password or "",
            host=tmpPostgres.hostname or "localhost",
            port=tmpPostgres.port or 5432,
            sslmode="require" if "neon.tech" in tmpPostgres.hostname else "disable",  
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(f"""
            SELECT pg_terminate_backend(pid) 
            FROM pg_stat_activity 
            WHERE datname = '{tmpPostgres.path.lstrip('/')}';
        """)

        cursor.execute(f"DROP DATABASE IF EXISTS {tmpPostgres.path.lstrip('/')};")
        cursor.execute(f"CREATE DATABASE {tmpPostgres.path.lstrip('/')} ENCODING 'UTF8';")

        cursor.close()
        connection.close()
    
    def setUp(self):
      """Create test users, log in, and get authentication token"""
      self.user1 = User.objects.create_user(username="user1", password="password1")
      self.user2 = User.objects.create_user(username="user2", password="password2")

      self.client.login(username="user1", password="password1")
      self.org1 = Organisation.objects.create(name="Crypto Corp", owner=self.user1)
      self.org2 = Organisation.objects.create(name="Blockchain Ltd", owner=self.user2)

      response = self.client.post("/api/token/", {"username": "user1", "password": "password1"})
      self.assertEqual(response.status_code, 200)
      self.token = response.data["access"]

      self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

      self.crypto1 = CryptoPrice.objects.create(org=self.org1, symbol="BTC", price="45000.12")
      self.crypto2 = CryptoPrice.objects.create(org=self.org1, symbol="ETH", price="3000.50")


    def test_create_organization(self):
        """Test creating an organization"""
        payload = {"name": "New Org"}
        response = self.client.post("/api/organizations/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_organizations(self):
        """Test getting list of organizations"""
        response = self.client.get("/api/organizations/")
        print(response.data) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only user1's org should be visible

    def test_get_organization_by_id(self):
        """Test retrieving a specific organization"""
        response = self.client.get(f"/api/organizations/{self.org1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Crypto Corp")

    def test_update_organization(self):
        """Test updating an organization"""
        response = self.client.put(f"/api/organizations/{self.org1.id}/", {"name": "Updated Crypto Corp"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Crypto Corp")

    def test_delete_organization(self):
        """Test deleting an organization"""
        response = self.client.delete(f"/api/organizations/{self.org1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_crypto_price(self):
        """Test creating a crypto price"""
        payload = {
            "symbol": "BTC",
            "price": "45000.12",
            "org": str(self.org1.id) 
        }
        response = self.client.post("/api/crypto-prices/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_crypto_prices(self):
        """Test retrieving all crypto prices"""
        response = self.client.get("/api/crypto-prices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Pagination returns 'results' key
    def test_get_crypto_price_by_id(self):
        """Test retrieving a specific crypto price"""
        response = self.client.get(f"/api/crypto-prices/{self.crypto1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["symbol"], "BTC")

    def test_update_crypto_price(self):
        """Test updating a crypto price"""
        response = self.client.put(f"/api/crypto-prices/{self.crypto1.id}/", {"symbol": "BTC", "price": "46000.99"})
        print(response.status_code, response.data)  # Check the error message
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], "46000.99")

    def test_delete_crypto_price(self):
        """Test deleting a crypto price"""
        response = self.client.delete(f"/api/crypto-prices/{self.crypto1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
