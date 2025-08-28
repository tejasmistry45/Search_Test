import httpx
from bs4 import BeautifulSoup

async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=10)
        r.raise_for_status()
        return r.text

def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return " ".join(p.get_text() for p in soup.find_all("p"))
