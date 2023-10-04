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

import sys
from .MultiCommand import MultiCommand
from .DNSMasqConfigAction import DNSMasqConfigAction
from .StartStopAction import StartStopAction
from .DestroyAction import DestroyAction
from .MultiCloneAction import MultiCloneAction

def main():
	mc = MultiCommand(description = "Proxmox toolkit", run_method = True)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("pattern", metavar = "regex/filename", help = "Regex that describes machine names to use. Can be prefixed by '@' and then is interpreted as a file which contains all machine names.")
		parser.add_argument("start_ip", metavar = "ip", help = "IP address to assign to the first machine.")
	mc.register("dnsmasq", "Create a pseudo-static DNSmasq DHCP configuration from PVE machine name list and a starting IP.", genparser, action = DNSMasqConfigAction)

	def genparser(parser):
		parser.add_argument("-s", "--action-shutdown", action = "store_true", help = "Shutdown the machine(s) via ACPI.")
		parser.add_argument("-S", "--action-stop", action = "store_true", help = "Stop the machine(s).")
		parser.add_argument("-r", "--action-reboot", action = "store_true", help = "Reboot the machine(s) via ACPI.")
		parser.add_argument("-R", "--action-reset", action = "store_true", help = "Reboot the machine(s).")
		parser.add_argument("-t", "--action-start", action = "store_true", help = "Start the machine(s).")
		parser.add_argument("-g", "--gracetime", metavar = "secs", type = float, default = 15.0, help = "Time in seconds between consecutive start actions. Defaults to %(default).1f secs.")
		parser.add_argument("-y", "--no-confirmation", action = "store_true", help = "Do not ask for confirmation before commencing the requested actions.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("pattern", metavar = "regex/filename", help = "Regex that describes machine names to use. Can be prefixed by '@' and then is interpreted as a file which contains all machine names.")
	mc.register("startstop", "Start/stop/reboot multiple machines.", genparser, action = StartStopAction)

	def genparser(parser):
		parser.add_argument("-y", "--no-confirmation", action = "store_true", help = "Do not ask for confirmation before commencing the requested actions.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("pattern", metavar = "regex/filename", help = "Regex that describes machine names to use. Can be prefixed by '@' and then is interpreted as a file which contains all machine names.")
	mc.register("destroy", "Destroy multiple machines.", genparser, action = DestroyAction)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("source_id", type = int, help = "Machine ID to use as a clone source.")
		parser.add_argument("count", type = int, help = "Numer of clones to create.")
		parser.add_argument("prefix", help = "Clone name prefix.")
	mc.register("multiclone", "Clone a machine multiple times.", genparser, action = MultiCloneAction)

	returncode = mc.run(sys.argv[1:])
	sys.exit(returncode or 0)
