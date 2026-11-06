import requests
import re

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

variables = {
    'page': 1,
    'perPage': 50
}

url = 'https://graphql.anilist.co'


response = requests.post(url, json={'query': query, 'variables': variables})
result = response.json()

def clean_description(text):
    paragraphs = text.split('\n\n')
    for p in paragraphs:
        if not p.startswith('__'):
            return p
        if not text:
            return None
    return None

if 'errors' in result:
    print(result['errors'])
else:
    character = result['data']['Page']['characters']
    for c in character:
        if c['gender'] == 'Female':
            print(c['name']['full'])
            if c['media']['nodes']:
                print(c['media']['nodes'][0]['title']['romaji'])
            if c['image']:
                print(c['image']['large'])
            desc = clean_description(c['description'])
            if desc:
                print(repr(desc))
            print(c['age'])
            print(c['gender'])


