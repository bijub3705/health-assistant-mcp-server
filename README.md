# Health Assistant MCP Server

A Model Context Protocol (MCP) server for health insurance-related functionality, including claim details, plan benefits, and healthcare provider information.

## Features

1. **Claim Management**
   - Retrieve claim status and details by claim number

2. **Plan Benefits**
   - View coverage details for specific health insurance plans
   - Understand service limitations and copay information

3. **Provider Search**
   - Find healthcare providers by name and location
   - View provider specialties, contact information, and availability

## Getting Started

### Prerequisites

- Python 3.11+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd health-assistant-mcp-server
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # Or on Unix/macOS:
   # source .venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

- fastmcp==2.13.0.2
- mcp==1.20.0
- pydantic==2.12.3

### Running the Server

Start the MCP server with the following command:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000` by default.

### Development

For development with auto-reload:

```bash
uvicorn main:app --reload
```

## API Documentation

Once the server is running, you can access the following endpoints:

### 1. Get Claim Details

**Tool Name:** `get_claim_details`

Retrieve detailed information about a specific insurance claim.

**Parameters:**
- `claim_number` (string, required): The unique identifier for the claim

**Example Response:**
```json
{
  "claim_number": "CLM123456",
  "status": "APPROVED",
  "date_of_service": "2023-10-15",
  "provider_name": "Dr. Sarah Johnson",
  "total_amount": 1200.0,
  "amount_covered": 1000.0,
  "patient_responsibility": 200.0,
  "service_description": "Annual physical examination"
}
```

### 2. Get Plan Benefits

**Tool Name:** `get_plan_benefits`

Retrieve the benefits and coverage details for a specific health insurance plan.

**Parameters:**
- `plan_id` (string, required): The unique identifier for the insurance plan

**Example Response:**
```json
[
  {
    "service": "Primary Care Visit",
    "coverage": "$30 copay",
    "limitations": "Up to 4 visits per year"
  },
  {
    "service": "Specialist Visit",
    "coverage": "$50 copay",
    "limitations": "Requires referral"
  }
]
```

### 3. Get Health Provider Details

**Tool Name:** `get_health_provider_details`

Search for healthcare providers by name and/or location.

**Parameters:**
- `provider_name` (string, optional): Full or partial name of the provider
- `zip_code` (string, optional): ZIP code to search within

**Example Response:**
```json
[
  {
    "name": "Dr. Sarah Johnson",
    "specialty": "Family Medicine",
    "address": "123 Health St, Suite 100",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "phone": "(212) 555-0101",
    "accepting_new_patients": true,
    "languages": ["English", "Spanish"]
  }
]
```

## Mock Data

The server comes with pre-populated mock data for demonstration purposes. The following data is available:

- **Claims:** CLM123456, CLM789012
- **Plans:** PLAN001, PLAN002
- **Providers:** Dr. Sarah Johnson, Dr. Michael Chen, Dr. Emily Wilson

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
