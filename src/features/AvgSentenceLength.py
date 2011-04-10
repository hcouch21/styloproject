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
import nltk

class AvgSentenceLength(LinguisticFeature):
    _short_name = "AvgSentenceLength"
    _long_name = "Average Sentence Length"
    _description = "Average length of sentences in the sample."

    def extract(self, sample):
        total_length = 0
        sentences = nltk.sent_tokenize(sample.plain_text)

        # Calculate the total number of words in each sentence
        for sentence in sentences :
            total_length += len(sentence.split())

        # Number of words / Number of sentences
        result = FeatureResult(self._short_name)
        result.value = float(total_length) / float(len(sentences))

        return [result]
