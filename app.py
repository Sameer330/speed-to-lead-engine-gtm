from fastapi import FastAPI
from models import InboundLead, EnrichedCompanyProfile
from crawler import crawl_company
from qualifier import evaluate_lead
from notifier import format_slack_dossier, send_slack_alert

app = FastAPI(title="Anthropic Enterprise Speed-to-Lead Engine", version="1.0.0")

@app.get('/health')
async def get_health():
    return {'status': 'healthy', 'service': 'speed-to-lead-engine'}

@app.post('/webhook/inbound-lead')
async def webhook_inhound_lead(lead: InboundLead):
    if not lead.is_business_email:
        profile = EnrichedCompanyProfile(domain="", crawl_status="personal_email")
    else:
        profile = await crawl_company(lead.extracted_domain)

    evaluation = evaluate_lead(lead=lead, profile=profile)
    
    slack_card = format_slack_dossier(lead=lead, profile=profile, evaluation=evaluation)

    if evaluation.tier in ['Tier A', 'Tier B']:
        await send_slack_alert(slack_card)

    return {
        'status': 'processed',
        'lead': lead.model_dump(),
        'evaluation': evaluation.model_dump(),
        'profile': profile.model_dump(),
        'slack_card': slack_card,
    }