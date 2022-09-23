
import json
import os
from typing import get_type_hints

import mcdreforged.api.all as MCDR
from mcdreforged.utils.serializer import serialize, deserialize

from .storage import *

__all__ = [
	'JSONStorage'
]

class JSONStorage(Storage):
	__fields: dict

	def __init__(self, pluginid: str, name: str, auto_save: bool = False):
		super().__init__(pluginid, name)
		self._auto_save = auto_save

	def __init_subclass__(cls):
		fields = {}
		for name, typ in get_type_hints(cls).items():
			if not name.startswith('_'):
				assert isinstance(getattr(cls, name), typ)
				fields[name] = typ
		cls.__fields = fields

	@classmethod
	def get_fields(cls):
		return cls.__fields

	def on_init(self):
		self.load()

	def on_destory(self):
		self.save()

	@property
	def default_path(self):
		return os.path.join(get_config().storage, self.pluginid, f'{self.name}.json')

	@property
	def auto_save(self):
		return self._auto_save

	@auto_save.setter
	def auto_save(self, val: bool):
		self._auto_save = val

	def serialize(self) -> dict:
		return serialize(self)

	@classmethod
	def deserialize(cls, data: dict, **kwargs):
		assert isinstance(data, dict)
		return deserialize(data, cls, **kwargs)

	def update(self, data: dict):
		vars(self).update(self.__class__.deserialize(data))

	def load(self, *, path: str = None):
		if path is None:
			path = self.default_path
		if not os.path.exists(path):
			self.save(path=path)
			return
		data: dict
		with open(path, 'r') as fd:
			data = json.load(fd)
		self.update(data)

	def save(self, *, path: str = None):
		if path is None:
			path = self.default_path
		with open(path, 'w') as fd:
			json.dump(self.serialize(), fd)

	def __setattr__(self, name: str, val):
		typ = self.__class__.__fields.get(name, None)
		if typ is not None:
			assert isinstance(val, typ)
		super().__setattr__(name, val)
		if typ is not None and self._auto_save:
			self.save()
