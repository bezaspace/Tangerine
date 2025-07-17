from pydantic import BaseModel
from typing import List, Optional

class Practitioner(BaseModel):
    id: int
    name: str
    specialty: str
    rating: float
    experience: str
    location: str
    nextAvailable: str
    image: str

class PractitionerResponse(BaseModel):
    practitioners: List[Practitioner]
    total: int

class PractitionerDetail(Practitioner):
    description: Optional[str] = None
    qualifications: Optional[List[str]] = None
    languages: Optional[List[str]] = None

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    originalPrice: Optional[float] = None
    rating: float
    reviews: int
    image: str
    category: str
    inStock: bool

class ProductResponse(BaseModel):
    products: List[Product]
    total: int

class ProductCategory(BaseModel):
    name: str
    count: int