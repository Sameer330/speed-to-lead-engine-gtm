import httpx
from models import EnrichedCompanyProfile
from bs4 import BeautifulSoup
import asyncio

async def crawl_company(domain: str) -> EnrichedCompanyProfile:
    if domain == "":
        return EnrichedCompanyProfile(domain='', crawl_status='no_domain')

    try:
        async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'https://{domain}',
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    },
                    timeout=5.0,
                    follow_redirects=True
                )
        
                soup = BeautifulSoup(response.content, "html.parser")
        
                meta_tag = soup.find("meta", attrs={"name": "description"})
                
                description = None

                if meta_tag and meta_tag.get('content'):
                    description = meta_tag['content']
                    print(f'Meta Description: {description}')
                else:
                    print("No meta description found.")
        
                h1_tags = [h.get_text(strip=True) for h in soup.find_all('h1') if h.get_text(strip=True)]
                
                return EnrichedCompanyProfile(
                    domain=domain,
                    title=soup.title.get_text(strip=True) if soup.title else None,
                    meta_description=description,
                    h1_tags=h1_tags,
                    crawl_status='success',
                )
    except Exception as e:
         return EnrichedCompanyProfile(
              domain=domain,
              crawl_status=f'failed: {str(e)}'
         )

if __name__ == '__main__':
    result = asyncio.run(crawl_company('sarvam.ai'))

    print(f'\nCrawl Result: \n{result.model_dump_json(indent=2)}')