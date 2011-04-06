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

class PctPunctuation(LinguisticFeature):
    _short_name = "PctPunctuation"
    _long_name = "Punctuation Percentage"
    _description = "Percentage of each type of punctuation in the sample."

    _punctuation = {
        "PctPunctPeriod" : ".",
        "PctPunctComma" : ",",
        "PctPunctExclamation" : "!",
        "PctPunctQuestion" : "?",
        "PctPunctSemicolon" : ";",
    }

    def extract(self, sample):
        rVal = []

        sample_length = len(sample.plain_text)

        for key, value in self._punctuation.items():
            val = round((float(len([x for x in sample.nltk_text
                                    if x == value])) / sample_length) * 100, 2)
            result = FeatureResult(key)
            result.value = val

            rVal.append(result)

        return rVal
