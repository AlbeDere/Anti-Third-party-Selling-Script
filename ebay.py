# import requests
# from configure import SECURITY_APPNAME

# # eBay Finding API endpoint URL
# url = "https://svcs.ebay.com/services/search/FindingService/v1"

# # API request parameters
# params = {
#     'OPERATION-NAME': 'findItemsByKeywords',
#     'SERVICE-VERSION': '1.0.0',
#     'SECURITY-APPNAME': SECURITY_APPNAME,
#     'RESPONSE-DATA-FORMAT': 'JSON',
#     'keywords': 'iphone',
#     'paginationInput.entriesPerPage': '10'  # Number of items per page
# }

# # Make API request
# response = requests.get(url, params=params)

# # Process response
# if response.status_code == 200:
#     data = response.json()
#     # Parse and extract relevant information from the response
#     for item in data['findItemsByKeywordsResponse'][0]['searchResult'][0]['item']:
#         print(item['title'][0], item['sellingStatus'][0]['currentPrice'][0]['__value__'])
# else:
#     print("Error:", response.status_code)


