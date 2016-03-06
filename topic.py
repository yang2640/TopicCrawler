import re
from collections import defaultdict
from collections import Counter
from stemming.porter2 import stem


class Topic:
    def __init__(self, texts, args):
        self.texts = texts

        # define the sentence delimiters
        self.sentDelimter = args.sentDelimiter

        # define the word tokenize pattern
        self.wordPattern = args.wordPattern

        # set default stop words
        self.setStopWords(args.stopWordFile)

        # if stemming will be performed
        self.stemming = args.stemming

        # the most common number of words will be returned
        self.wordCnt = args.wordCnt

        # the most common number of phrases will be returned
        self.phraseCnt = args.phraseCnt

        # get the stop word lists
        self.wordMap = defaultdict(int)
        self.twoWordPhraseMap = defaultdict(int)
        self.threeWordPhraseMap = defaultdict(int)


    def setWordPattern(self, wordPattern):
        self.wordPattern = wordPattern

    def setSentDelimiter(self, sentDelimiter):
        self.sentDelimter = sentDelimiter

    def sentTokenize(self, text):
        # split into paragraphs
        paragraphs = text.splitlines()

        # split into sentences
        sents = []
        for p in paragraphs:
            sents.extend(re.split(self.sentDelimter, p))

        return sents

    def addWords(self, subwords):
        for x in subwords:
            self.wordMap[x] += 1

    def addOneWordPhrases(self, subwords):
        n = len(subwords)
        for i in xrange(n - 1):
            phrase = '%s %s' % (subwords[i], subwords[i + 1])
            self.twoWordPhraseMap[phrase] += 1

    def addTwoWordPhrases(self, subwords):
        n = len(subwords)
        for i in xrange(n - 2):
            phrase = '%s %s %s' % (subwords[i], subwords[i + 1], subwords[i + 2])
            self.threeWordPhraseMap[phrase] += 1

    def addWordsAndPhrases(self, subwords):
        self.addWords(subwords)
        self.addOneWordPhrases(subwords)
        self.addTwoWordPhrases(subwords)


    # tokenize into words and phrases
    def wordTokenize(self, text):
        # use regular expression to match the words
        found = re.findall(self.wordPattern, text)

        # normalize the words
        normText = self.normalize(found)

        # remove stop words
        if self.stopwords:
            subwords = []
            for x in normText:
                # word lenght <= 2 are not likely to be topic words
                if not x in self.stopwords and len(x) > 2:
                    subwords.append(x)
                else:
                    # conclude last subwords
                    self.addWordsAndPhrases(subwords)
                    subwords = []
        # add last one
        if subwords:
            self.addWordsAndPhrases(subwords)


    def normalize(self, text):
        # all transform to lower case
        text = [x.lower() for x in text]

        # stemming
        if self.stemming:
            text = [stem(x) for x in text]

        return text


    def setStopWords(self, stopWordFile):
        try:
            with open(stopWordFile, 'r') as f:
                self.stopwords = f.read().splitlines()
        except:
            print 'open stopword file %s error!' % (stopWordFile)


    def getTopics(self, phraseFreq = 2):
        # sort the items by count
        wordCounter = Counter(self.wordMap)
        twoWordPhraseCounter = Counter(self.twoWordPhraseMap)
        threeWordPhraseCounter = Counter(self.threeWordPhraseMap)

        res = []
        res.extend([x[0] for x in wordCounter.most_common(self.wordCnt)])
        # remove the phrases that only appear <= phraseFreq times as that is not meaningful
        res.extend([x[0] for x in twoWordPhraseCounter.most_common(self.phraseCnt) if x[1] > phraseFreq])
        res.extend([x[0] for x in threeWordPhraseCounter.most_common(self.phraseCnt) if x[1] > phraseFreq])
        return res

    def getTopicsHelper(self, texts):
        # process the crawled texts
        for text in texts:
            sentences = self.sentTokenize(text)
            for sentence in sentences:
                self.wordTokenize(sentence)





