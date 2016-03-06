Install:
1. You have to install pip
2. pip -r requirements.txt, to install the required packages

-----------------------------------------------------------------------------
Manual:

usage: python crawler.py [-h] [--stemming] [-s STOPWORDFILE] [-w WORDPATTERN]
                  [-d SENTDELIMITER] [-n WORDCNT] [-m PHRASECNT]
                  url

give the url, and find the most common topic words

positional arguments:
  url                   the url to crawl

optional arguments:
  -h, --help            show this help message and exit
  --stemming            define stemming will be performed
  -s STOPWORDFILE, --stopWordFile STOPWORDFILE
                        stop word file path
  -w WORDPATTERN, --wordPattern WORDPATTERN
                        reuglar expression defining the word pattern, default
                        is \w+[-_]\w+|\w+
  -d SENTDELIMITER, --sentDelimiter SENTDELIMITER
                        the delimiter to get short sentence, default is .,?!:;
  -n WORDCNT, --wordCnt WORDCNT
                        number of words to be returned
  -m PHRASECNT, --phraseCnt PHRASECNT
                        number of phrases to be returned


-----------------------------------------------------------------------------
Ideas:

1. Since using nltk or textblob library is cheating by requirement, my motivation is to do word
frequency counting instead of senmentic analysis, e.g. topic model

2. I have cleaned up the html to mainly focus on the content

3. implemented features:
	(1) using regular expression for sentence breaking and word matching
	(2) text normalizing
		<1> all to lowercase
		<2> stemming
	(3) remove stop words
	(4) two-word phrase, and three-word phrase, I enumerate over words for phrases

-----------------------------------------------------------------------------
Issues and bugs:

1. when I query url =
'http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster',
it will fail, as Amazon see me as a robot, how to bypass this ?

2. resulted words and phraszes may contain duplicate information

-----------------------------------------------------------------------------
TODOs:

1. if possible, I shold apply some machine learning techniques, e.g., topic model, to get the words
that have more sementic meaning

2. use lemmanization instead of stemming

3. better phrase support

4. support multiple languages


-----------------------------------------------------------------------------
Examples:
1. python crawler.py http://www.walmart.com/search/\?query\=ipad
[u'shop', 'apple', 'free', 'ipad', u'pickup', 'store', 'store pickup', 'apple items', 'space gray', '16gb wi-fi', '16gb wi-fi refurbished', 'air 16gb wi-fi', 'store pickup today', '7-inch retina display']

2. python crawler.py --stemming http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/
['nsa', 'watch', 'snowden', 'govern', 'work', 'video', 'hong kong']

3. python crawler.py http://jakeaustwick.me/scraping-content-with-readability-and-python/
['url', 'content', 'readability', 'urls', 'redis', 'python', 'jake austwick', 'url-content url']
