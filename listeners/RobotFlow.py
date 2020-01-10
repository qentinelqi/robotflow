#
#  Copyright 2020     Qentinel
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  pylint: disable=invalid-name
"""Robot Flow is a Robot Framework listener that controls RPA execution
   based on flow charts.
"""
import copy
import flow


class RobotFlow():
    """
    This is an example listener using just start_suite and end_suite
    to modify executed cases dynamically.

    Usage:
    robot --listener listeners\\LiveMod.py test\\t1.robot
    """

    ROBOT_LISTENER_API_VERSION = 3
    MOD = 0

    def __init__(self, mode=''):
        self.sourcefile = None
        self.ymlfile = None
        self.modifier = None
        if mode == 'verbose':
            self.verbose = True
        else:
            self.verbose = False

    def start_suite(self, data, result): # pylint: disable=unused-argument
        """Load flow chart and prepare RF to start from the first task.
        """
        # pylint: disable=attribute-defined-outside-init
        self.vprint("Running suite: {}".format(data))
        self.vprint("Sourcefile: {}".format(data.source))
        self.sourcefile = data.source
        self.flow = flow.Flow.from_graphml(data.source, self.verbose)

        # Copy available tests and clear the actual execution list
        self.orig_tests = copy.deepcopy(data.tests)
        data.tests.clear()

        # Append the first case to execution list
        next_test_case = self.flow.next()
        self.vprint('N: {}'.format(next_test_case))
        test_case = self.flow.str2test(next_test_case, self.orig_tests)
        self.vprint('TC: {}'.format(test_case))
        data.tests.append(test_case)

    def start_test(self, data, result):
        self.vprint("Start test")
        self.vprint("Running test: {}".format(data))
        self.vprint("Available tests: {}".format(data.parent.tests._items))

    def end_test(self, data, result): # pylint: disable=unused-argument
        """Set RF to execute next task.
        """
        next_test_case = self.flow.next()
        self.vprint("Next: {}".format(next_test_case))
        test_case = self.flow.str2test(next_test_case, self.orig_tests)
        if test_case is not None:
            data.parent.tests.append(test_case)

    def vprint(self, message):
        """Print message if verbose is set
        """
        if self.verbose:
            print(message)
