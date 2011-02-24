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

class PlugIn(object):
    def register(self, hooks):
        raise NotImplementedError()

    def unregister(self, hooks):
        raise NotImplementedError()

class StyloStart(object):
    def run_stylo_start_action(self, state, manager):
        raise NotImplementedError()

class StyloStop(object):
    def run_stylo_stop_action(self, state, manager):
        raise NotImplementedError()

class ExtractStart(object):
    def run_extract_start_action(self, state, manager):
        raise NotImplementedError()

class ExtractStop(object):
    def run_extract_stop_action(self, state, manager):
        raise NotImplementedError()

class FeatureStart(object):
    def run_feature_start_action(self, state, feature):
        raise NotImplementedError()

class FeatureStop(object):
    def run_feature_stop_action(self, state, manager):
        raise NotImplementedError()

class ClassifyStart(object):
    def run_classify_start_action(self, state, manager):
        raise NotImplementedError()

class ClassifyStop(object):
    def run_classify_stop_action(self, state, manager):
        raise NotImplementedError()

class TrainStart(object):
    def run_train_start_action(self, state, manager):
        raise NotImplementedError()

class TrainStop(object):
    def run_train_stop_action(self, state, manager):
        raise NotImplementedError()

class ListFeatures(object):
    def run_list_features_action(self, state, manager):
        raise NotImplementedError()

class RunState(object):
    training = None

    corpus = None

    # Samples that still need extraction
    to_extract = None
    # Samples already extracted
    extracted = None

    # List of available features
    available_features = None
    # List of features to extract
    features_to_extract = None
    # The current feature we're extracting
    current_feature = None

class Hooks(object):
    STYLOSTART = "StyloStart"
    STYLOSTOP = "StyloStop"
    EXTRACTSTART = "ExtractStart"
    EXTRACTSTOP = "ExtractStop"
    FEATURESTART = "FeatureStart"
    FEATURESTOP = "FeatureStop"
    CLASSIFYSTART = "ClassifyStart"
    CLASSIFYSTOP = "ClassifyStop"
    TRAINSTART = "TrainStart"
    TRAINSTOP = "TrainStop"
    LISTFEATURES = "ListFeatures"

    functions = {
        EXTRACTSTART : "run_extract_start_action",
        TRAINSTART : "run_train_start_action",
        LISTFEATURES : "run_list_features_action",
    }