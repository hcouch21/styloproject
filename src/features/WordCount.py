from LinguisticFeature import *

class WordCount(LinguisticFeature):
    _short_name = "WordCount"
    _long_name = "Word Count"
    _description = "Number of words in the sample."

    _plain_text = False

    def extract(self, sample):
        return len(sample)
