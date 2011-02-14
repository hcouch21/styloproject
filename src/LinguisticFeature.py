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

class LinguisticFeature(object):
    _short_name = ""
    _long_name = ""
    _description = ""

    _plain_text = False

    def extract(self, sample):
        raise NotImplementedError()

    def get_short_name(self):
        return self._short_name

    def get_long_name(self):
        return self._long_name

    def get_description(self):
        return self._description

    def is_plain_text(self):
        return self._plain_text
