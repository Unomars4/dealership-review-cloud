import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os

def get_request(url, **kwargs):
    print(kwargs)
    try:
        if "api_key" in kwargs:
            api_key = kwargs["api_key"]
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        print("Network exception occurred")
    
    status_code = response.status_code
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)



def get_dealers_from_cf(url, **kwargs):
    "Parses JSON results into a CarDealer object list"

    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("DEaler",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, dealerId):
    "Parse JSON results into a CarDealer object list based on the dealer id"
    results = []
    json_results = get_request(url, dealer_id=dealerId)
    if json_results:
        dealers = json_results
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)
    
    return results

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_results = get_request(url, id=dealerId)
    print(json_results)
    if json_results:
        reviews = json_results
        for review in reviews:
            sentiment = analyze_review_sentiments(review["review"])
            review_obj = DealerReview(id=review["id"], name=review["name"], purchase=review["purchase"],
                                      review=review["review"], dealership=review["dealership"], sentiment=sentiment)
            results.append(review_obj)
    return results

def analyze_review_sentiments(dealer_review):
    url = os.environ.get("NLU_URL")
    api_key = os.environ.get("NLU_API_KEY")
    version = "2022-04-07"
    features = ["sentiment"]
    return_analyzed_text = True
    lang = "en"
    
    sentiment = get_request(f"{url}/v1/analyze", text=dealer_review, api_key=api_key, language=lang,
                            features=features, version=version, return_analyzed_text=return_analyzed_text)
    
    if "error" in sentiment:
        return sentiment["error"]
    
    return sentiment["sentiment"]["document"]["label"]

