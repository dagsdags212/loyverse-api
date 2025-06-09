from datetime import datetime, timezone
from typing import Optional, List, Any, Literal
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, field_validator
from pydantic import EmailStr, NonNegativeInt, NonNegativeFloat, JsonValue


class Base(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class Employee(SQLModel, table=True):
    __tablename__ = "employees"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    email: Optional[EmailStr]
    phone_number: Optional[str]
    stores: Optional[str]
    is_owner: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    @field_validator("stores", mode="before")
    @classmethod
    def join_store_ids(cls, values: list[str]) -> str:
        """Concatenates stored ids using a comma delimiter"""
        return ",".join(values)


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
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


class Variant(SQLModel, table=True):
    __tablename__ = "variants"

    variant_id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_id: UUID
    sku: str
    reference_variant_id: Optional[UUID] = Field(foreign_key="Variant.variant_id")
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


class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
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
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


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


class PaymentType(Base):
    name: str
    type: str
    stores: Optional[List[UUID]]


class PosDevice(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    stored_id: Optional[UUID]
    activated: bool
    deleted_at: Optional[datetime]


class Discount(Base):
    type: str
    name: str
    discount_amount: NonNegativeFloat
    discount_percent: NonNegativeFloat = Field(ge=0.0, le=100.0)
    stores: List[UUID]
    restricted_access: bool = Field(default=False)


class Category(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    color: str
    created_at: datetime
    deleted_at: Optional[datetime]


### Schema dependencies for `Merchant`


class Currency(BaseModel):
    code: str = Field(max_length=3, min_length=3)
    decimal_places: int = Field(default=2)


class Merchant(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    business_name: str
    email: Optional[EmailStr]
    country: str
    currency: Currency
    created_at: datetime


### Schema dependencies for `Shift`


class CashMovement(BaseModel):
    type: Literal["PAY_IN", "PAY_OUT"]
    money_amount: NonNegativeFloat
    comment: Optional[str]
    employee_id: UUID
    created_at: datetime


# class Payment:
#     payment_type_id: UUID
#     money_amount: NonNegativeFloat


class Shift(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    store_id: UUID
    pos_device_id: UUID
    opened_at: datetime
    closed_at: datetime
    opened_by_employee: UUID
    closed_by_employee: UUID
    starting_cash: Optional[NonNegativeFloat]
    cash_payments: NonNegativeFloat
    cash_refunds: NonNegativeFloat = 0.0
    paid_in: Optional[NonNegativeFloat]
    paid_out: Optional[NonNegativeFloat]
    expected_cash: NonNegativeFloat
    actual_cash: NonNegativeFloat
    gross_sales: NonNegativeFloat
    refunds: Optional[NonNegativeFloat]
    discounts: Optional[NonNegativeFloat]
    net_sales: Optional[NonNegativeFloat]
    tip: Optional[NonNegativeFloat] = 0.0
    surcharge: Optional[NonNegativeFloat] = 0.0
    # payments: List[Payment]
    cash_movements: List[CashMovement]
