from lxml import html
import requests


def get_tree(url='http://www.audible.com/search/ref=a_search_c4_1_1_1_srAuth?searchAuthor=The+Great+Courses&qid=1433065261&sr=1-1&searchSize=404'):
    page = requests.get(url)
    text = page.text
    return html.fromstring(text) 


def create_title(element):
    result = {}
    for item in element.items():
        if item[0] == 'href':
            result['link'] = "http://www.audible.com%s" % item[1].lstrip('\n')
        elif item[0] == 'alt':
            result['title'] = item[1]
            print item[1]
    return result


def create_metadata(element):
    result = {}
    rating = element.find_class('boldrating')
    if len(rating) > 0:
        result['rating'] = rating[0].text.rstrip('\n\t                        ').lstrip('\n\t                            ')
    else:
        result['rating'] = 'Not Yet Rated'
    links = element.find_class('adbl-link')
    result['author'] = links[0].text
    result['narrator'] = links[1].text
    series = element.find_class('adbl-series-link')
    if len(series) > 0:
        result['series'] = [l.text for l in element.find_class('adbl-series-link')[0].find_class('adbl-link')]
    result['length'] = element[-3].getchildren()[1].text
    result['release'] = element[-2].getchildren()[1].text
    return result


def get_book_elements(entry):
    output = []
    for element in entry.getchildren():
        children = element.getchildren()
        if len(children) > 0:
            output.extend(children)
    return output[:-1]


def get_titles_dict(tree):
    entries = tree.xpath('//div[@class="adbl-prod-meta-data-cont"]')
    result = []

    for entry in entries:
        book = {}
        elements = get_book_elements(entry)
        for element in elements:
            if element.tag == 'a':
                book.update(create_title(element))
            if element.tag == 'ul':
                book.update(create_metadata(element))
        result.append(book)
    return result


def run():
    tree = get_tree()
    next = tree.find_class('adbl-page-next')[0]
    result = get_titles_dict(tree)
    while next is not None:
        url = next.getchildren()[0].get('href')
        if url is None:
            return result
        print url
        tree = get_tree('http://www.audible.com%s' % url)
        next = tree.find_class('adbl-page-next')[0]
        result.extend(get_titles_dict(tree))
    return result
    

if __name__ == '__main__':
    run()
#print(page.read())

