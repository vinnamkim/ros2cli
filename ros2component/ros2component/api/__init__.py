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

from collections import namedtuple

from rclpy.node import HIDDEN_NODE_PREFIX
from ros2cli.node.strategy import NodeStrategy

NodeName = namedtuple('NodeName', ('name', 'namespace', 'full_name'))
TopicInfo = namedtuple('Topic', ('name', 'types'))

COMPONENTS_RESOURCE_TYPE = 'rclcpp_components'


def get_package_components(*, package_name=None):
    if not has_resource(COMPONENTS_RESOURCE_TYPE, package_name):
        return []
    component_registry, _ = get_resource(COMPONENTS_RESOURCE_TYPE, package_name)
    return [line.split(';')[0] for line in component_registry]


def get_available_components():
    components = {}
    component_registries = get_resources(COMPONENTS_RESOURCE_TYPE)
    for package_name, path_to_component_registry in component_registries.items():
        with open(path_to_component_registry, 'r') as f:
            components[package_name] = [line.split(';')[0] for line in f]
    return components


def get_container_components(*, node, remote_node_name):
    list_nodes_client = node.create_client(
        composition_interfaces.srv.ListNodes, '{}/_container/list_nodes'.format(

        )
    )


def get_running_components(*, node):
    list_nodes_client = node.create_client(
        composition_interfaces.srv.ListNodes, '{}/_container/list_nodes'.format(

        )
    )


def get_container_node_names(*, node):
    container_node_names = []
    node_names = get_node_names(node=node, include_hidden_nodes=True)
    for n in node_names:
        services = get_service_info(node=node, remote_node_name=n.full_name)
        if not any(s.name.endswith('_container/load_node') and s.types == '' for s in services):
            continue
        if not any(s.name.endswith('_container/unload_node') and s.types == '' for s in services):
            continue
        if not any(s.name.endswith('_container/list_nodes') and s.types == '' for s in services):
            continue
        container_node_names.append(n)
    return container_node_names


def container_node_name_completer(prefix, parsed_args, **kwargs):
    with NodeStrategy(parsed_args) as node:
        return [
            n.full_name for n in get_container_node_names(node=node)
        ]


class ComponentPluginNameCompleter:
    """Callable returning a list of container node names."""

    def __init__(self, *, package_name_key=None):
        self.package_name_key = package_name_key

    def __call__(self, prefix, parsed_args, **kwargs):
        package_name = getattr(parsed_args, self.package_name_key)
        return get_package_components(package_name=package_name)
