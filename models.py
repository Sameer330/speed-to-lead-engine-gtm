from pydantic import BaseModel
from typing import Optional

FREE_PROVIDERS = {'gmail.com', 'yahoo.com', 'outlook.com', 'zohomail.com', 'hotmail.com', 'icloud.com'}

class InboundLead(BaseModel):
    first_name: str
    last_name: str
    email: str
    company_name: str
    company_domain: Optional[str] = None
    use_case: Optional[str] = None
    company_size: Optional[str] = None

    @property
    def extracted_domain(self) -> str | None:
        if self.company_domain:
            return self.company_domain.replace('https://', '').replace('http://', '').replace('www.', '').strip('/')

        if '@' in self.email:
            domain = self.email.split('@')[-1].lower().strip()
            if domain not in FREE_PROVIDERS:
                return domain
        
        return None

    @property
    def is_business_email(self) -> bool:
        if '@' in self.email:
            domain = self.email.split('@')[-1].lower().strip()
            return domain not in FREE_PROVIDERS and domain != ""
        return False
    
class EnrichedCompanyProfile(BaseModel):
    domain: str
    title: Optional[str] = None
    meta_description: Optional[str] = None
    h1_tags: list[str] = []
    crawl_status: str

class LeadEvaluation(BaseModel):
    tier: str
    confidence: str
    company_summary: str
    pain_point: str
    suggested_action: str

