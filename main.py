from flask import Flask, request, jsonify
from flask_cors import CORS
from amazon import scrape_listing

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['GET'])
def api_scrape():
    # Extract query parameters
    product_name = request.args.get('product_name', type=str)
    limit = request.args.get('limit', default=10, type=int)
    max_price = request.args.get('max_price', type=float)
    
    if product_name:
        product_name = product_name.strip().replace(" ", "+")
        listing_url = f"https://www.amazon.com/s?k={product_name}&s=review-rank"
        products_data = scrape_listing(listing_url, limit, max_price)
        return jsonify(products_data)
    else:
        return jsonify({"error": "Product name is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)
