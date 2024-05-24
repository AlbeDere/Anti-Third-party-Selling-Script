function searchProducts() {
    var productName = document.getElementById('productName').value;
    var maxPrice = document.getElementById('maxPrice').value;
    var limit = document.getElementById('limit').value;
    var sorting = document.getElementById('sorting').value;
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
    fetch(url)
      .then(response => response.json())
      .then(data => {
        window.location.reload(); // Reload the page with new search results
        displayResults(data);
      })
      .catch(error => console.error('Error:', error));
  }
  