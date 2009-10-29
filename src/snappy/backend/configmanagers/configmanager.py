from UserDict import DictMixin
class ConfigDict(DictMixin, object):
	def __init__(self):
		super(ConfigDict, self).__init__()
		self.dict = dict()
	def __getitem__(self, key):
		self.dict.__getitem__(key)
	def __setitem__(self, key, value):
		self.dict.__setitem__(key, value)

class ConfigManager(object):
	def __init__(self):
		super(ConfigManager, self).__init__()
		from snappy.backend.urlproviders.trim import UrlProvider
		self.urlprovider = UrlProvider()
		self.settings = ConfigDict()

	def set_password(self, key, password):
		self.settings[key] = password

	def get_password(self, key):
		return self.settings[key]