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

class PctLargeWords(LinguisticFeature):
    _short_name = "PctLargeWords"
    _long_name = "Percent Large Words"
    _description = "Percentage of words in the sample with " + \
                                           "at least 10 characters."

    def extract(self, sample):
        """ Calculate the number of large words divided by the number of words.
        sample -- Sample to extract from

        """
        result = FeatureResult(self._short_name)
        result.value = 0

        num_large_words = 0
        words = self._get_words(sample)
        for word in words :
            if len(word) >= 10 :
                num_large_words += 1

        result.value = float(num_large_words) / float(len(words))

        return [result]
