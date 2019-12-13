'''Scrape eBay for results of a given search.'''
# import csv
# import pprint
from pprint import PrettyPrinter
from EbaySearch import EbaySearch

# EBAYSEARCH = 'https://www.ebay.com/sch/i.html'
DEFAULT_SEARCH_TERM = 'ipad pro 11 256'
DEBUG = True


def main(term=DEFAULT_SEARCH_TERM):
    '''Given a search term, execute the search.
    Also, print the results to console.
    '''

    # Make a search object with our given term
    if DEBUG:
        print('Searching eBay for %s' % term)
    search = EbaySearch(term)
    # Get our results
    results = search.results

    if DEBUG:
        print(search.result_count.text)

    printer = PrettyPrinter()

    printer.pprint(results)
    newlistings = 0
    for listing in results:
        if listing['New']:
            newlistings += 1
    if DEBUG:
        print('There are %i new listings out of %i on this page.' %
              (newlistings, len(results)))


if __name__ == "__main__":
    main()
