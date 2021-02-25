import os
from typing import List, Optional, Dict

from src.type.argument_definition import ArgumentDefinition
from src.type.big_file_property import BigFileProperty
from src.measurer.measurer_list import measurers


def measure(directory: str, argument_table: Dict) -> Optional[List[BigFileProperty]]:
    if not os.path.isdir(directory):
        return None

    print(f"Scanning {directory}...")
    return recursive_measure(argument_table, directory, directory)


def recursive_measure(argument_table: Dict, base_dir: str, current_directory: str) -> List[BigFileProperty]:
    children = [current_directory + os.sep + x for x in os.listdir(current_directory)]
    files = [x for x in children if os.path.isfile(x)]
    dirs = [x for x in children if os.path.isdir(x)]
    properties = []

    for file in files:
        print(f"   {file}")
        partial_infos = []
        for measurer in measurers:
            print(f"      => {str(type(measurer))}")
            args = generate_argument(measurer.get_required_argument(), argument_table)
            partial_info = measurer.measure(file, args)
            if partial_info is not None:
                partial_infos.append(partial_info)

        if len(partial_infos) != 0:
            properties.append(
                BigFileProperty(
                    path=file,
                    info_list=partial_infos
                )
            )

    for dir in dirs:
        properties += recursive_measure(argument_table, base_dir, dir)

    return properties


def generate_argument(required_argument: List[ArgumentDefinition], argument_table: Dict):
    required_argument_table = {x.name: x for x in required_argument}
    provided_arg_names = set(argument_table.keys())
    missing_arg_names = required_argument_table.keys() - provided_arg_names

    default_provided_arg_names = {x.name for x in required_argument if x.default_value is not None}
    default_used_arg_names = set(filter(lambda x: x in default_provided_arg_names, missing_arg_names))
    no_value_arg_names = missing_arg_names - default_used_arg_names

    if len(no_value_arg_names) > 0:
        raise RuntimeError("Missing arguments: {}".format(", ".join(no_value_arg_names)))

    provided_arguments = {x: argument_table[x] for x in provided_arg_names if x in required_argument_table.keys()}
    default_arguments = {x: required_argument_table[x].default_value for x in default_used_arg_names}
    generated_argument = provided_arguments | default_arguments

    for arg in generated_argument.keys():
        provided_type = type(generated_argument[arg])
        required_type = required_argument_table[arg].arg_type
        if provided_type != required_type:
            raise TypeError(f"Type does not match to requirements: '{arg}' ({provided_type} != {required_type})")

    return generated_argument
