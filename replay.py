#!/usr/bin/env python
#
# Copyright 2012-2014 ihptru (Igor Popov)
#
# This file is part of OpenRA-Replay-Parser, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys

# script works since OpenRA version 2012-0315
# script takes path to .rep file as an argument

try:
    replay_path = sys.argv[1]
except Exception as e:
    print("Requires a path to .rep file")
    exit()

Data = open(replay_path).read(3000000)

if len(re.findall('StartGame', Data)) == 0:
    print("could not detect the moment of the game starting... exit")
    exit(3)

Data = Data.split('StartGame')[0]

# server's info
global_s = Data.split('GlobalSettings:')[-1]

server_name = re.findall('ServerName: (.*)', global_s)[0].replace("'", "\\'")
maphash = re.findall('Map: (.*)', global_s)[0]
mods = re.findall('Mods: (.*)', global_s)[0]
version = re.findall('\tMods: (.*)', Data.split('Handshake:')[1].split('Response')[0])[0].split('@')[1]

title = os.path.basename(replay_path)

print("Filename: " + title)
print("Version: " + version)
print("Server name: " + server_name)
print("Hash of played map: " + maphash)
print("Game Mods: " + mods)

# last clients
clients = Data.split('GlobalSettings')[-2].split('Client@', 1)[1]

client_names = re.findall('\tName: (.*)', clients)
client_colorramps = re.findall('\tColor: (.*)', clients)
client_countries = re.findall('\tCountry: (.*)', clients)
client_teams = re.findall('\tTeam: (.*)', clients)
print("Clients:")

for i in range(len(client_names)):
    print("------------------------")
    print("  Name: " + client_names[i].replace("'", "\\'"))
    print("  Color: " + client_colorramps[i])
    print("  Country: " + client_countries[i])
    print("  Team: " + client_teams[i])
print("------------------------")
exit(0)
