import requests

receipt_example_1 = {
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}

receipt_example_2 = {
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}

def main():
    # send a post request to http://127.0.0.1:8000/receipts/process with the receipt_example as json body
    response = requests.post('http://127.0.0.1:8000/receipts/process', json=receipt_example_1) 
    given_id = response.json()['id']
    # send a get request to http://127.0.0.1:8000/receipts/<given_id>/points with the given id as path parameter
    response = requests.get('http://127.0.0.1:8000/receipts/' + str(given_id) + '/points') 
    print(response.text)

    response = requests.post('http://127.0.0.1:8000/receipts/process', json=receipt_example_2) 
    given_id = response.json()['id']
    #print(response.headers)
    # send a get request to http://127.0.0.1:8000/receipts/<given_id>/points with the given id as path parameter
    response = requests.get('http://127.0.0.1:8000/receipts/' + str(given_id) + '/points') 
    print(response.text)
    #print(response.headers)



if __name__ == "__main__":
    main()