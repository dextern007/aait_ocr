from langdetect import detect
# from textblob import TextBlob

def get_launguage_code(txt):
    return detect(txt)