import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time
 
 
def get_request(url, **kwargs):  
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# def get_dealers_from_cf(url):
#     results = []
#     json_result = get_request(url)
#     if json_result:
#         dealers = json_result["body"]
#         for dealer in dealers:
#             dealer_doc = dealer["doc"]
#             dealer_obj = CarDealer(
#                 address=dealer_doc["address"],
#                 city=dealer_doc["city"],
#                 full_name=dealer_doc["full_name"],
#                 id=dealer_doc["id"],
#                 lat=dealer_doc["lat"],
#                 long=dealer_doc["long"],
#                 short_name=dealer_doc["short_name"],
#                 st=dealer_doc["st"],
#                 zip=dealer_doc["zip"]
#             )
#             results.append(dealer_obj)
#     return results

# def get_dealers_from_cf(url, **kwargs):
#     results = []
#     # state = kwargs.get("state")
#     # if state:
#     #     json_result = get_request(url, state=state)
#     # else:
#     json_result = get_request(url)
#     if json_result and "doc" in json_result and "dealerships" in json_result["doc"]:
#     # if json_result:
#         # Get the row list in JSON as dealers
#         # print("63 - RA",json_result)
#         dealerships = json_result["doc"]["dealerships"]
        
#         # For each dealer object
#         for dealership in dealerships:
#             # print(dealer)
#             # Get its content in `doc` object
#             # dealer_doc = dealer["doc"]
#             dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
#                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
#                                 short_name=dealer_doc["short_name"],
#                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
#             results.append(dealer_obj)

#     return results

def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    # if json_result and "doc" in json_result and "dealerships" in json_result["doc"]:
    #     # Get the row list in JSON as dealers
    #     dealerships = json_result["doc"]["dealerships"]
    #     # For each dealer object
    #     for dealer in dealerships:
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   full_name=dealer_doc["full_name"],short_name=dealer_doc["short_name"],                               
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print(json_result)
    if json_result:
        dealers = json_result
        dealer_doc = dealers[0]
        # print(dealer_doc)
        dealer_obj = CarDealer(
            address=dealer_doc["address"],
            city=dealer_doc["city"],
            full_name=dealer_doc["full_name"],
            id=dealer_doc["id"],
            lat=dealer_doc["lat"],
            long=dealer_doc["long"],
            short_name=dealer_doc["short_name"],
            st=dealer_doc["st"],
            zip=dealer_doc["zip"]
        )
    return dealer_obj

def get_dealers_by_st_from_cf(url, state):
    results = []
    json_result = get_request(url, st=state)
    if json_result:
        dealers = json_result["body"]
        for dealer_doc in dealers:
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
 
    if json_result:
        print("line 105",json_result)
        reviews = json_result["data"]["docs"]

        for dealer_review in reviews:
            
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]
            
            # sentiment = analyze_review_sentiments(review_obj.review)
            # print(sentiment)
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            # review_obj.sentiment = sentiment
            results.append(review_obj)

    return results

def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/3bfeac0e-d360-408a-b8e1-edc90ecda864"
    api_key = "f3odHzHvqLN6s8NWKWSoPiagSwt4uxWuptudfThmvhr8"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-08-01',authenticator=authenticator)
    try:
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(sentiment=SentimentOptions(targets=[text]))
        ).get_result()
        label = response['sentiment']['document']['label']
    except Exception as e:
        print("Exception occurred during sentiment analysis:", str(e))
        label = "unknown"
    
    return label
    # natural_language_understanding.set_service_url(url)
    # response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    # label=json.dumps(response, indent=2)
    # label = response['sentiment']['document']['label']
    
    # return(label)
