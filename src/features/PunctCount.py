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
        rVal = []

        sample_length = len(sample.plain_text)

        for key, value in self._punctuation.items():
#            val = round((float(sample.plain_text.count(value)) /
#                              sample_length) * 100, 2)
            result = FeatureResult(key)
            result.value = sample.plain_text.count(value)

            rVal.append(result)

        return rVal
