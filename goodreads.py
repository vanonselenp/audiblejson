from lxml import html
import requests

import json

base_url = "https://www.goodreads.com/"

def get_page(url='https://www.goodreads.com/search?q=watercolor&qid='):
    page = requests.get(url)
    text = page.text
    return html.fromstring(text)

def get_books(tree):
    result = []
    books = tree.xpath('//tr[@itemtype="http://schema.org/Book"]')
    for book in books:
        tds = book.getchildren()
        title = tds[0].getchildren()[1].values()
        rating = tds[1].getchildren()[5].getchildren()[0].getchildren()[0].getchildren()[0].tail.split('—')[1].split(' ')[1]
        result.append({
            "title": title[0],
            "url": title[1],
            "ratings": int("".join(rating.split(',')))
        })
    return result

def get_next_page(page):
    next = page.xpath('//a[@class="next_page"]')[0]
    return "%s%s" % (base_url, next.values()[2])
    
def download_all_books():
    page = get_page()
    books = []

    while(True):
        books.extend(get_books(page))
        try:
            x = get_next_page(page)
        except:
            break
        page = get_page(x)
        print(len(books))

    with open('books.json', 'w') as f:
        f.write(json.dumps(books))

if __name__ == "__main__":
    with open('books.json', 'r') as f:
        data = json.loads(f.read())

    def sorter(element):
        return element["ratings"]
    
    data.sort(reverse=True, key=sorter)
    print(json.dumps(data))

#     <tr itemscope="" itemtype="http://schema.org/Book">
#     <td width="5%" valign="top">
#       <div id="164100" class="u-anchorTarget"></div>
#         <a title="Egon Schiele: Drawings and Watercolors" href="/book/show/164100.Egon_Schiele?from_search=true&amp;from_srp=true&amp;qid=do5sNrPANB&amp;rank=1">
#           <img alt="Egon Schiele: Drawings and ..." class="bookCover" itemprop="image" src="https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1347488415i/164100._SY75_.jpg">
# </a>    </td>
#     <td width="100%" valign="top">
#       <a class="bookTitle" itemprop="url" href="/book/show/164100.Egon_Schiele?from_search=true&amp;from_srp=true&amp;qid=do5sNrPANB&amp;rank=1">
#         <span itemprop="name" role="heading" aria-level="4">Egon Schiele: Drawings and Watercolors</span>
# </a>      <br>
#         <span class="by">by</span>
# <span itemprop="author" itemscope="" itemtype="http://schema.org/Person">
# <div class="authorName__container">
# <a class="authorName" itemprop="url" href="https://www.goodreads.com/author/show/95311.Jane_Kallir?from_search=true&amp;from_srp=true"><span itemprop="name">Jane Kallir</span></a>, 
# </div>
# <div class="authorName__container">
# <a class="authorName" itemprop="url" href="https://www.goodreads.com/author/show/76912.Ivan_Vartanian?from_search=true&amp;from_srp=true"><span itemprop="name">Ivan Vartanian</span></a> <span class="authorName greyText smallText role">(Editor)</span>, 
# </div>
# <div class="authorName__container">
# <a class="authorName" itemprop="url" href="https://www.goodreads.com/author/show/115187.Richard_Avedon?from_search=true&amp;from_srp=true"><span itemprop="name">Richard Avedon</span></a> <span class="authorName greyText smallText role">(Foreword by)</span>
# </div>
# </span>

#         <br>
#         <div>
#           <span class="greyText smallText uitext">
#                 <span class="minirating">
#                   <span class="stars staticStars notranslate">
#                       <span size="12x12" class="staticStar p10"></span><span size="12x12" class="staticStar p10"></span><span size="12x12" class="staticStar p10"></span><span size="12x12" class="staticStar p10"></span><span size="12x12" class="staticStar p3"></span></span> 4.26 avg rating — 2,864 ratings</span>
#               —
#                 published
#                2003
#               —
#               <a class="greyText" rel="nofollow" href="/work/editions/158419-egon-schiele-drawings-and-watercolors">1 edition</a>
#           </span>
#         </div>


        

#           <div style="float: left">
#             <div class="wtrButtonContainer" id="1_book_164100">
# <div class="wtrUp wtrLeft">
# <form action="/shelf/add_to_shelf" accept-charset="UTF-8" method="post"><input name="utf8" type="hidden" value="✓"><input type="hidden" name="authenticity_token" value="k+qZW7Xk6jacdnDr3tiuB/w+G8w6PSKwLMzSewCByZhL69rkd7pukZajLDtuyEb1toStYl5q1+i83cltZndDcw==">
# <input type="hidden" name="book_id" id="book_id" value="164100">
# <input type="hidden" name="name" id="name" value="to-read">
# <input type="hidden" name="unique_id" id="unique_id" value="1_book_164100">
# <input type="hidden" name="wtr_new" id="wtr_new" value="true">
# <input type="hidden" name="from_choice" id="from_choice" value="false">
# <input type="hidden" name="from_home_module" id="from_home_module" value="false">
# <input type="hidden" name="ref" id="ref" value="" class="wtrLeftUpRef">
# <input type="hidden" name="existing_review" id="existing_review" value="false" class="wtrExisting">
# <input type="hidden" name="page_url" id="page_url">
# <input type="hidden" name="from_search" id="from_search" value="true">
# <input type="hidden" name="qid" id="qid" value="do5sNrPANB">
# <input type="hidden" name="rank" id="rank" value="1">
# <button class="wtrToRead" type="submit">
# <span class="progressTrigger">Want to Read</span>
# <span class="progressIndicator">saving…</span>
# </button>
# </form>

# </div>

# <div class="wtrRight wtrUp">
# <form class="hiddenShelfForm" action="/shelf/add_to_shelf" accept-charset="UTF-8" method="post"><input name="utf8" type="hidden" value="✓"><input type="hidden" name="authenticity_token" value="k+qZW7Xk6jacdnDr3tiuB/w+G8w6PSKwLMzSewCByZhL69rkd7pukZajLDtuyEb1toStYl5q1+i83cltZndDcw==">
# <input type="hidden" name="unique_id" id="unique_id" value="1_book_164100">
# <input type="hidden" name="book_id" id="book_id" value="164100">
# <input type="hidden" name="a" id="a">
# <input type="hidden" name="name" id="name">
# <input type="hidden" name="from_choice" id="from_choice" value="false">
# <input type="hidden" name="from_home_module" id="from_home_module" value="false">
# <input type="hidden" name="page_url" id="page_url">
# <input type="hidden" name="from_search" id="from_search" value="true">
# <input type="hidden" name="qid" id="qid" value="do5sNrPANB">
# <input type="hidden" name="rank" id="rank" value="1">
# </form>

# <button class="wtrShelfButton"></button>
# <div class="wtrShelfMenu">
# <div class="wtrShelfList">
# <ul class="wtrExclusiveShelves">
# <li data-shelf-name="read">
# <button class="wtrExclusiveShelf" name="name" type="submit" value="read">
# <span class="progressTrigger">Read</span>
# <img alt="saving…" class="progressIndicator" src="https://s.gr-assets.com/assets/loading-trans-ced157046184c3bc7c180ffbfc6825a4.gif">
# </button>

# </li>
# <li data-shelf-name="currently-reading">
# <button class="wtrExclusiveShelf" name="name" type="submit" value="currently-reading">
# <span class="progressTrigger">Currently Reading</span>
# <img alt="saving…" class="progressIndicator" src="https://s.gr-assets.com/assets/loading-trans-ced157046184c3bc7c180ffbfc6825a4.gif">
# </button>

# </li>
# <li data-shelf-name="to-read">
# <button class="wtrExclusiveShelf" name="name" type="submit" value="to-read">
# <span class="progressTrigger">Want to Read</span>
# <img alt="saving…" class="progressIndicator" src="https://s.gr-assets.com/assets/loading-trans-ced157046184c3bc7c180ffbfc6825a4.gif">
# </button>

# </li>
# <li data-shelf-name="abandoned">
# <button class="wtrExclusiveShelf" name="name" type="submit" value="abandoned">
# <span class="progressTrigger">abandoned</span>
# <img alt="saving…" class="progressIndicator" src="https://s.gr-assets.com/assets/loading-trans-ced157046184c3bc7c180ffbfc6825a4.gif">
# </button>

# </li>
# </ul>
# <ul class="wtrNonExclusiveShelves">
# <li data-shelf-name="maybe">
# <label><img alt="loading…" class="progressIndicator" src="https://s.gr-assets.com/assets/loading-trans-ced157046184c3bc7c180ffbfc6825a4.gif">
# <input type="checkbox" name="name" id="name" value="maybe" class="progressTrigger wtrNonExclusiveShelf">
# maybe
# </label></li>

# <li data-shelf-name="watercolor">
# <label><img alt="loading…" class="progressIndicator" src="https://s.gr-assets.com/assets/loading-trans-ced157046184c3bc7c180ffbfc6825a4.gif">
# <input type="checkbox" name="name" id="name" value="watercolor" class="progressTrigger wtrNonExclusiveShelf">
# watercolor
# </label></li>

# </ul>
# <div class="wtrShelfSearchAddShelf">
# <form autocomplete="off" action="https://www.goodreads.com/shelf/add_to_shelf" accept-charset="UTF-8" method="post"><input name="utf8" type="hidden" value="✓"><input type="hidden" name="authenticity_token" value="k+qZW7Xk6jacdnDr3tiuB/w+G8w6PSKwLMzSewCByZhL69rkd7pukZajLDtuyEb1toStYl5q1+i83cltZndDcw==">
# <input type="hidden" name="unique_id" id="unique_id">
# <input type="hidden" name="book_id" id="book_id">
# <button class="progressTrigger" name="name" type="submit" value="">
# Add "<span class="wtrButtonLabelShelfName"></span>" Shelf
# </button>
# <img alt="saving…" class="progressIndicator" src="https://s.gr-assets.com/assets/loading-trans-ced157046184c3bc7c180ffbfc6825a4.gif">
# </form>

# </div>
# </div>
# <div class="wtrOtherShelfOptions">
# <label class="wtrExclusiveShelf wtrAddShelf" for="add_shelf_1_book_164100">Add shelf</label>
# <form class="wtrAddShelf gr-form gr-form--compact" autocomplete="off" action="https://www.goodreads.com/shelf/add_to_shelf" accept-charset="UTF-8" method="post"><input name="utf8" type="hidden" value="✓"><input type="hidden" name="authenticity_token" value="k+qZW7Xk6jacdnDr3tiuB/w+G8w6PSKwLMzSewCByZhL69rkd7pukZajLDtuyEb1toStYl5q1+i83cltZndDcw==">
# <input type="hidden" name="unique_id" id="unique_id">
# <input type="hidden" name="book_id" id="book_id">
# <input type="hidden" name="from_choice" id="from_choice" value="false">
# <input type="text" name="name" id="add_shelf_1_book_164100" autocorrect="off" autocomplete="off">
# <img alt="saving…" class="progressIndicator" src="https://s.gr-assets.com/assets/loading-trans-ced157046184c3bc7c180ffbfc6825a4.gif">
# <button name="button" type="submit" class="gr-form--compact__submitButton progressTrigger">Add</button>
# </form>

# </div>
# </div>
# </div>

# <div class="ratingStars wtrRating">
# <div class="starsErrorTooltip hidden">
# Error rating book. Refresh and try again.
# </div>
# <div class="myRating uitext greyText">Rate this book</div>
# <div class="clearRating uitext" style="display: none;">Clear rating</div>
# <div class="stars" data-resource-id="164100" data-user-id="51083862" data-submit-url="/review/rate/164100?from_search=true&amp;from_srp=true&amp;qid=do5sNrPANB&amp;rank=1&amp;stars_click=true&amp;wtr_button_id=1_book_164100" data-rating="0"><a class="star off" title="did not like it" href="#" ref="">1 of 5 stars</a><a class="star off" title="it was ok" href="#" ref="">2 of 5 stars</a><a class="star off" title="liked it" href="#" ref="">3 of 5 stars</a><a class="star off" title="really liked it" href="#" ref="">4 of 5 stars</a><a class="star off" title="it was amazing" href="#" ref="">5 of 5 stars</a></div>
# </div>

# </div>

#           </div>
#           <div class="getACopyButtonWrapper getACopyButtonWrapper--desktop">
#             <div data-react-class="ReactComponents.GetACopyButton" data-react-props="{&quot;getACopyDataUrl&quot;:&quot;/book/164100/buy_buttons&quot;}"><div data-reactid=".2ckwia7lv1q" data-react-checksum="1770930766"><button class="gr-button gr-button--fullWidth u-paddingTopTiny u-paddingBottomTiny u-defaultType" data-reactid=".2ckwia7lv1q.0">Get a copy</button></div></div>
#           </div>


#             </td>
#             <td width="130px">

#       </td>

#   </tr>