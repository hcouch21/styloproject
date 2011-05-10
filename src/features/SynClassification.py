#    This file is part of Stylo.
#
#    Stylo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Stylo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Stylo.  If not, see <http://www.gnu.org/licenses/>.

import sys
from nltk.corpus import wordnet

from Domain import FeatureResult
from LinguisticFeature import *

class SynClassification(LinguisticFeature):
    """ Feature that calculates the product of the number of synonyms of
        each word and the minimum nuber of times those synonyms are used
        in the sample
    """
    _short_name = "SynClassification"
    _long_name = "Synonym Classification"
    _description = "Classification of synonym use"

    def extract(self, sample):
        """ For each word in the sample, calculate the product of the 
            number of synonyms that word has and the minimum of the number 
            of times those synonyms are used in the sample.

        """
        # Dictionary of WORD -> [# SYNONYMS, MIN COUNT]
        synonyms = {}

        words = [x.lower() for x in sample.nltk_text]

        # For each word..
        for word in words :
            # Grab all the synonyms..
            lemmas = [x.lemma_names[0] for x in wordnet.synsets(word)]

            # Mark the number of synonyms
            synonyms[word] = [len(lemmas)]

            min_count = sys.maxint
            for synonym in lemmas :
                count = sample.nltk_text.count(synonym)

                if count < min_count :
                    min_count = count

            # Insert the minimum count to the array
            synonyms[word].append(min_count)

        result = FeatureResult(self._short_name)
        result.value = sum([(x[0] * x[1]) for x in synonyms.values()])

        return [result]
