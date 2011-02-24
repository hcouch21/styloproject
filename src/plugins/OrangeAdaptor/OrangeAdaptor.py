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

import sys

from PlugInInterface import *

class OrangeAdaptor(PlugIn, ClassifyStart, TrainStart):
    def register(self, hooks):
        hooks[Hooks.CLASSIFYSTART].append(self)
        hooks[Hooks.TRAINSTART].append(self)

    def unregister(self, hooks):
        hooks[Hooks.CLASSIFYSTART].remove(self)
        hooks[Hooks.TRAINSTART].append(self)

    def run_classify_start_action(self, state, manager):
        print "Classification started..."

    def run_train_start_action(self, state, manager):
        if state.training is None or state.training != True:
            print "Error: Not a training state object"
            sys.exit(1)

        headers_written = False

        with open(state.corpus.path + "stylo/training.tab", "w") as f:
            for author in state.corpus.authors:
                state.to_extract = author.samples

                manager.fire_event(Hooks.EXTRACTSTART, state)

                if not headers_written:
                    header_line = "Author\t"
                    type_line = "discrete\t"
                    special_line = "class\t"

                    for feature_name in state.features_to_extract:
                        header_line += "%s\t" % feature_name
                        type_line += "discrete\t"
                        special_line += "\t"

                    f.write("%s\n" % header_line)
                    f.write("%s\n" % type_line)
                    f.write("%s\n" % special_line)

                    headers_written = True

                for sample in author.samples:
                    f.write("%s\t" % author.name)
                    for feat_res in sample.feature_results:
                        f.write("%s\t" % feat_res.value)

                    f.write("\n")