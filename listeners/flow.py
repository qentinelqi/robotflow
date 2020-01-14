#
#  Copyright 2019     Qentinel
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
"""Flow is a graphml parser for RobotFlow.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
from robot.libraries.BuiltIn import BuiltIn


class Flow():
    """ Custom class for flow control """

    def __init__(self, graph, initial=None, verbose=False):
        self.verbose = verbose
        self.graph = graph
        if initial:
            self.initial = initial
        else:
            self.initial = self.parse_initial()
        self._state = None
        self.running = False

    @classmethod
    def from_graphml(cls, script_file, verbose=False):
        """Parse grapml.
        """
        graph_file = script_file.split(".")[0] + ".graphml"
        if verbose:
            print("Script file: {}".format(script_file))
            print("GraphML file: {}".format(graph_file))
        if not Path(graph_file).exists():
            raise FileNotFoundError("File not found: {}".format(graph_file))

        tree = ET.parse(str(graph_file))
        root = tree.getroot()

        id2node = {}
        nodes = {}
        for item in root.iter('{http://graphml.graphdrawing.org/xmlns}node'):
            attrib_id = item.attrib["id"]
            for label in item.iter('{http://www.yworks.com/xml/graphml}GenericNode'):
                attrib_type = label.attrib["configuration"]
            for label in item.iter('{http://www.yworks.com/xml/graphml}NodeLabel'):
                label = label.text
            nodes[label] = {}
            nodes[label]["id"] = attrib_id
            nodes[label]["type"] = attrib_type
            nodes[label]["target"] = None
            id2node[attrib_id] = label

        if verbose:
            print(nodes)
            print(id2node)

        for item in root.iter('{http://graphml.graphdrawing.org/xmlns}edge'):
            source = id2node[item.attrib["source"]]
            target = id2node[item.attrib["target"]]
            if verbose:
                print(source + ":" + target)
            target_label = None
            for label in item.iter('{http://www.yworks.com/xml/graphml}EdgeLabel'):
                target_label = label.text
            if not nodes[source]["target"]:
                nodes[source]["target"] = [(target, target_label)]
            else:
                # multiple targets
                nodes[source]["target"].append((target, target_label))
        return cls(nodes, verbose=verbose)

    def parse_initial(self):
        """Parse initial node from graph xml.
        """
        for item in self.graph:
            found = False
            for i in self.graph:
                if self.graph[i]["target"]:
                    if item in self.graph[i]["target"][0]:
                        found = True
            if not found:
                if self.verbose:
                    print("found initial: {}".format(item))
                return item
        return None

    def next(self):
        """Return next task.
        """
        if not self.running:
            self._state = self.initial
            self.running = True
            return self._state
        if not self._state:
            # has reached the end
            return None
        new = self.graph[self._state]["target"]
        if new is None:
            return None
        len_new = len(new)
        if len_new == 0:
            # last state, no new tasks
            self._state = None
        elif len_new == 1:
            # one path to next task
            new = self.graph[self._state]["target"]
            self._state = new[0][0]
        else:
            # choose next task by label
            target_dict = dict()
            for item in new:
                if item[1] in target_dict.keys():
                    raise ValueError('Task has duplicate exit points: {}'
                                     .format(item[1]))
                target_dict[item[1]] = item[0]
            if self.verbose:
                print('Target: {}'.format(target_dict))
            output = BuiltIn().get_variable_value("${OUTPUT}")
            new_target = target_dict[output]
            self._state = new_target
        return self._state

    def _validate_cond(self, cond):
        # pylint: disable=no-self-use
        """ Validate allowed strings to be passed for evaluation """
        if cond.lower() not in ["true", "false"]:
            raise NotImplementedError("only true or false are accepted as conditions")

    def str2test(self, testname, tests):
        # pylint: disable=no-self-use
        """ Return test case object """
        for test in tests:
            if testname == test.name:
                return test
        return None
