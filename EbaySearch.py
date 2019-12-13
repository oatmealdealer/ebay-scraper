'''Class definition for the EbaySearch object.
Some helper functions also included.'''
from bs4 import BeautifulSoup
import requests


class EbaySearch:
    '''Object class for a given eBay search.'''

    baseUrl = 'https://www.ebay.com/sch/i.html'
    soup = None
    result_count = None
    results = []

    def __init__(self, term, execute_on_init=True):
        self.term = term
        if execute_on_init:
            self.soup = self.execute()
            self.result_count = self.get_result_count()
            self.results = self.get_results()

    def execute(self):
        '''Execute the search and return the resulting page.'''

        args = {
            '_nkw': self.term
        }
        soup = get_page(self.baseUrl, params=args)
        return soup

    def get_result_count(self):
        ''' Get the tag containing the result count for the search.
        Update this later to just return the number.
        '''

        # Collect all instances of the result count header class
        head = self.soup.find_all('h1', class_='srp-controls__count-heading')
        # Return our first result
        return head[0]

    def get_results(self):
        '''Get a list of all the results on the page.'''
        results = []
        links = self.soup.find_all('a', class_='s-item__link')

        for link in links:
            attrs = {}

            # Element 1. The URL, without any parameters
            attrs['URL'] = link['href'][0:link['href'].find("?")]

            # 2. There should be an h3 tag nested inside
            head = link.h3
            # 3. If it's a new listing, there will be a span tag inside.
            if head.span is None:
                attrs['New'] = False
            else:
                attrs['New'] = True
                # If there is a span tag, we want to remove it.
                # Otherwise our text will have "New Listing" at the beginning.
                head.span.extract()
            # Append the title attribute to our dict.
            attrs['Title'] = head.text
            # Finally, append the tag's results to the output.
            results.append(attrs)
        self.results.append(results)
        return results

    def get_item_links(self):
        ''' Given some soup, fetch all the items on the page.'''
        # links = []
        # links = self.soup.find_all(is_item_link)
        return self.soup.find_all(is_item_link)
        # return links


def is_item_link(tag):
    '''Check if a given tag is a link to an eBay item.'''
    if not tag.has_attr('class'):
        return False
    conditions = [
        tag.has_attr('href'),
        tag.name == 'a',
        tag['class'] == 's-item__link'
    ]
    return all(conditions)


def get_page(url, params=None):
    '''
    Given a URL and optional parameters, make the request
    and return it as a BeautifulSoup object.
    '''
    request = requests.get(url, params)  # Get the page via requests

    # Parse the text with BS4 using the lxml parser
    soup = BeautifulSoup(request.text, 'lxml')
    # Return the soup object
    return soup
