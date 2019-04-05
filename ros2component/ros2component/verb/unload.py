# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from ros2component.api import ContainerNodeNameCompleter
from ros2component.verb import VerbExtension


class UnloadVerb(VerbExtension):
    """Unload a component into a container node."""

    def add_arguments(self, parser, cli_name):
        add_arguments(parser)
        argument = parser.add_argument(
            'container_node_name',
            help='Container node name to load component into')
        argument.completer = ContainerNodeNameCompleter()
        argument = parser.add_argument(
            'component', type=int, nargs='+', dest='components',
            help='Package name of the plugin component to be loaded')

    def main(self, *, args):
        with NodeStrategy(args) as node:
            container_node_names = get_container_node_names(node=node, include_hidden_nodes=False)
            if args.container_node_name in [n.full_name for n in container_node_names]:
                return unload_component(
                    node=node, remote_container_node_name=args.container_node_name,
                    components=args.components
                )
            else:
                return "Unable to find container node '" + args.container_node_name + "'"
