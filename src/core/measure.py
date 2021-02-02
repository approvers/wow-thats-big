import os
from typing import List, Optional

from src.core.type.argument import Argument
from src.core.type.big_file_property import BigFileProperty
from src.core.measurer.measurer_list import measurers


def measure(argument: Argument) -> Optional[List[BigFileProperty]]:
    if not os.path.isdir(argument.directory):
        return None

    return recursive_measure(argument, argument.directory, argument.directory)


def recursive_measure(argument: Argument, base_dir: str, current_directory: str) -> List[BigFileProperty]:
    children = [current_directory + os.sep + x for x in os.listdir(current_directory)]
    files = [x for x in children if os.path.isfile(x)]
    dirs = [x for x in children if os.path.isdir(x)]

    properties = []
    for file in files:
        partial_infos = [x.measure(file, argument) for x in measurers]
        non_filtered_infos = list(filter(lambda x: x is not None, partial_infos))
        if len(non_filtered_infos) > 0:
            properties.append(
                BigFileProperty(
                    file.removeprefix(base_dir),
                    non_filtered_infos
                )
            )

    for dir in dirs:
        properties += recursive_measure(argument, base_dir, dir)

    return properties
