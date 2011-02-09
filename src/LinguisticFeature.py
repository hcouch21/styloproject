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
