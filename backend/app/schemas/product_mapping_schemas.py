from pydantic import BaseModel
from typing import Optional

class ProductMappingBase(BaseModel):
    supplier_id: int
    supplier_product_id: int
    product_id: int

class ProductMappingCreate(ProductMappingBase):
    pass

class ProductMappingRead(ProductMappingBase):
    id: int

    class Config:
        orm_mode = True