from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
from pydantic import field_validator
from pydantic import EmailStr, NonNegativeInt, NonNegativeFloat
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlmodel import Relationship, JSON
from loyverse.api import Loyverse


class Employee(SQLModel, table=True):
    __tablename__ = 'employees'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    email: Optional[EmailStr]
    phone_number: Optional[str]
    stores: str
    is_owner: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    @field_validator('stores', mode='before')
    @classmethod
    def flatten_store_ids(cls, id_list: list[str]) -> str:
        return id_list[0]


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
    receipts: List["Receipt"] = Relationship(back_populates="customer")

class Variant(SQLModel, table=True):
    __tablename__ = 'variants'

    variant_id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_id: Optional[UUID]
    sku: Optional[str]
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

class Item(SQLModel, table=True):
    __tablename__ = 'items'

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
    primary_supplier_id: Optional[UUID]
    tax_ids: Optional[str]
    modifier_ids: Optional[str]
    form: Optional[str]
    color: Optional[str]
    image_url: Optional[str]
    option1_name: Optional[str]
    option2_name: Optional[str]
    option3_name: Optional[str]
    variants: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    @field_validator("tax_ids", 'modifier_ids', mode='before')
    @classmethod
    def concat_id_list(cls, value) -> str:
        if value:
            return ','.join(value)

    @field_validator('variants', mode='before')
    @classmethod
    def extract_variant_ids(cls, variants: list[dict[str, any]]) -> str:
        return ','.join(map(lambda x: x.get('variant_id'), variants))


class Receipt(SQLModel, table=True):
    __tablename__ = 'receipts'
    
    receipt_number: str = Field(primary_key=True)
    note: Optional[str]
    receipt_type: str
    refund_for: Optional[str]
    order: Optional[str]
    created_at: datetime
    updated_at: datetime
    cancelled_at: Optional[datetime]
    source: Optional[str]
    total_money: NonNegativeFloat
    total_tax: Optional[NonNegativeFloat]
    total_discount: NonNegativeFloat = 0.0
    points_earned: Optional[NonNegativeFloat]
    points_deducted: Optional[NonNegativeFloat] = 0.0
    points_balance: Optional[NonNegativeFloat]
    customer_id: Optional[UUID] = Field(foreign_key='customers.id')
    employee_id: Optional[UUID] = Field(foreign_key='employees.id')
    store_id: Optional[UUID] # Foreign key 
    pos_device_id: Optional[UUID] # Foreign key
    tip: Optional[NonNegativeFloat] = 0.0
    surcharge: Optional[NonNegativeFloat]
    line_items: List[str] = Field(default_factory=list, sa_type=JSON)
    payments: str
    customer: Optional[Customer] = Relationship(back_populates='receipts')

    @field_validator('payments', mode='before')
    @classmethod
    def extract_payment_name(cls, value) -> str:
        return value[0].get('name')

    @field_validator('line_items', mode='before')
    @classmethod
    def extract_item_ids(cls, value) -> list[str]:
        ids = map(lambda x: x.get('item_id'), value)
        return list(ids)
        


class DatabaseSeeder:
    @classmethod
    def employees(cls, engine):
        data = Loyverse.employees.get()
        employees = [Employee.model_validate(d) for d in data]
        with Session(engine) as session:
            for e in employees:
                session.add(e)
            session.commit()

    @classmethod
    def customers(cls, engine):
        data = Loyverse.customers.get()
        customers = [Customer.model_validate(d) for d in data]
        with Session(engine) as session:
            for c in customers:
                session.add(c)
            session.commit()

    @classmethod
    def variants(cls, engine):
        data = Loyverse.variants.get()
        variants = [Variant.model_validate(d) for d in data]
        with Session(engine) as session:
            for v in variants:
                session.add(v)
            session.commit()

    @classmethod
    def items(cls, engine):
        data = Loyverse.items.get()
        items = [Item.model_validate(d) for d in data]
        with Session(engine) as session:
            for v in items:
                session.add(v)
            session.commit()

    @classmethod
    def receipts(cls, engine):
        data = Loyverse.receipts.get()
        receipts = [Receipt.model_validate(r) for r in data]
        with Session(engine) as session:
            for r in receipts:
                session.add(r)
            session.commit()

def seed_db(db_name) -> None:
    if db_name:
        db_url = f"duckdb:///{db_name}"
    else:
        db_url = 'duckdb:///:memory:'
    engine = create_engine(db_url, echo=True)

    SQLModel.metadata.create_all(engine)

    DatabaseSeeder.employees(engine)
    DatabaseSeeder.customers(engine)
    DatabaseSeeder.variants(engine)
    DatabaseSeeder.items(engine)
    DatabaseSeeder.receipts(engine)

if __name__ == "__main__":
    seed_db('loyverse.db')
