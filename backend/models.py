from pydantic import BaseModel
from typing import Optional

class SOPBase(BaseModel):
    department: Optional[str] = None
    process_name: str
    objective: Optional[str] = None
    scope: Optional[str] = None
    roles: Optional[str] = None
    prerequisites: Optional[str] = None
    steps: Optional[str] = None
    kpis: Optional[str] = None
    risk_factors: Optional[str] = None
    tools_required: Optional[str] = None
    review_frequency: Optional[str] = None

class SOPCreate(SOPBase):
    pass

class SOPUpdate(BaseModel):
    department: Optional[str] = None
    process_name: Optional[str] = None
    objective: Optional[str] = None
    scope: Optional[str] = None
    roles: Optional[str] = None
    prerequisites: Optional[str] = None
    steps: Optional[str] = None
    kpis: Optional[str] = None
    risk_factors: Optional[str] = None
    tools_required: Optional[str] = None
    review_frequency: Optional[str] = None

class SOPResponse(SOPBase):
    id: int
    created_at: str
    class Config:
        from_attributes = True

class GenerateRequest(BaseModel):
    process_name: str
