#    This file is part of Stylo.
#
#    Stylo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Stylo.  If not, see <http://www.gnu.org/licenses/>.

from LinguisticFeature import *

class PunctCount(LinguisticFeature):
    _short_name = "PunctCount"
    _long_name = "Punctuation Count"
    _description = "Number of each type of punctuation in the sample."

    _plain_text = False

    __punctuation__ = {
        "PunctPeriod" : ".",
        "PunctComma" : ",",
        "PunctExclamation" : "!",
        "PunctQuestion" : "?",
    }

    def extract(self, sample):
        rVal = {}

        sample_length = len(sample)

        for key, value in __punctuation__.items():
            rVal[key] = round((float(sample.count(value)) / 
                              sample_length) * 100, 2)

        return rVal
