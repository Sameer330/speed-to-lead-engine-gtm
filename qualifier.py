from models import InboundLead, EnrichedCompanyProfile, LeadEvaluation
from crawler import crawl_company
import subprocess
import json
import asyncio

def evaluate_lead(lead: InboundLead, profile: EnrichedCompanyProfile) -> LeadEvaluation:
    if not lead.is_business_email:
        return LeadEvaluation(
            tier="Disqualified",
            confidence="High",
            company_summary="Personal email address detected.",
            pain_point="Non-business email submission.",
            suggested_action="🚫 Disqualify: Archive without notifying sales"
        )
    
    try:
        with open('triage-prompt.txt', 'r', encoding='utf-8') as file:
            triage_prompt = file.read()
    except:
        print('Issue reading file `triage-prompt.txt`')
        return LeadEvaluation(
            tier='N/A',
            confidence='N/A',
            company_summary='N/A',
            pain_point='N/A',
            suggested_action='N/A',
        )

    formatted_prompt = triage_prompt.format(
        lead_name=f'{lead.first_name} {lead.last_name}',
        lead_email=lead.email,
        company_name=lead.company_name,
        company_domain=lead.company_domain,
        company_size=lead.company_size,
        use_case=lead.use_case,
        scraped_title=profile.title,
        scraped_description=profile.meta_description,
        scraped_h1s=profile.h1_tags,
    )

    result = subprocess.run(
        ['agy', '-p', formatted_prompt],
        capture_output=True,
        text=True,
    )

    ai_output = json.loads(result.stdout.strip())

    return LeadEvaluation(
        tier=ai_output.get('tier'),
        confidence=ai_output.get('confidence'),
        company_summary=ai_output.get('company_summary'),
        pain_point=ai_output.get('pain_point'),
        suggested_action=ai_output.get('suggested_action'),
    )

if __name__ == '__main__':
    # test case 1
    enterprise_lead = InboundLead(
        first_name='Elon',
        last_name='Musk',
        email='elon@linear.app',
        company_name='Linear',
        company_domain='linear.app',
        company_size='50-100',
        use_case='We are deploying AI agents across our issue tracking workflow and hitting 429 rate limit errors in production. Need dedicated throughput (provisioned TPM) and an enterprise ZDR contract before our release next month.'
    )

    print("\n--- Crawling Website for Enterprise Lead ---")
    scraped_profile = asyncio.run(crawl_company(enterprise_lead.extracted_domain))

    print("\n--- Running AI Triage ---")
    eval_result = evaluate_lead(enterprise_lead, scraped_profile)
    eval_result = evaluate_lead(enterprise_lead, scraped_profile)
    print(f"Tier: {eval_result.tier}")
    print(f"Confidence: {eval_result.confidence}")
    print(f"Company Summary: {eval_result.company_summary}")
    print(f"Pain Point: {eval_result.pain_point}")
    print(f"Suggested Action: {eval_result.suggested_action}")

    # test case 2
    spam_lead = InboundLead(
        first_name='Sameer',
        last_name='Student',
        email='sameer@gmail.com',
        company_name='Personal',
        use_case="Just playing around with AI APIs."
    )
    print("\n--- Testing Personal Email (Fast-Fail) ---")
    spam_eval = evaluate_lead(spam_lead, EnrichedCompanyProfile(domain="", crawl_status='failed'))
    print(f"Tier: {spam_eval.tier} | Action: {spam_eval.suggested_action}")