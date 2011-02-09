import imp

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
    }
    
    def load_plugin(self, name):
        mod = None

        try:
            mod = imp.load_source(name, "plugins/%s/%s.py" % (name, name))
            pi = getattr(mod, name)()
            pi.register(self._hooks)
            self._plug_ins[name] = pi
        except Exception as e:
            print "Failed to load plugin %s." % name

    def load_plugins(self):
        pass

    def remove_plugin(self, plugin):
        pi = self._plug_ins[plugin]
        
        if pi is not None:
            pi.unregister(self._hooks)
            del self._plug_ins[plugin]
            del pi

    def __str__(self):
        rVal = ""

        for k in self._hooks.keys():
            rVal += "%s:\n" % k

            count = 0
            for p in self._hooks[k]:
                rVal += "%d) %s\n" % (count, p.__class__.__name__)

            rVal += "\n"

        return rVal