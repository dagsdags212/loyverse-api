from datetime import datetime, timezone
from typing import Optional, List, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, field_validator
from pydantic import EmailStr, NonNegativeInt, NonNegativeFloat, JsonValue
from src.api import Loyverse


class Base(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class Employee(Base):
    name: str
    email: Optional[EmailStr]
    phone_number: Optional[str]
    stores: Optional[List[UUID]]
    is_owner: bool


class Customer(Base):
    name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    address: Optional[str]
    city: Optional[str] = "Los Banos"
    region: Optional[str] = "Laguna"
    postal_code: Optional[str] = "4031"
    country_code: Optional[str] = "PHL"
    note: Optional[str]
    customer_code: Optional[str]
    first_visit: datetime
    last_visit: datetime
    total_visits: NonNegativeInt = 0
    total_spent: NonNegativeFloat = 0.0
    total_points: NonNegativeFloat = 0.0
    permanent_deletion_at: Optional[datetime]


class Variant(BaseModel):
    variant_id: UUID = Field(default_factory=uuid4)
    item_id: UUID
    sku: str
    reference_variant_id: Optional[UUID]
    option1_value: Optional[str]
    option2_value: Optional[str]
    option3_value: Optional[str]
    barcode: Optional[str]
    cost: Optional[NonNegativeFloat]
    purchase_cost: Optional[NonNegativeFloat]
    default_pricing_type: str
    default_price: Optional[NonNegativeFloat]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class Item(Base):
    handle: str
    reference_id: Optional[UUID]
    item_name: str
    description: Optional[str]
    track_stock: bool
    sold_by_weight: bool
    is_composite: bool
    use_production: bool
    category_id: Optional[UUID]
    components: List[Any]
    primary_supplier_id: Optional[UUID]
    tax_ids: Optional[List[UUID]]
    modifier_ids: Optional[List[UUID]]
    form: Optional[str]
    color: Optional[str]
    image_url: Optional[str]
    option1_name: Optional[str]
    option2_name: Optional[str]
    option3_name: Optional[str]
    variants: List[Variant]


class Receipt(BaseModel):
    receipt_number: Optional[str]
    note: Optional[str]
    receipt_type: Optional[str]
    refund_for: Optional[str]
    order: Optional[str]
    created_at: datetime
    updated_at: datetime
    source: Optional[str]
    cancelled_at: Optional[datetime]
    total_money: NonNegativeFloat
    total_tax: Optional[NonNegativeFloat]
    points_earned: Optional[NonNegativeFloat]
    points_deducted: Optional[NonNegativeFloat] = 0.0
    points_balance: Optional[NonNegativeFloat]
    customer_id: Optional[UUID]
    total_discount: Optional[List[NonNegativeFloat]]
    employee_id: Optional[UUID]
    store_id: Optional[UUID]
    pos_device_id: Optional[UUID]
    total_discount: Optional[List[NonNegativeFloat]] | Optional[NonNegativeFloat]
    total_taxes: Optional[List[NonNegativeFloat]]
    tip: Optional[NonNegativeFloat] = 0.0
    surcharge: Optional[NonNegativeFloat]
    line_items: List[JsonValue]
    payments: List[JsonValue]

    @field_validator("created_at", "updated_at", mode="after")
    @classmethod
    def validate_datetimes(cls, dt: datetime):
        # Prevent input of dates preceeding store opening
        opening = datetime(2025, 1, 15, tzinfo=timezone.utc)
        if (dt - opening).days < 0:
            raise ValueError("date of receipt creation cannot preceed 2025-01-15")

        # Prevent input of future dates
        if (datetime.now(timezone.utc) - dt).days <= 0:
            raise ValueError("receipts cannot be created in the future")

        return dt
