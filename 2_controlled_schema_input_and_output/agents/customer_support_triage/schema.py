from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

# --- Enums for strict control ---

class CustomerTier(str, Enum):
    FREE = "Free"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"

class PriorityLevel(str, Enum):
    P0 = "P0"  # Critical/Immediate
    P1 = "P1"  # High Priority
    P2 = "P2"  # Normal/Routine

class TicketCategory(str, Enum):
    BILLING = "Billing"
    TECHNICAL = "Technical"
    FEATURE_REQUEST = "Feature_Request"
    ACCOUNT_ACCESS = "Account_Access"
    OTHER = "Other"

# --- Input Schemas ---

class SupportTicketInput(BaseModel):
    """
    The structure for the incoming raw support ticket data.
    """
    raw_ticket_text: str = Field(
        ..., 
        description="The full, unstructured text of the customer's support request."
    )
    customer_tier: CustomerTier = Field(
        ..., 
        description="The subscription level of the customer, used to help determine priority."
    )
    timestamp: str = Field(
        ..., 
        description="The ISO 8601 timestamp of when the ticket was submitted."
    )

# --- Output Schemas ---

class SupportTriageOutput(BaseModel):
    """
    The structured analysis performed by the Agent.
    """
    priority_level: PriorityLevel = Field(
        ..., 
        description="The calculated priority. Enterprise customers or technical blockers should usually be P0/P1."
    )
    detected_sentiment: str = Field(
        ..., 
        description="A brief description of the user's emotional state (e.g., 'Frustrated', 'Neutral', 'Urgent')."
    )
    category: TicketCategory = Field(
        ..., 
        description="The primary department or functional area this ticket belongs to."
    )
    summary_sentence: str = Field(
        ..., 
        description="A concise, one-sentence summary of the core issue for quick reading by agents."
    )
    requires_manager_intervention: bool = Field(
        default=False,
        description="Set to true if the sentiment is extremely negative or the issue is a legal threat."
    )