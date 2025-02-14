from fastapi import FastAPI, HTTPException
import uuid
from datetime import datetime
from typing import List

app = FastAPI()

# Initialize in-memory storage of receipts data
receipts_data: dict[str, int] = {}

def calculate_score(retailer_name, total_str, purchaseDate, purchaseTime, items_list):
    # Calculate points from retailer name (each alnum character counts as 1 point)
    retail_points = sum(1 for c in retailer_name if c.isalnum())
    print(f"Adding retail_points {retail_points}")
    # Check if total_str is a valid number divisible by 0.25
    total_points = 0
    try:
        num_total = float(total_str)
        numerals = int(100*num_total)
        if int(100*num_total) % 25 == 0:
            total_points += 25
        if int(100*num_total) % 100 == 0:
            total_points += 50
    except ValueError:
        pass  # consider it invalid, no points
    
    print(f"Adding total points {total_points}")
    # Calculate points from items
    item_points = 0
    for i, item in enumerate(items_list):
        short_desc = item['shortDescription'].strip()
        price = float(item.get('price', 0.0))
        len_short = len(short_desc) if isinstance(short_desc, str) else 0
        if len_short % 3 == 0 and len_short > 0:
            #item_points += 1
            print(item)
            calc_price = round((price * 0.2) +0.5)  # Equivalent to ceiling function
            item_points += calc_price
            print(f"Adding item_points {calc_price}")
        if i % 2 == 1:
            item_points += 5
            print(f"Adding item_points 5")
    
    # Check date for odd or even day
    purchase_split = purchaseDate.split("-")
    current_day = int(purchase_split[2])  # This would be obtained from a real calendar function
    if current_day % 2 == 1:
        date_points = 6
    else:
        date_points = 0
    print(f"Adding date_points {date_points}")
    
    # Check time within 14:00 to 15:59 for additional points
    split_time = purchaseTime.split(":")
    hour = int(split_time[0])
    minute =  int(split_time[1])
    if (hour == 14 and
        minute >= 0 and
        hour <= 15 and
        minute < 60):
        time_points = 10
    else:
        time_points = 0

    print(f"Adding time_points {time_points}")

    
    total_score = (
        retail_points +
        total_points +
        item_points +
        date_points +
        time_points
    )
    
    return total_score


@app.post("/receipts/process")
async def process_receipt(receipt_json: dict):
    # Validate input receipt JSON
    if not isinstance(receipt_json, dict) or 'retailer' not in receipt_json:
        raise HTTPException(status_code=400, detail="Invalid receipt format")

    retailer = receipt_json['retailer']
    purchaseTime = receipt_json['purchaseTime']
    items = receipt_json['items']
    purchaseDate = receipt_json['purchaseDate']
    total = receipt_json['total']
    points_earned = calculate_score(retailer,total,purchaseDate, purchaseTime, items) 
    receipt_id = str(uuid.uuid4())
    receipts_data[receipt_id] = points_earned
    return {"id": receipt_id}

@app.get("/receipts/{receipt_id}/points")
async def get_points(receipt_id: str):
    if receipt_id not in receipts_data:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return {"points": receipts_data[receipt_id]}