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


# Function to fetch and parse a product page
def scrape_listing(url, limit, max_price, products=None):
    if products is None:
        products = []
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_containers = soup.select("div[data-asin]:not([data-asin=''])")
        
        for container in product_containers:
            if len(products) >= limit:  # Exit if we've collected enough products
                return products
            
            # Price extraction and formatting
            price_element = container.select_one("span.a-price > span.a-offscreen")
            if price_element:
                price_text = price_element.get_text(strip=True)
                price_value = float(price_text.replace('$', '').replace(',', ''))
                if price_value >= max_price:  # Skip if price is above the limit
                    continue
            else:
                continue  # Skip if no price is found
            
            # Extract other product details
            title = container.select_one("a.a-link-normal.a-text-normal").get_text(strip=True) if container.select_one("a.a-link-normal.a-text-normal") else 'N/A'
            rating = container.select_one("i.a-icon-star-small > span").get_text(strip=True) if container.select_one("i.a-icon-star-small > span") else 'N/A'
            image = container.select_one("img.s-image").get('src') if container.select_one("img.s-image") else 'N/A'
            product_url = urljoin(url, container.select_one("a.a-link-normal.a-text-normal").get('href')) if container.select_one("a.a-link-normal.a-text-normal") else 'N/A'
            
            products.append({
                "title": title,
                "price": price_text,
                "rating": rating,
                "image": image,
                "url": product_url
            })
        
        # Check for and process the next page if needed and if not reached the limit
        next_page_el = soup.select_one('a.s-pagination-next')
        if next_page_el and len(products) < limit:
            next_page_url = next_page_el.attrs.get('href')
            next_page_url = urljoin(url, next_page_url)
            return scrape_listing(next_page_url, limit, max_price, products)
    
    return products