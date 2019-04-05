# Copyright 2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ros2cli.node.strategy import add_arguments
from ros2cli.node.strategy import NodeStrategy
from ros2component.api import get_container_node_names
from ros2component.api import get_components_in_container
from ros2component.api import container_node_name_completer
from ros2node.verb import VerbExtension


class ListVerb(VerbExtension):
    """Output a list of available containers and components."""

    def add_arguments(self, parser, cli_name):
        add_arguments(parser)
        argument = parser.add_argument(
            'container_node_name', nargs='?', default=None,
            help='Optional Display all nodes even hidden ones')
        argument.completer = container_node_name_completer
        parser.add_argument(
            '--containers-only', action='store_true',
            help='Only display the number of nodes discovered')

    def main(self, *, args):
        with NodeStrategy(args) as node:
            if args.container_node_name is not None:
                container_node_names = get_container_node_names(node=node)

                if args.container_node_name not in 
                container_node_names = [
                    n for n in container_node_names if n.full_name == args.container_node_name
                ]
                if not any(container_node_names):
                    return "Unable to find container node '" + args.container_node_name + "'"
            else:
                get_components_in_container()
            for container_node_name in container_node_names:
                print(container_node_name.full_name)
                if not args.containers_only:
                    components = get_container_components(
                        node=node, remote_container_node_name=container_node_name)
                    print('  Components:')
                    print(*[
                        2 * '  ' + '{}  {}'.format(c.uid, c.full_name) for c in components
                    ], sep='\n')
