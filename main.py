from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field
from fastmcp import FastMCP

# Initialize MCP server
app = FastMCP("health-assistant-mcp")

# Models
class ClaimStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    PAID = "PAID"

class ClaimDetails(BaseModel):
    claim_number: str = Field(..., description="Unique identifier for the claim")
    status: ClaimStatus = Field(..., description="Current status of the claim")
    date_of_service: str = Field(..., description="Date when the service was provided")
    provider_name: str = Field(..., description="Name of the healthcare provider")
    total_amount: float = Field(..., description="Total claim amount")
    amount_covered: float = Field(..., description="Amount covered by insurance")
    patient_responsibility: float = Field(..., description="Amount to be paid by patient")
    service_description: str = Field(..., description="Description of the service provided")

class PlanBenefit(BaseModel):
    service: str = Field(..., description="Name of the medical service")
    coverage: str = Field(..., description="Coverage details (e.g., '100% after deductible')")
    limitations: Optional[str] = Field(None, description="Any limitations or restrictions")

class ProviderDetails(BaseModel):
    name: str = Field(..., description="Provider's full name")
    specialty: str = Field(..., description="Medical specialty")
    address: str = Field(..., description="Practice address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    zip_code: str = Field(..., description="ZIP code")
    phone: str = Field(..., description="Contact phone number")
    accepting_new_patients: bool = Field(..., description="Whether the provider is accepting new patients")
    languages: List[str] = Field(..., description="Languages spoken by the provider")

# Mock data
MOCK_CLAIMS = {
    "CLM123456": {
        "status": ClaimStatus.APPROVED,
        "date_of_service": "2023-10-15",
        "provider_name": "Dr. Sarah Johnson",
        "total_amount": 1200.00,
        "amount_covered": 1000.00,
        "patient_responsibility": 200.00,
        "service_description": "Annual physical examination"
    },
    "CLM789012": {
        "status": ClaimStatus.PENDING,
        "date_of_service": "2023-11-01",
        "provider_name": "City Medical Center",
        "total_amount": 2500.00,
        "amount_covered": 2000.00,
        "patient_responsibility": 500.00,
        "service_description": "MRI Scan"
    }
}

MOCK_PLAN_BENEFITS = {
    "PLAN001": [
        {"service": "Primary Care Visit", "coverage": "$30 copay", "limitations": "Up to 4 visits per year"},
        {"service": "Specialist Visit", "coverage": "$50 copay", "limitations": "Requires referral"},
        {"service": "Emergency Room", "coverage": "$300 copay", "limitations": "After deductible"},
        {"service": "Prescription Drugs", "coverage": "Tier 1: $10, Tier 2: $30, Tier 3: $50", "limitations": "30-day supply"}
    ],
    "PLAN002": [
        {"service": "Primary Care Visit", "coverage": "$20 copay", "limitations": "Up to 6 visits per year"},
        {"service": "Specialist Visit", "coverage": "$40 copay", "limitations": "No referral needed"},
        {"service": "Emergency Room", "coverage": "$250 copay", "limitations": "After deductible"},
        {"service": "Prescription Drugs", "coverage": "Tier 1: $5, Tier 2: $25, Tier 3: $45", "limitations": "90-day supply available"}
    ]
}

MOCK_PROVIDERS = [
    {
        "name": "Dr. Sarah Johnson",
        "specialty": "Family Medicine",
        "address": "123 Health St, Suite 100",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "phone": "(212) 555-0101",
        "accepting_new_patients": True,
        "languages": ["English", "Spanish"]
    },
    {
        "name": "Dr. Michael Chen",
        "specialty": "Cardiology",
        "address": "456 Heart Ave",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "phone": "(212) 555-0202",
        "accepting_new_patients": False,
        "languages": ["English", "Mandarin"]
    },
    {
        "name": "Dr. Emily Wilson",
        "specialty": "Pediatrics",
        "address": "789 Child St",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02108",
        "phone": "(617) 555-0303",
        "accepting_new_patients": True,
        "languages": ["English", "French"]
    }
]

# MCP Tools
@app.tool(name="get_claim_details")
async def get_claim_details(claim_number: str) -> ClaimDetails:
    """
    Retrieve claim status and details by claim number
    
    Args:
        claim_number: The unique identifier for the insurance claim
        
    Returns:
        ClaimDetails: Detailed information about the claim including status, amounts, and service description
    """
    if claim_number not in MOCK_CLAIMS:
        raise ValueError(f"Claim with number {claim_number} not found")
    
    return ClaimDetails(claim_number=claim_number, **MOCK_CLAIMS[claim_number])

@app.tool(name="get_plan_benefits")
async def get_plan_benefits(plan_id: str) -> List[PlanBenefit]:
    """
    Retrieve benefits and coverage details for a specific health insurance plan
    
    Args:
        plan_id: The unique identifier for the insurance plan
        
    Returns:
        List[PlanBenefit]: A list of benefits and coverage details for the specified plan
    """
    if plan_id not in MOCK_PLAN_BENEFITS:
        raise ValueError(f"Plan with ID {plan_id} not found")
    
    return [PlanBenefit(**benefit) for benefit in MOCK_PLAN_BENEFITS[plan_id]]

@app.tool(name="get_health_provider_details")
async def get_health_provider_details(
    provider_name: str = "", 
    zip_code: str = ""
) -> List[ProviderDetails]:
    """
    Search for healthcare providers by name and/or zip code
    
    Args:
        provider_name: Full or partial name of the healthcare provider (optional)
        zip_code: ZIP code to search within (optional)
        
    Returns:
        List[ProviderDetails]: A list of matching healthcare providers with their details
    """
    results = MOCK_PROVIDERS
    
    if provider_name:
        provider_name = provider_name.lower()
        results = [p for p in results if provider_name in p["name"].lower()]
    
    if zip_code:
        results = [p for p in results if p["zip_code"] == zip_code]
    
    return [ProviderDetails(**provider) for provider in results]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
