chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "searchAmazon",
    title: "Search Similar Products",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "searchAmazon") {
    const selectedText = info.selectionText;
    if (selectedText) {
      fetch(`http://localhost:5000/scrape?product_name=${encodeURIComponent(selectedText)}&limit=10`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        const products = JSON.stringify(data.products);
        const nonce = data.nonce;
        const searchKeyword = selectedText;

        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: displayResults,
          args: [products, nonce, searchKeyword] // Pass serialized data and search keyword
        });
      })
      .catch(error => console.error('Error:', error));
    }
  }
});

function displayResults(products, nonce, searchKeyword) {
  products = JSON.parse(products); // Deserialize the products

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
        <input type='text' id='productName' placeholder='Enter product name' value="${searchKeyword}">
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
      <script nonce="${nonce}">
        window.addEventListener('load', () => {
          console.log('Result window DOM fully loaded and parsed');
          if (window.setupSearch && window.searchProducts) {
            window.setupSearch();
            window.searchProducts(); // Automatically search with the initial keyword
          } else {
            console.error('setupSearch or searchProducts is not defined');
          }
        });
      </script>
    </body>
    </html>
  `);
  doc.close();
}
