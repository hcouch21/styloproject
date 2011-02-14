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

from PlugInInterface import *

class FeatureExtractor(PlugIn, ExtractStart):
    def register(self, hooks):
        hooks[Hooks.EXTRACTSTART].append(self)

    def unregister(self, hooks):
        hooks[Hooks.EXTRACTSTART].remove(self)
    
    def run_extract_start_action(self, state, manager):
        print "Feature extraction started..."

        for feature in FeatureFactory.get_installed_features():
            print FeatureFactory.get_feature(feature).get_long_name()