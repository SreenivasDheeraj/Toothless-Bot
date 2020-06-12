import requests
import webbrowser
import timeit
starttime = timeit.default_timer()
#Function to search stackoverflow(through api) for exact value of query and return json file
def search(query):
    resp=requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&intitle={}&site=stackoverflow".format(query))
    return resp.json()

#Read json file and get the urls of answers to query
def get_urls(json_dict):
    urls=[]
    count=0      #to limit number of maximum results to 3
    for i in json_dict["items"]:
        if ( i["is_answered"]):
            urls.append(i["link"])
            print(i["link"])
            count+=1
        if ( count == 3 or count == len(i)):
            break
    return urls

#Open the query in web browser
def open_urls(url_list):
    for i in url_list:
        webbrowser.open(i)
    if(len(url_list)==0):
        print("Rejection is a part of life don't be sad")

#Sample Implementation
if __name__ == "__main__":
    query=input("Enter your query:")
    json_resp=search(query)
    response=get_urls(json_resp)
    open_urls(response)
