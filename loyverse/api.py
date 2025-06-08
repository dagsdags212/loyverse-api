import os
from datetime import datetime
from dotenv import load_dotenv
import httpx
from loguru import logger


class LoyverseEndpoint:
    base_url = "https://api.loyverse.com/v1.0"

    def __init__(self, endpoint: str, params: dict[str, any] = {"limit": 250}):
        load_dotenv()
        self.__api_key = os.getenv("LOYVERSE_API_KEY")
        self.headers = {"Authorization": f"Bearer {self.__api_key}"}
        self.params = params
        self.endpoint = endpoint

    @property
    def url(self) -> str:
        """Return endpoint URL"""
        return f"{self.base_url}/{self.endpoint}"

    def from_id(self, id: str) -> dict[str, any]:
        """Retrieve a single item from the endpoint"""
        response = httpx.get(f"{self.url}/{id}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def from_ids(self, *ids: str) -> list[dict[str, any]]:
        """Retrieve multiple items from the endpoint"""
        if len(ids) == 0:
            logger.info("No IDs provided")
            return []
        elif len(ids) == 1:
            ids = ids[0]
        else:
            ids = ",".join(ids)

        response = httpx.get(f"{self.url}?customer_ids={ids}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get(self) -> dict[str, any]:
        """Performs a GET request to the endpoint and returns all associated data"""
        data = []
        response = httpx.get(self.url, headers=self.headers, params=self.params)
        response.raise_for_status()

        data.extend(response.json().get(self.endpoint, []))

        cursor = response.json().get("cursor")
        while cursor:
            logger.info("Fetching next page...")
            self.params["cursor"] = cursor
            response = httpx.get(self.url, headers=self.headers, params=self.params)
            response.raise_for_status()
            data.extend(response.json().get(self.endpoint, []))
            cursor = response.json().get("cursor")

        # Reset cursor parameter
        if self.params.get("cursor"):
            del self.params["cursor"]

        return data

    def create(self, json: dict[str, any]) -> dict[str, any]:
        """Create a new item in the endpoint"""
        response = httpx.post(self.url, headers=self.headers, json=json)
        response.raise_for_status()
        return response.json()

    def update(self, id: str, json: dict[str, any]) -> dict[str, any]:
        """Update an existing item in the endpoint"""
        del json["id"]
        json.update({"id": id})
        print("PAYLOAD:", json)
        response = httpx.post(self.url, headers=self.headers, json=json)
        response.raise_for_status()
        return response.json()

    def delete(self, id: str) -> dict[str, any]:
        """Delete an existing item from the endpoint"""
        response = httpx.delete(f"{self.url}/{id}", headers=self.headers)
        response.raise_for_status()
        return response.json()


class CustomersEndpoint(LoyverseEndpoint):
    """
    Implements data fetching methods specific for the /customers endpoint.
    """

    def __init__(self):
        super().__init__("customers")

    def from_email(self, email: str) -> dict[str, any]:
        """Retrieve a customer from the endpoint by email"""
        response = httpx.get(f"{self.url}?email={email}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def created_at_min(self, date: datetime) -> dict[str, any]:
        """Retrieve customers created on or after the given date"""
        date_str = date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        response = httpx.get(
            f"{self.url}?created_at_min={date_str}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def created_at_max(self, date: datetime) -> dict[str, any]:
        """Retrieve customers created on or before the given date"""
        date_str = date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        response = httpx.get(
            f"{self.url}?created_at_max={date_str}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def created_within(self, start: datetime, end: datetime) -> dict[str, any]:
        """Retrieve customers created within the given date range"""
        start_str = start.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_str = end.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        response = httpx.get(
            f"{self.url}?created_at_min={start_str}&created_at_max={end_str}",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def updated_at_min(self, date: datetime) -> dict[str, any]:
        """Retrieve customers updated on or after the given date"""
        date_str = date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        response = httpx.get(
            f"{self.url}?updated_at_min={date_str}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def updated_at_max(self, date: datetime) -> dict[str, any]:
        """Retrieve customers updated on or before the given date"""
        date_str = date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        response = httpx.get(
            f"{self.url}?updated_at_max={date_str}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def updated_within(self, start: datetime, end: datetime) -> dict[str, any]:
        """Retrieve customers updated within the given date range"""
        start_str = start.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_str = end.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        response = httpx.get(
            f"{self.url}?updated_at_min={start_str}&updated_at_max={end_str}",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()


class ReceiptsEndpoint(LoyverseEndpoint):
    """
    Implements data fetching methods specific for the /receipts endpoint.
    """

    def __init__(self):
        super().__init__("receipts")

    def from_receipt_number(self, receipt_number: str) -> dict[str, any]:
        """Retrieve the receipt information for the given receipt number"""
        response = httpx.get(
            f"{self.url}?receipt_number={receipt_number}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def from_receipt_numbers(self, *receipt_numbers: str) -> dict[str, any]:
        """Retrieve the receipt information for the given receipt numbers"""
        if len(receipt_numbers) == 0:
            logger.info("No receipt numbers provided")
            return []
        elif len(receipt_numbers) == 1:
            receipt_numbers = receipt_numbers[0]
        else:
            receipt_numbers = ",".join(receipt_numbers)

        response = httpx.get(
            f"{self.url}?receipt_numbers={receipt_numbers}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def after_receipt_number(self, receipt_number: str) -> dict[str, any]:
        """Retrieve the receipt information following the given receipt number"""
        response = httpx.get(
            f"{self.url}?since_receipt_number={receipt_number}&limit=1",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def before_receipt_number(self, receipt_number: str) -> dict[str, any]:
        """Retrieve the receipt information preceding the given receipt number"""
        response = httpx.get(
            f"{self.url}?before_receipt_number={receipt_number}&limit=1",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()


class Loyverse:
    categories = LoyverseEndpoint("categories")
    customers = CustomersEndpoint()
    discounts = LoyverseEndpoint("discounts")
    employees = LoyverseEndpoint("employees")
    inventory = LoyverseEndpoint("inventory")
    items = LoyverseEndpoint("items")
    modifiers = LoyverseEndpoint("modifiers")
    payment_types = LoyverseEndpoint("payment_types")
    pos_devices = LoyverseEndpoint("pos_devices")
    receipts = ReceiptsEndpoint()
    shifts = LoyverseEndpoint("shifts")
    stores = LoyverseEndpoint("stores")
    suppliers = LoyverseEndpoint("suppliers")
    taxes = LoyverseEndpoint("taxes")
    webhooks = LoyverseEndpoint("webhooks")
    variants = LoyverseEndpoint("variants")
