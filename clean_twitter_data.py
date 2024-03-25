import csv 
import re

counter = 0

stopwords = ["post", ":", 'replies', 'media', 'likes', "views", "LTE", 'view', "LI", "Vo",  "4G",  "Cell C","real411"]


StrListToLower = lambda x: map(lambda i : i.lower(), x)


def filterString(s):
    if len(s) <= 1: return False
    if s.isnumeric(): return False
    return True


def formatteStr(s):
    return [i for i in s if filterString(i)]


def check_substring_regex(text, subs):
  regex_pattern = r"|".join(subs)  # Join substrings with OR operator
  is_in_stop_words = bool(re.search(regex_pattern, text, re.I))
  views =  bool(re.search(r"(?<!^)(\d+(?:,\d+)*)[kK](?<!$)", text, re.I))
  time = bool(re.search(r"^\d+(d|h)$", text, re.I))
  return any([is_in_stop_words, views, time])


def clean(str):
    new_str = ""
    cleaned = formatteStr(str)
    for i in cleaned:
        if not (check_substring_regex(i, stopwords)):
            new_str= new_str + " " + i
    return new_str



print("hELLO")

with open("twitter.csv", "r", newline='') as inFile, open("clean_twitter.csv", 'w', newline='') as outfile:
    fileReader = csv.reader(inFile)

    fieldnames = ["overview", "media", "source"]
    writer = csv.DictWriter(outfile, delimiter=',', fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

    for row in fileReader:
        if counter > 1:
            new_str = clean(row[1].split("\r\n")).strip()
            writer.writerow({"source":row[2], "media":new_str, "overview": row[0]})
        counter+=1
