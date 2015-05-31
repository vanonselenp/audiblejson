from lxml import html
import requests

def get_tree():
    page = requests.get('http://www.audible.com/search/ref=a_search_c4_1_1_1_srAuth?searchAuthor=The+Great+Courses&qid=1433065261&sr=1-1&searchSize=404')
    text = page.text
    return html.fromstring(text) 


def create_title(element):
    result = {}
    for item in element.items():
        if item[0] == 'href':
            result['link'] = item[1].lstrip('\n')
        elif item[0] == 'alt':
            result['title'] = item[1]
    return result


def create_metadata(element):
    result = {}
    rating = element.find_class('boldrating')[0].text.rstrip('\n\t                        ').lstrip('\n\t                            ')
    result['rating'] = rating
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
    return get_titles_dict(tree)


if __name__ == '__main__':
    run()
#print(page.read())

