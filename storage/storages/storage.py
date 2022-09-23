
from abc import ABC, abstractmethod

import mcdreforged.api.all as MCDR

__all__ = [
	'Storage', 'Field'
]


class Storage(ABC):
	def __init__(self, pluginid: str, name: str):
		self.__pluginid = pluginid
		self.__name = name

	@property
	def pluginid(self):
		return self.__pluginid

	@property
	def name(self):
		return self.__name

	@abstractmethod
	def on_init(self):
		raise NotImplementedError()

	@abstractmethod
	def on_destory(self):
		raise NotImplementedError()

class DBStorage(Storage):
	def __init__(self, pluginid: str, name: str):
		super().__init__(pluginid, name)

	@property
	def table(self):
		return f'mcdr_{self.pluginid}_{self.name}'

	def on_init(self):
		self.on_connect()

	def on_destory(self):
		self.on_close()

	@abstractmethod
	def on_connect(self):
		raise NotImplementedError()

	@abstractmethod
	def on_close(self):
		raise NotImplementedError()

class Field(type):
	def __new__(cls, *args, **kwargs) -> type:
		return type.__new__(cls, '__FieldWrapper', (type, ), {})

	def __instancecheck__(self, instance):
		return isinstance(instance, self.__clazz)

	def __init__(self, name: str, clazz: type):
		self.__name = name
		assert clazz is not None and clazz is not type(None)
		self.__clazz = clazz

	@property
	def name(self) -> str:
		return self.__name

	@property
	def clazz(self) -> type:
		return self.__clazz

	def __str__(self) -> str:
		return 'FieldWrapper'

	def __repr__(self) -> str:
		return '<FieldWrapper name="{0}" type={1}>'.format(self.name, repr(self.clazz))
