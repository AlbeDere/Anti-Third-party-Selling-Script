# Amazon Product Similarity Browser Extension

This project is a browser extension that allows users to highlight a product on any webpage, right-click, and search for similar products on Amazon using a custom-built Python API. The results are displayed in a new window.

## Features

- Highlight a product name on any webpage and search for similar products on Amazon.
- Display search results in a new window with product details including title, price, rating, and image.
- Allow users to refine their search with additional parameters: product name, maximum price, limit, and sorting options.

## Setup

### Prerequisites

- Python 3.x
- Flask
- BeautifulSoup
- Requests
- Flask-CORS
- Docker (optional)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/amazon-product-similarity-extension.git
    cd amazon-product-similarity-extension
    ```

2. Set up the Python environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Run the Flask API:
    ```bash
    python main.py
    ```

### Docker

Alternatively, you can run the application using Docker:

1. Build the Docker image:
    ```bash
    docker build -t amazon-extension .
    ```

2. Run the Docker container:
    ```bash
    docker run -p 5000:5000 amazon-extension
    ```

## Configuring the Browser Extension

1. Load the extension into your browser:
    - Open your browser's extension management page (e.g., `chrome://extensions` for Chrome).
    - Enable "Developer mode".
    - Click "Load unpacked" and select the directory containing the extension files.

## Usage

1. Highlight the product name you want to search for on any webpage.
2. Right-click and select "Search Similar Products".
3. A new window will open displaying similar products from Amazon.

## API Endpoints

### `GET /scrape`

Fetch similar products from Amazon.

**Query Parameters:**

- `product_name` (str): Name of the product to search for (required).
- `sort_by` (str): Sorting option (default: 'Featured'). Options include:
  - Featured
  - Price: Low to High
  - Price: High to Low
  - Avg. Customer Review
  - Newest Arrivals
  - Best Sellers
- `limit` (int): Number of products to fetch (default: 10).
- `max_price` (float): Maximum price of products (optional).

**Example Request:**

```bash
curl "http://127.0.0.1:5000/scrape?product_name=laptop&sort_by=Price%3A+Low+to+High&limit=5&max_price=1000"
