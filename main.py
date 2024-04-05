import pandas as pd
from amazon_scrape import scrape_listing


def main():
    listing_url  = "https://www.amazon.com/s?k=nunchucks&s=review-rank&qid=1712343083&ref=sr_st_review-rank&ds=v1%3ASrhk8QHvIlb0ZpSFjkxs0LoUXe3il2JdpIwi5rFGtTQ"
    max_products = 10
    products_data = scrape_listing(listing_url, max_products)
    # Convert to DataFrame and save
    df = pd.DataFrame(products_data)
    df.to_csv("products_data.csv", index=False)


if __name__ == '__main__':
    main()

#TODO tomorrow add selenium for sorting by popular!
