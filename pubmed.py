
import os
import requests

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search_pubmed(query):
    url = f"{BASE_URL}/esearch.fcgi"

    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 3,
        "retmode": "json",
        "api_key": os.getenv("PUBMED_API_KEY")
    }

    res = requests.get(url, params=params)
    data = res.json()

    return data["esearchresult"]["idlist"]


def fetch_abstracts(ids):
    url = f"{BASE_URL}/efetch.fcgi"

    params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml",
        "rettype": "abstract",
        "api_key": os.getenv("PUBMED_API_KEY")
    }

    res = requests.get(url, params=params)
    return res.text

