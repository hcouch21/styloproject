from LinguisticFeature import *

class CharCount(LinguisticFeature):
    _short_name = "CharCount"
    _long_name = "Character Count"
    _description = "Number of characters in the sample."

    _plain_text = True

    def extract(sample):
        return len(sample)

