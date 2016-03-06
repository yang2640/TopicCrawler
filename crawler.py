from lxml import html
import requests
import sys
import topic
import argparse
from lxml.html.clean import Cleaner

class Crawler:
    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url, timeout=10)

            # Only store the content if the page load was successful
            if response.ok:
                # clean html tags
                cleaner = Cleaner()
                self.pageContent = cleaner.clean_html(response.content)
            else:
                sys.exit('Error processing URL: %s\nstatus code: %d' % (url, response.status_code))

        except Exception as inst:
            print inst
            sys.exit('Error processing URL: %s\n' % (url))

        # using xpath to get all the content texts
        tree = html.fromstring(self.pageContent)
        self.texts = tree.xpath('//text()')

    def getTexts(self):
        return self.texts

    def getUrl(self):
        return self.url


if __name__ == '__main__':
    """
    example urls:
    url = 'http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?
                s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster'
    url = 'http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/'
    url = 'http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/'
    url = 'http://jakeaustwick.me/scraping-content-with-readability-and-python/'
    """

    # add command lines
    parser = argparse.ArgumentParser(description='give the url, and find the most common topic words')
    parser.add_argument('url', help = 'the url to crawl')
    parser.add_argument('--stemming', action = 'store_true', help = 'define stemming will be performed')
    parser.add_argument('-s', '--stopWordFile', default = 'stop_words', help = 'stop word file path')
    parser.add_argument('-w', '--wordPattern', default = r'\w+[-_]\w+|\w+', help =
                        'reuglar expression defining the word pattern, default is \w+[-_]\w+|\w+')
    parser.add_argument('-d', '--sentDelimiter', default = r'.,!?:;', help =
                        'the delimiter to get short sentence, default is .,?!:;')
    parser.add_argument('-n', '--wordCnt', default = 6, type = int, help = 'number of words to be returned')
    parser.add_argument('-m', '--phraseCnt', default = 4, type = int, help = 'number of phrases to be returned')
    args = parser.parse_args()


    crawler = Crawler(args.url)
    topic = topic.Topic(crawler.getTexts(), args)
    topic.getTopicsHelper(crawler.getTexts())
    res = topic.getTopics()
    print res

