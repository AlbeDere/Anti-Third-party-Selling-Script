import pandas as pd
from amazon import scrape_listing
import ebay


def main():
    product_name = input("What is the product name: ").strip().replace(" ", "+")
    listing_url  = f"https://www.amazon.com/s?k={product_name}&s=review-rank"
    print(listing_url)
    max_products = 10
    max_price = 250
    products_data = scrape_listing(listing_url, max_products, max_price)
    # Convert to DataFrame and save
    df = pd.DataFrame(products_data)
    df.to_csv("products_data.csv", index=False)


if __name__ == '__main__':
    main()

