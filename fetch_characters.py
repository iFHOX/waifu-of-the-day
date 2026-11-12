import json
import time
import requests
import re
import html

query = '''
query ($page: Int, $perPage: Int) {
    Page (page: $page, perPage: $perPage) {
            pageInfo {
                currentPage
                hasNextPage
                perPage
            }
            characters (sort: FAVOURITES_DESC) {
                id
                siteUrl
                image {
                    large
                }
                name {
                    full
                }
                media(perPage: 1) {
                    nodes {
                        title {
                            romaji
                        }
                    }
                }
                description
                age
                gender
            }
        }
    }
'''

def clean_description(text):
    if not text:
        return None
    spoilerpattern = r'~!.*?!~'
    htmlpattern = r'</?(?:a|i|b|br)\b[^>]*>'
    cleanspoiler = re.sub(spoilerpattern, '', text, flags=re.DOTALL)
    cleanhref = re.sub(htmlpattern, '', cleanspoiler, flags=re.IGNORECASE)
    paragraphs = cleanhref.split('\n\n')
    pattern = r'\[(.*?)\]\((.*?)\)'
    for p in paragraphs:
        p = p.strip()
        p = html.unescape(p)
        if p.startswith(('__', '**')):
            continue
        pretexted = re.sub(pattern, r'\1', p)
        cleaned = pretexted.replace('__', '').replace('\n', ' ').replace('**', '').replace('_', '').strip()
        cleaned = ' '.join(cleaned.split())
        if len(cleaned) < 40:
            continue
        return cleaned
    return None

def fetch_page(page):
    variables = {
        'page': page,
        'perPage': 50
    }

    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    result = response.json()
    if 'errors' in result:
        print(result['errors'])
        return None
    else:
        return result['data']['Page']

results = []
page = 1


while len(results) < 400:
    data = fetch_page(page)
    if data is None:
        break
    for c in data['characters']:
        if c['gender'] == 'Female' and c['media']['nodes'] and c['image'] and c['description'] :
            desc = clean_description(c['description'])
            if desc:
                results.append({
                    'name': c['name']['full'],
                    'series': c['media']['nodes'][0]['title']['romaji'],
                    'image': c['image']['large'],
                    'description': desc,
                    'siteUrl': c['siteUrl'],
                })
    if not data['pageInfo']['hasNextPage']:
        break
    print(f"page {page}: {len(results)} so far")
    page += 1
    time.sleep(1)

with open('characters.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)










