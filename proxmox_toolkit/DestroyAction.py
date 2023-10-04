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

import subprocess
from .PVEConfig import PVEConfigs
from .BaseAction import BaseAction

class DestroyAction(BaseAction):
	def run(self):
		self._pveconfig = PVEConfigs()
		configs = list(self._pveconfig.select_by_name(self._args.pattern))

		if not self._args.no_confirmation:
			print(f"Remove {len(configs)} machines including their disk content:")
			for config in configs:
				print(f"    {config.name} (ID {config.mid})")
			yn = input("Proceed (y/n)? ")
			if yn.lower() != "y":
				print("Aborted.")
				return 1

		for config in configs:
			subprocess.check_call([ "qm", "destroy", str(config.mid) ])
