import requests
import csv
from time import sleep

page = 1
limit = 50

def parseInfo(csvFile, data):
    news_data = []
    for i in data:
        if( not i["parent_complaint_id"]):
            overview = i["overview"]
            media = i["assets"][0]["rekognition_text"]
            source = i["source"]["name"]
            news_data.append({"source":source, "media":media, "overview": overview})
    csvFile.writerows(news_data)


with open("real.csv", "w",newline='') as f:
    
    fieldnames = ["overview", "media", "source"]
    writer = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    
    
    while True:
        base_URl = f"https://1w03o378z7.execute-api.eu-west-1.amazonaws.com/prod/complaints?page={page}&limit={limit}status=RSV" # for updating the string on every iteration

        r = requests.get(base_URl)
        
        if r.status_code != 200: break
        
        data = r.json()["data"]
        if len(data) > 0:
            parseInfo(writer, data)
        
        else:break
        
        page+=1    
        print(base_URl)       