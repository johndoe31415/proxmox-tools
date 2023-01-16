#	proxmox-tools - Tools to aid management of a Proxmox setup
#	Copyright (C) 2022-2023 Johannes Bauer
#
#	This file is part of proxmox-tools.
#
#	proxmox-tools is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	proxmox-tools is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with proxmox-tools; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import os
import re

class PVEConfig():
	_MULTICOMMAND_KEYS = re.compile(r"(net\d+|meta|smbios\d+|scsi\d+|sata\d+)")

	def __init__(self, config_data):
		self._config_data = config_data

	@property
	def name(self):
		return self._config_data["name"]

	@property
	def mac(self):
		net = self._config_data["net0"]
		for key in [ "e1000", "virtio" ]:
			if key in net:
				return net[key].lower()
		else:
			raise Exception(f"Cannot determine MAC address: {net}")

	@classmethod
	def load_from_file(cls, filename):
		config_data = { }
		with open(filename) as f:
			for line in f:
				(key, value) = line.rstrip("\n").split(": ", maxsplit = 1)
				if cls._MULTICOMMAND_KEYS.fullmatch(key):
					value = cls._parse_multivalue(value)
				config_data[key] = value
		return cls(config_data)

	@classmethod
	def _parse_multivalue(cls, text):
		result = { }
		text = text.split(",")
		for keyvalue in text:
			keyvalue = keyvalue.split("=", maxsplit = 1)
			if len(keyvalue) == 2:
				(key, value) = keyvalue
			else:
				(key, value) = (keyvalue[0], None)
			result[key] = value
		return result


class PVEConfigs():
	def __init__(self, dirname = "/etc/pve/nodes"):
		self._configs = { }
		for (basedir, subdirs, files) in os.walk(dirname):
			for filename in files:
				if filename.endswith(".conf"):
					full_filename = basedir + "/" + filename
					self._configs[full_filename] = PVEConfig.load_from_file(full_filename)

		self._by_name = { config.name: config for config in self._configs.values() }

	def __getitem__(self, name):
		return self._by_name[name]

	def __iter__(self):
		return iter(self._by_name)

if __name__ == "__main__":
	pve = PVEConfigs()
	print(pve["win10-3"].mac)
