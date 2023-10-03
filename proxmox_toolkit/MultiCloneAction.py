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
from .BaseAction import BaseAction
from .PVEConfig import PVEConfigs

class MultiCloneAction(BaseAction):
	def run(self):
		self._pveconfigs = PVEConfigs()
		max_id = max(pveconfig.mid for pveconfig in self._pveconfigs.values)
		for mach_no in range(1, self._args.count + 1):
			mach_name = f"{self._args.prefix}-{mach_no:02d}"
			new_mid = max_id + mach_no
			cmd = [ "qm", "clone", str(self._args.source_id), str(new_mid), "--name", mach_name ]
			if self._args.verbose >= 1:
				print(cmd)
			subprocess.check_call(cmd)
