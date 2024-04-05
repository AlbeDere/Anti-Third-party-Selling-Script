import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Headers and initial setup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# Visited URLs for tracking already scraped URLs
already_visited = set()

# Function to fetch and parse a product page
def fetch_product_details(page_url):
    if page_url in already_visited:
        return None
    response = requests.get(page_url, headers=headers)
    if response.status_code == 200:
        already_visited.add(page_url)  # Mark this URL as visited
        soup = BeautifulSoup(response.content, 'html.parser')
        details = {
            'title': soup.select_one("#productTitle").text.strip() if soup.select_one("#productTitle") else 'N/A',
            'price': soup.select_one('span.a-offscreen').text.strip() if soup.select_one('span.a-offscreen') else 'N/A',
            'rating': soup.select_one("#acrPopover").get("title", 'N/A').replace("out of 5 stars", "").strip(),
            'image': soup.select_one("#landingImage").get('src', 'N/A') if soup.select_one("#landingImage") else 'N/A',
            'url': page_url
        }
        return details
    else:
        print(f"Failed to retrieve {page_url}")
        return None

# Function to scrape listing and compile product information
def scrape_listing(url, limit=10):
    products = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_links = soup.select("[data-asin] h2 a")
    
    for link in product_links[:limit]:  # Process only up to 'limit' product links
        product_url = urljoin(url, link['href'])
        product_details = fetch_product_details(product_url)
        if product_details:
            products.append(product_details)
    
    return products