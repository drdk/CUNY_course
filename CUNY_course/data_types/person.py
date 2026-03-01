from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


class RelationshipStatus(Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    IN_A_RELATIONSHIP = "in_a_relationship"
    ITS_COMPLICATED = "its_complicated"


class Address(BaseModel):
    street: str
    house_number: int
    floor: Optional[int]
    city: str
    zip_code: int


class Person(BaseModel):
    name: str
    age: int
    height_cm: float
    weight_kg: float
    is_employed: bool
    address: Address
    relationship_status: RelationshipStatus


class RelationshipStatus2(Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    IN_A_RELATIONSHIP = "in_a_relationship"
    ITS_COMPLICATED = "its_complicated"
    UNKNOWN = "unknown"


class Address2(BaseModel):
    street: Optional[str]
    house_number: Optional[int]
    floor: Optional[int]
    city: Optional[str]
    zip_code: Optional[int]


class Person2(BaseModel):
    name: Optional[str]
    age: Optional[int]
    height_cm: Optional[float]
    weight_kg: Optional[float]
    is_employed: Optional[bool]
    address: Optional[Address2]
    relationship_status: RelationshipStatus2


class BasePerson(BaseModel):
    name: Optional[str]
    age: Optional[int]
    height_cm: Optional[float]
    weight_kg: Optional[float]
    is_employed: Optional[bool]
    address: Optional[Address2]


class RelationshipType(Enum):
    MARRIAGE = "marriage"
    PARTNERSHIP = "partnership"
    DATING = "dating"
    AFFAIR = "affair"
    ITS_COMPLICATED = "its_complicated"
    OTHER = "other"


class TerminationReason(Enum):
    DECEASED = "deceased"
    DIVORCE = "divorce"
    OTHER = "other"
    UNKNOWN = "unknown"


class Relationship(BaseModel):
    person: BasePerson
    active: bool
    relationship_type: RelationshipType
    duration_years: Optional[int]
    termination_reason: Optional[TerminationReason]


class PersonWithRelationships(BasePerson):
    current_relationships: List[Relationship]
    past_relationship_history: List[Relationship]
