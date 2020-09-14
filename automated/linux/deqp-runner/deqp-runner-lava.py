#!/usr/bin/env python3

#
# LAVA/OE deqp-runner results parse script
#
# Copyright (C) 2020, Linaro Limited.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import re
import subprocess
import sys

lava_results = ['pass', 'skip', 'fail', 'unknown']
result_replaces = {
    'Crash': 'fail',
    'ExpectedFail': 'pass',
    'Flake': 'fail',
    'UnexpectedPass': 'fail',
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s <result_file>" % sys.argv[0])
        sys.exit(1)

    rex = re.compile("(?P<test_case_id>.*),(?P<result>.*)$")
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            m = rex.search(line)
            if m:
                test_case = m.group('test_case_id')

                result = m.group('result').lower()
                for r in result_replaces.keys():
                    result = result.replace(r, result_replaces[r])
                result = result.lower()
                if result not in lava_results:
                    result = 'unknown'

                subprocess.check_call("lava-test-case \"%s\" --result \"%s\"" %
                                      (test_case, result), shell=True)
