import os
import pandas as pd

# Use the folder where this script is located, no matter where you run it from
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# The 9 brand files (cclass, focus and the unclean files are excluded on purpose)
BRAND_FILES = {
    "audi": "audi.csv",
    "bmw": "bmw.csv",
    "ford": "ford.csv",
    "hyundai": "hyundi.csv",   # the file name is misspelled in the dataset
    "mercedes": "merc.csv",
    "skoda": "skoda.csv",
    "toyota": "toyota.csv",
    "vauxhall": "vauxhall.csv",
    "vw": "vw.csv",
}

frames = []
for brand, filename in BRAND_FILES.items():
    df = pd.read_csv(os.path.join(DATA_DIR, filename))
    df = df.rename(columns={"tax(£)": "tax"})      # hyundai uses a different column name
    df["brand"] = brand
    frames.append(df)

cars = pd.concat(frames, ignore_index=True)

# Basic cleaning
cars["model"] = cars["model"].str.strip()
cars = cars.drop_duplicates()
cars = cars[(cars["price"] > 0) & (cars["engineSize"] > 0)]
cars = cars[cars["year"] <= 2020]                  # the data was scraped in 2020

print(cars.shape)
print(cars.isna().sum())
print(cars.head())

cars.to_csv(os.path.join(DATA_DIR, "cars_merged.csv"), index=False)
