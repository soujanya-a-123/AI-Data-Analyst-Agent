import pandas as pd
import random
from datetime import datetime, timedelta


random.seed(42)


# ============================================================
# SETTINGS
# ============================================================

num_records = 500


regions = [
    "North",
    "South",
    "East",
    "West"
]

states = {
    "North": ["Delhi", "Punjab", "Haryana"],
    "South": ["Karnataka", "Tamil Nadu", "Telangana"],
    "East": ["West Bengal", "Odisha", "Bihar"],
    "West": ["Maharashtra", "Gujarat", "Rajasthan"]
}

cities = {
    "Delhi": ["Delhi"],
    "Punjab": ["Amritsar", "Ludhiana"],
    "Haryana": ["Gurugram", "Faridabad"],
    "Karnataka": ["Bengaluru", "Mysuru"],
    "Tamil Nadu": ["Chennai", "Coimbatore"],
    "Telangana": ["Hyderabad"],
    "West Bengal": ["Kolkata"],
    "Odisha": ["Bhubaneswar"],
    "Bihar": ["Patna"],
    "Maharashtra": ["Mumbai", "Pune"],
    "Gujarat": ["Ahmedabad", "Surat"],
    "Rajasthan": ["Jaipur"]
}

categories = {
    "Electronics": [
        "Laptop",
        "Smartphone",
        "Tablet",
        "Headphones"
    ],
    "Furniture": [
        "Chair",
        "Desk",
        "Sofa",
        "Bookshelf"
    ],
    "Clothing": [
        "Shirt",
        "Jeans",
        "Jacket",
        "Shoes"
    ],
    "Office": [
        "Printer",
        "Notebook",
        "Pen",
        "Monitor"
    ]
}


# ============================================================
# GENERATE DATA
# ============================================================

records = []

start_date = datetime(2025, 1, 1)

for i in range(1, num_records + 1):

    region = random.choice(regions)

    state = random.choice(
        states[region]
    )

    city = random.choice(
        cities[state]
    )

    category = random.choice(
        list(categories.keys())
    )

    product = random.choice(
        categories[category]
    )

    quantity = random.randint(
        1,
        10
    )

    unit_price = random.randint(
        500,
        50000
    )

    sales = quantity * unit_price

    discount = random.choice(
        [0, 5, 10, 15, 20]
    )

    discount_amount = (
        sales * discount / 100
    )

    final_sales = (
        sales - discount_amount
    )

    profit = (
        final_sales * random.uniform(
            0.05,
            0.30
        )
    )

    order_date = (
        start_date
        + timedelta(
            days=random.randint(
                0,
                364
            )
        )
    )

    customer = (
        f"Customer_{random.randint(1, 100)}"
    )

    salesperson = (
        f"Salesperson_{random.randint(1, 15)}"
    )

    records.append(
        {
            "Order_ID": i,
            "Order_Date": order_date.strftime(
                "%Y-%m-%d"
            ),
            "Customer": customer,
            "Region": region,
            "State": state,
            "City": city,
            "Category": category,
            "Product": product,
            "Quantity": quantity,
            "Sales": round(
                final_sales,
                2
            ),
            "Discount": discount,
            "Profit": round(
                profit,
                2
            ),
            "Salesperson": salesperson
        }
    )


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(
    records
)


# ============================================================
# SAVE
# ============================================================

df.to_csv(
    "sample_data.csv",
    index=False
)


print(
    "sample_data.csv created successfully!"
)

print(
    f"Rows: {len(df)}"
)

print(
    f"Columns: {len(df.columns)}"
)