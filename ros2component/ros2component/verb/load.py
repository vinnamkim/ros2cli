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
from ros2component.api import ComponentPluginNameCompleter
from ros2component.verb import VerbExtension

from ros2pkg.api import package_name_completer


class LoadVerb(VerbExtension):
    """Load a component into a container node."""

    def add_arguments(self, parser, cli_name):
        add_arguments(parser)
        argument = parser.add_argument(
            'container_node_name',
            help='Container node name to load component into')
        argument.completer = ContainerNodeNameCompleter()
        argument = parser.add_argument(
            'package_name',
            help='Package name of the plugin component to be loaded')
        argument.completer = package_name_completer
        argument = parser.add_argument(
            'plugin_name',
            help='Name of the plugin component to be loaded.'
        )
        argument.completer = ComponentNameCompleter()
        parser.add_argument(
            '--node-name', default='',
            help='Name of component node once loaded'
        )
        parser.add_argument(
            '--namespace-name', default='',
            help='Name of component node once loaded'
        )
        parser.add_argument(
            '--log-level', default='',
            help='Name of component node once loaded'
        )
        parser.add_argument(
            '--remap-rules', default='',
            help='Name of component node once loaded'
        )
        parser.add_argument(
            '--parameters', default='',
            help='Name of component node once loaded'
        )
        parser.add_argument(
            '--extra-arguments', default='',
            help='Name of component node once loaded'
        )

    def main(self, *, args):
        with NodeStrategy(args) as node:
            container_node_names = get_container_node_names(
                node=node, include_hidden_nodes=False)
            if args.container_node_name in [n.full_name for n in container_node_names]:
                with DirectNode(args) as node:
                    return load_component(
                        node=node, remote_container_node_name=args.container_node_name,
                    )
            else:
                return "Unable to find node '" + args.node_name + "'"
