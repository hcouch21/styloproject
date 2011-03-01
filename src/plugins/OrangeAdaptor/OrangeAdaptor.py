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

import os
import sys

from Domain import FeatureResult
from PlugInInterface import *

try:
    import orange
except:
    print "Could not import Orange!"
    sys.exit(1)

class OrangeAdaptor(PlugIn, ClassifyStart, TrainStart):
    def register(self, hooks):
        hooks[Hooks.CLASSIFYSTART].append(self)
        hooks[Hooks.TRAINSTART].append(self)

    def unregister(self, hooks):
        hooks[Hooks.CLASSIFYSTART].remove(self)
        hooks[Hooks.TRAINSTART].append(self)

    def run_classify_start_action(self, state, manager):
        train_data = orange.ExampleTable(state.corpus.path + "stylo/training.tab")
        classifier = orange.BayesLearner(train_data)

        header_complete = False
        header_line = "Author\t"
        type_line = "discrete\t"
        special_line = "class\t"
        data = ""
        for sample in state.extracted:
            data += "\t"
            for feature_result in sample.feature_results:
                if not header_complete:
                    header_line += "%s\t" % feature_result.name
                    type_line += "discrete\t"
                    special_line += "\t"

                data += "%s\t" % feature_result.value

                # Set weights
                feature_result.weight = orange.MeasureAttribute_relevance(feature_result.name, train_data)

            header_complete = True
            data += "\n"

        with open("classify_data.tab", "w") as f:
            f.write("%s\n" % header_line)
            f.write("%s\n" % type_line)
            f.write("%s\n" % special_line)
            f.write("%s" % data)

        class_data = orange.ExampleTable("classify_data.tab")
        os.remove("classify_data.tab")

        count = 0
        for example in class_data:
            author_result = FeatureResult("Author")
            author_result.value = classifier(example).value
            author_result.weight = max(classifier(example, orange.GetProbabilities))
            state.extracted[count].feature_results.insert(0, author_result)
            count += 1

    def run_train_start_action(self, state, manager):
        if state.training is None or state.training != True:
            print "Error: Not a training state object"
            sys.exit(1)

        data = ""
        for author in state.corpus.authors:
            state.to_extract = author.samples

            manager.fire_event(Hooks.EXTRACTSTART, state)

            for sample in state.extracted:
                data += "%s\t" % author.name
                for feat_res in sample.feature_results:
                    data += "%s\t" % feat_res.value

                data += "\n"

            header_line = "Author\t"
            type_line = "discrete\t"
            special_line = "class\t"

            for feature_result in state.extracted[0].feature_results:
                header_line += "%s\t" % feature_result.name
                type_line += "discrete\t"
                special_line += "\t"

        with open(state.corpus.path + "stylo/training.tab", "w") as f:
            f.write("%s\n" % header_line)
            f.write("%s\n" % type_line)
            f.write("%s\n" % special_line)
            f.write("%s" % data)