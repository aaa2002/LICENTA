import requests
import xml.etree.ElementTree as ET

def search_arxiv(query, max_results=5):
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"ti:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }

    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return parse_arxiv_response(response.text)
    except Exception as e:
        print("arXiv API error:", e)
        return []

def parse_arxiv_response(xml_text):
    root = ET.fromstring(xml_text)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = []

    for entry in root.findall('atom:entry', ns):
        try:
            title = entry.find('atom:title', ns).text.strip()
            summary = entry.find('atom:summary', ns).text.strip()
            link = entry.find('atom:id', ns).text.strip()
            authors = [
                author.find('atom:name', ns).text.strip()
                for author in entry.findall('atom:author', ns)
            ]

            entries.append({
                'title': title,
                'abstract': summary,
                'url': link,
                'authors': authors
            })
        except Exception as e:
            print("Error parsing entry:", e)

    return entries
