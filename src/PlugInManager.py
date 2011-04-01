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

import imp

from PlugInInterface import *

class PluginManager(object):
    _plug_ins = {}
    _hooks = {
        "StyloStart" : [],
        "StyloStop" : [],

        "ExtractStart" : [],
        "ExtractStop" : [],

        "FeatureStart" : [],
        "FeatureStop" : [],

        "ClassifyStart" : [],
        "ClassifyStop" : [],

        "TrainStart" : [],
        "TrainStop" : [],

        "ListFeatures" : [],
    }
    
    def load_plugin(self, name):
        """Loads a plugin and registers it with a call to register

        name -- Name of the plugin to load (module name as well as class name)

        """

        mod = None

        try:
            mod = imp.load_source(name, "plugins/%s/%s.py" % (name, name))
            pi = getattr(mod, name)()
            pi.register(self._hooks)
            self._plug_ins[name] = pi
        # Couldn't load the plugin, probably because of import error
        except Exception as e:
            print "Failed to load plugin %s." % name
            print e

    def load_plugins(self):
        pass

    def remove_plugin(self, plugin):
        """Removes the specified plugin from callback list

        plugin -- Plugin object to remove

        """
        pi = self._plug_ins[plugin]
        
        if pi is not None:
            pi.unregister(self._hooks)
            del self._plug_ins[plugin]
            del pi

    def fire_event(self, event, state):
        """Fires the given event for each plugin which needs it

        event -- The event to fire
        state -- RunState object about the current state of Stylo

        """
        for plugin in self._hooks[event]:
            event_action = getattr(plugin, Hooks.functions[event])
            event_action(state, self)

    def __str__(self):
        rVal = ""

        for k in self._hooks.keys():
            rVal += "%s:\n" % k

            count = 0
            for p in self._hooks[k]:
                rVal += "%d) %s\n" % (count, p.__class__.__name__)

            rVal += "\n"

        return rVal
