import pandas as pd

df = pd.DataFrame({
    "order_id": ["ORD001", "ORD002", "ORD003"],
    "city": ["北京", "上海", "广州"],
    "amount": [129.9, 89.0, 456.5],
    "quantity": [2, 1, 3],
})
print(df.head(2))
print(df.shape)
print(df.dtypes)
print(df["amount"].describe())