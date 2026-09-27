import pandas as pd

# loading all the csv files
customers = pd.read_csv("olist_customers_dataset.csv")
geolocation = pd.read_csv("olist_geolocation_dataset.csv")
order_items = pd.read_csv("olist_order_items_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")
reviews = pd.read_csv("olist_order_reviews_dataset.csv")
orders = pd.read_csv("olist_orders_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
sellers = pd.read_csv("olist_sellers_dataset.csv")
cat_translation = pd.read_csv("product_category_name_translation.csv")

# just checking the shape and columns of each table first
print(orders.shape)
print(orders.columns)
print(orders.head())

print(customers.shape)
print(customers.columns)

print(order_items.shape)
print(order_items.columns)

print(payments.shape)
print(reviews.shape)
print(products.shape)
print(sellers.shape)
print(cat_translation.head())

# order status
print(orders["order_status"].value_counts())

# converting date columns so i can do date math
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
orders["order_estimated_delivery_date"] = pd.to_datetime(orders["order_estimated_delivery_date"])

print(orders["order_purchase_timestamp"].min())
print(orders["order_purchase_timestamp"].max())

# only delivered orders, cause the others don't have a delivery date
delivered = orders[orders["order_status"] == "delivered"].copy()

# how late is each order compared to what was estimated
delivered["delay_days"] = (delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]).dt.days

late_orders = delivered[delivered["delay_days"] > 0]
print(len(delivered))
print(len(late_orders))
print(len(late_orders) / len(delivered) * 100)
print(late_orders["delay_days"].mean())

# now check if late orders get worse reviews
merged = delivered.merge(reviews[["order_id", "review_score"]], on="order_id")
merged["is_late"] = merged["delay_days"] > 0
print(merged.groupby("is_late")["review_score"].mean())

# which categories make the most money
item_prod = order_items.merge(products[["product_id", "product_category_name"]], on="product_id")
item_prod = item_prod.merge(cat_translation, on="product_category_name")
category_revenue = item_prod.groupby("product_category_name_english")["price"].sum()
category_revenue = category_revenue.sort_values(ascending=False)
print(category_revenue.head(10))

# checking how many sellers there are and how much each one sold
seller_revenue = item_prod.groupby("seller_id")["price"].sum().sort_values(ascending=False)
print(len(seller_revenue))
top10 = int(len(seller_revenue) * 0.1)
print(seller_revenue.head(top10).sum() / seller_revenue.sum() * 100)

seller_order_count = order_items.groupby("seller_id")["order_id"].nunique()
print((seller_order_count <= 10).mean() * 100)

# customer states vs seller states
print(customers["customer_state"].value_counts().head())
print(sellers["seller_state"].value_counts().head())

# does shipping across states take longer / cost more
delivered["delivery_days"] = (delivered["order_delivered_customer_date"] - delivered["order_purchase_timestamp"]).dt.days

geo = delivered.merge(customers[["customer_id", "customer_state"]], on="customer_id")
geo = geo.merge(order_items[["order_id", "seller_id", "freight_value", "price"]], on="order_id")
geo = geo.merge(sellers[["seller_id", "seller_state"]], on="seller_id")
geo["same_state"] = geo["customer_state"] == geo["seller_state"]

print(geo.groupby("same_state")["delivery_days"].mean())
print(geo.groupby("same_state")["freight_value"].mean())
print((geo["same_state"] == False).mean() * 100)

# avg delivery time for biggest states
top_states = customers["customer_state"].value_counts().head(8).index
print(geo[geo["customer_state"].isin(top_states)].groupby("customer_state")["delivery_days"].mean().sort_values(ascending=False))

# review score distribution
print(reviews["review_score"].value_counts(normalize=True) * 100)

# how many reviews actually have a written comment
print(reviews["review_comment_message"].notna().mean() * 100)

# missing categories
print(products["product_category_name"].isna().sum())

# payment stuff
print(payments["payment_type"].value_counts(normalize=True) * 100)
print(payments["payment_installments"].mean())
