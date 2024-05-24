from flask import Flask, request, jsonify
from flask_cors import CORS
from amazon import scrape_listing

app = Flask(__name__)
CORS(app)

sort_by = {
    "Featured": "https://www.amazon.com/s?k={product_name}",
    "Price: Low to High": "https://www.amazon.com/s?k={product_name}&s=price-asc-rank",
    "Price: High to Low": "https://www.amazon.com/s?k={product_name}&s=price-desc-rank",
    "Avg. Customer Review": "https://www.amazon.com/s?k={product_name}&s=review-rank",
    "Newest Arrivals": "https://www.amazon.com/s?k={product_name}&s=date-desc-rank",
    "Best Sellers": "https://www.amazon.com/s?k={product_name}&s=exact-aware-popularity-rank"
}

@app.route('/scrape', methods=['GET'])
def api_scrape():
    # Extract query parameters
    product_name = request.args.get('product_name', type=str)
    sort_option = request.args.get('sort_by', type=str, default='Featured')
    limit = request.args.get('limit', default=10, type=int)
    max_price = request.args.get('max_price', type=float)
    
    if not product_name:
        return jsonify({"error": "Product name is required"}), 400
    
    product_name = product_name.strip().replace(" ", "+")
    
    listing_url = sort_by[sort_option].format(product_name=product_name)
    products_data = scrape_listing(listing_url, limit, max_price)
    return jsonify(products_data)

if __name__ == '__main__':
    app.run(debug=True)
