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

class PunctCount(LinguisticFeature):
    _short_name = "PunctCount"
    _long_name = "Punctuation Count"
    _description = "Number of each type of punctuation in the sample."

    _punctuation = {
        "PunctCountPeriod" : ".",
        "PunctCountComma" : ",",
        "PunctCountExclamation" : "!",
        "PunctCountQuestion" : "?",
        "PunctCountSemicolon" : ";",
    }

    def extract(self, sample):
        """ Calculate the number of each type of punctuation in the sample
        sample -- Sample to analyze

        """
        rVal = []

        sample_length = len(sample.plain_text)

        # Count each punctuation separately
        for key, value in self._punctuation.items():
            result = FeatureResult(key)
            result.value = len([x for x in sample.nltk_text if x == value])

            rVal.append(result)

        return rVal
