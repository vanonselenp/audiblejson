from lxml import html
import requests

def get_tree():
    page = requests.get('http://www.audible.com/search/ref=a_search_c4_1_1_1_srAuth?searchAuthor=The+Great+Courses&qid=1433065261&sr=1-1&searchSize=404')
    text = page.text
    return html.fromstring(text) 

def title_from_entry(entry):
    children = entry.getchildren()
    for c in children:
        if len(c.items()) > 0 and c.items()[0][1] == 'adbl-prod-title':
            return c.getchildren()[0].text
    return ""

def get_titles_dict(tree):
    entry = tree.xpath('//div[@class="adbl-prod-meta-data-cont"]')
    result = []
    for e in entry:
        d = dict() 
        d['title'] = title_from_entry(e)
        result.append(d)
    return result 
                

def run():
    tree = get_tree()
    return get_titles_dict(tree)

if __name__ == '__main__':
    run()
#print(page.read())

