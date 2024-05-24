from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import base64
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

@app.before_request
def add_nonce():
    nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
    request.nonce = nonce

@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = f"script-src 'self' 'nonce-{request.nonce}' http://localhost:5000;"
    return response

@app.route('/scrape', methods=['GET'])
def api_scrape():
    product_name = request.args.get('product_name', type=str)
    sort_option = request.args.get('sort_by', type=str, default='Featured')
    limit = request.args.get('limit', default=10, type=int)
    max_price = request.args.get('max_price', type=float)
    
    if not product_name:
        return jsonify({"error": "Product name is required"}), 400
    
    product_name = product_name.strip().replace(" ", "+")
    
    listing_url = sort_by[sort_option].format(product_name=product_name)
    products_data = scrape_listing(listing_url, limit, max_price)
    
    # Include the nonce in the response
    return jsonify({"products": products_data, "nonce": request.nonce})

@app.route('/script.js')
def serve_script():
    script_content = """
    function setupSearch() {
        console.log('Setting up search functionality');
        const searchButton = document.getElementById('searchButton');
        if (searchButton) {
            searchButton.addEventListener('click', () => {
                console.log('Search button clicked');
                searchProducts();
            });
        } else {
            console.error('Search button not found');
        }
    }

    function searchProducts() {
        console.log('searchProducts function called');
        var productName = document.getElementById('productName').value;
        var maxPrice = document.getElementById('maxPrice').value;
        var limit = document.getElementById('limit').value;
        var sorting = document.getElementById('sorting').value;
        
        console.log('Product Name:', productName);
        console.log('Max Price:', maxPrice);
        console.log('Limit:', limit);
        console.log('Sorting:', sorting);
        
        var url = 'http://localhost:5000/scrape?product_name=' + encodeURIComponent(productName);
        if (maxPrice) {
            url += '&max_price=' + maxPrice;
        }
        if (limit) {
            url += '&limit=' + limit;
        }
        if (sorting) {
            url += '&sort_by=' + encodeURIComponent(sorting);
        }
        
        console.log('Fetch URL:', url);
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                console.log('Fetch Data:', data);
                updateTable(data.products);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function updateTable(data) {
        console.log('updateTable function called');
        let tableContent = '<tr><th>Title</th><th>Price</th><th>Image</th></tr>';
        if (data && data.forEach) {
            data.forEach(product => {
                tableContent += '<tr><td><a href="' + product.url + '" target="_blank">' + product.title + '</a></td><td>' + product.price + '</td><td><img src="' + product.image + '" alt="' + product.title + '"></td></tr>';
            });
        }
        document.getElementById('resultsTable').innerHTML = tableContent;
    }

    window.setupSearch = setupSearch;
    window.searchProducts = searchProducts;

    document.addEventListener('DOMContentLoaded', setupSearch);
    """
    response = app.make_response(script_content)
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Content-Security-Policy'] = f"script-src 'self' 'nonce-{request.nonce}'"
    return response

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Amazon Product Search</title>
        </head>
        <body>
            <button onclick="showResults()">Show Results</button>
            <script nonce="{{ nonce }}">
                function showResults() {
                    fetch('/scrape?product_name=sample')
                        .then(response => response.json())
                        .then(data => displayResults(data.products, data.nonce))
                        .catch(error => console.error('Error:', error));
                }

                function displayResults(products, nonce) {
                    const resultWindow = window.open("", "Similar Products", "width=600,height=700");
                    const doc = resultWindow.document;

                    doc.open();
                    doc.write(`
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                          <meta charset="UTF-8">
                          <meta name="viewport" content="width=device-width, initial-scale=1.0">
                          <title>Similar Products</title>
                          <style>
                            table { width: 100%; border-collapse: collapse; }
                            th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
                            th { background-color: #f2f2f2; }
                            img { max-width: 100px; max-height: 100px; }
                          </style>
                          <script nonce="${nonce}" src="http://localhost:5000/script.js"></script>
                        </head>
                        <body>
                          <h1 style='text-align: center;'>Similar Products</h1>
                          <div style='text-align: center; margin-bottom: 20px;'>
                            <input type='text' id='productName' placeholder='Enter product name'>
                            <input type='number' id='maxPrice' placeholder='Max Price'>
                            <input type='number' id='limit' placeholder='Limit'>
                            <select id='sorting'>
                              <option value='Featured'>Featured</option>
                              <option value='Price: Low to High'>Price: Low to High</option>
                              <option value='Price: High to Low'>Price: High to Low</option>
                              <option value='Avg. Customer Review'>Avg. Customer Review</option>
                              <option value='Newest Arrivals'>Newest Arrivals</option>
                              <option value='Best Sellers'>Best Sellers</option>
                            </select>
                            <button id='searchButton'>Search</button>
                          </div>
                          <table id="resultsTable">
                            <tr><th>Title</th><th>Price</th><th>Image</th></tr>
                          </table>
                        </body>
                        </html>
                    `);
                    doc.close();
                }
            </script>
        </body>
        </html>
    ''', nonce=request.nonce)


if __name__ == '__main__':
    app.run(debug=True)
