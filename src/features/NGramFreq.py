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

from Domain import FeatureResult
from LinguisticFeature import *

class NGramFreq(LinguisticFeature):
    _short_name = "NGramFreq"
    _long_name = "N-Gram Frequency"
    _description = "Frequency of unigrams, bigrams, and trigrams in the sample"

    def extract(self, sample):
        """ Extract uni-, bi-, and trigram frequency information from a sample
        sample -- Sample to extract from

        """
        unigrams = {}
        bigrams = {}
        trigrams = {}
        num_unigrams = 0
        num_bigrams = 0
        num_trigrams = 0

#        chars = list(sample.plain_text.lower().replace("\n", "")
#                        .replace(" ","").replace("\t", ""))
        chars = [x.lower() for x in sample.nltk_text]
        num_chars = len(chars)

        for i in range(num_chars):
            # Construct Unigram
            unigram = chars[i]

            # Increment unigram counts
            if unigram in unigrams :
                unigrams[unigram] += 1
            else :
                unigrams[unigram] = 1
            num_unigrams += 1

            # Construct Bigram
            if (i < num_chars - 1) :
                bigram = chars[i] + "_" + \
                         chars[i + 1]

                # Increment bigram counts
                if bigram in bigrams :
                    bigrams[bigram] += 1
                else :
                    bigrams[bigram] = 1
                num_bigrams += 1

            # Construct Trigram
            if i < num_chars - 2 :
                trigram = chars[i] + "_" + \
                          chars[i + 1] + "_" + \
                          chars[i + 2]
            
                # Increment trigram counts
                if trigram in trigrams :
                    trigrams[trigram] += 1
                else :
                    trigrams[trigram] = 1
                num_trigrams += 1

        result_set = []

        # Construct unigram FeatureResults
        total = float(num_unigrams)
        for unigram in unigrams :
            result = FeatureResult("Unigram_" + unigram)
            result.value = unigrams[unigram] / total
            result_set.append(result)

        # Construct bigram FeatureResults
        total = float(num_bigrams)
        for bigram in bigrams :
            result = FeatureResult("Bigram_" + bigram)
            result.value = bigrams[bigram] / total
            result_set.append(result)

        # Construct trigram FeatureResults
        total = float(num_trigrams)
        for trigram in trigrams :
            result = FeatureResult("Trigram_" + trigram)
            result.value = trigrams[trigram] / total
            result_set.append(result)

        # Unique unigrams
        result = FeatureResult("UniqueUnigramPct")
        result.value = len(unigrams) / float(num_unigrams)
        result_set.append(result)

        # Unique bigrams
        result = FeatureResult("UniqueBigramPct")
        result.value = len(bigrams) / float(num_bigrams)
        result_set.append(result)

        # Unique tri
        result = FeatureResult("UniqueTrigramPct")
        result.value = len(trigrams) / float(num_trigrams)
        result_set.append(result)

        return result_set
