from models import InboundLead, EnrichedCompanyProfile, LeadEvaluation
import json
import os
import httpx

def format_slack_dossier(lead: InboundLead, profile: EnrichedCompanyProfile, evaluation: LeadEvaluation) -> dict:
    tier_emoji = "🚨" if "Tier A" in evaluation.tier else ("📅" if "Tier B" in evaluation.tier else "ℹ️")

    payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{tier_emoji} [{evaluation.tier.upper()}] Inbound Lead: {lead.first_name} {lead.last_name} @ {lead.company_name}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Company:*\n{lead.company_name} ({lead.extracted_domain or 'N/A'})"},
                        {"type": "mrkdwn", "text": f"*Contact:*\n{lead.first_name} {lead.last_name} (<mailto:{lead.email}|{lead.email}>)"},
                        {"type": "mrkdwn", "text": f"*Company Size:*\n{lead.company_size or 'Unknown'}"},
                        {"type": "mrkdwn", "text": f"*Evaluation Confidence:*\n{evaluation.confidence}"}
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*🏢 Company Overview:*\n{evaluation.company_summary}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*⚡ Technical Bottleneck (AE Cheat Sheet):*\n{evaluation.pain_point}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*🎯 Recommended Next Action:*\n{evaluation.suggested_action}"
                    }
                }
            ]
        }
    return payload

async def send_slack_alert(payload: dict, webhook_url: str | None = None) -> bool:
    url = webhook_url or os.getenv('SLACK_WEBHOOK_URL')
    if url:
        response = await httpx.post(url, json=payload, timeout=5.0)
        return response.status_code == 200
    else:
        print("\n[SIMULATED SLACK DISPATCH]")
        header_text = payload["blocks"][0]["text"]["text"]
        print(f"Channel: #inbound-sales-alerts | {header_text}")
        return True