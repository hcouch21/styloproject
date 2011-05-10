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

from nltk_contrib.readability import syllables_en

class AvgSyllables(LinguisticFeature):
    """ Feature that calculates the average number of syllables per word
        in the sample
    """
    _short_name = "AvgSyllables"
    _long_name = "Average Syllables"
    _description = "The average number of syllables per word."

    def extract(self, sample):
        result = FeatureResult(self._short_name)
        num_syllables = []
        
        words = self._get_words(sample)

        # Create a list of the number of syllables of each word
        for word in words :
            num_syllables.append(syllables_en.count(word))
        
        result.value = float(sum(num_syllables)) / float(len(words))

        return [result]
