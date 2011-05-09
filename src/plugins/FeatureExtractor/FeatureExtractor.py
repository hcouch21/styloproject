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

from plugins.FeatureExtractor.FeatureFactory import *
from PlugInInterface import *

class FeatureExtractor(PlugIn, ExtractStart, ListFeatures):
    dependencies = None
    conflicts = None
    needs_vanilla_data = False
    modifies_data = True
    category = Categories.FEATUREEXTRACTION
    
    def register(self, events):
        """Set up callbacks for events we want to know about"""

        events[Events.EXTRACTSTART].append(self)
        events[Events.LISTFEATURES].append(self)

    def unregister(self, events):
        """Remove us from the list of callbacks"""
        
        events[Events.EXTRACTSTART].remove(self)
        events[Events.LISTFEATURES].remove(self)
    
    def run_extract_start_action(self, state, manager):
        """Called when Stylo is in the extraction stage

        state -- Current state of Stylo
        manager -- Plugin manager (used if we want to fire new events)

        """

        # If no features specified, use them all
        if state.features_to_extract is None:
            state.features_to_extract = []
            
            manager.fire_event(Events.LISTFEATURES,  state)
            for feature in state.available_features:
                state.features_to_extract.append(feature._short_name)

        state.extracted = []

        while len(state.to_extract) != 0:
            sample = state.to_extract.pop(0)
            sample.feature_results = {}
            
            for feature_name in state.features_to_extract:
                manager.fire_event(Events.FEATURESTART, state)

                state.current_feature = feature_name
                feature = FeatureFactory.get_feature(feature_name)

                for extracted_feature in feature.extract(sample) :
                    sample.feature_results[extracted_feature.name] = \
                                                             extracted_feature

                manager.fire_event(Events.FEATURESTOP, state)

            state.extracted.append(sample)

    def run_list_features_action(self, state, manager):
        """Called when Stylo is in the list feature stage

        state -- Current state of Stylo
        manager -- Plugin manager (used if we want to fire new events)

        """
        
        keep_features = []
        remove_features = []
        
        # If user set features, separate into yes and no groups
        if state.options.features:
            for feature_name in state.options.features.split(","):
                if feature_name.startswith("-"):
                    remove_features.append(feature_name[1:])
                else:
                    keep_features.append(feature_name)
        
        # Create available_features list if no other plugin has
        if state.available_features is None:
            state.available_features = []

        # Now get a list of features and figure out if we want them or not
        for name in FeatureFactory.get_installed_features():
            feature = FeatureFactory.get_feature(name)
            
            if name in remove_features:
                continue
            elif (len(keep_features) > 0) and (name in keep_features):
                state.available_features.append(feature)
            elif len(keep_features) == 0:
                state.available_features.append(feature)
