import math
import os
from typing import Optional, Dict, List

from src.measurer.abst_measurer import AbstractMeasurer
from src.type.argument_definition import ArgumentDefinition
from src.type.big_file_property import PartialBigFileProperty


class FileSizeMeasurer(AbstractMeasurer):
    MIN_FILE_SIZE_KB = "min_file_size_kb"

    def get_required_argument(self) -> List[ArgumentDefinition]:
        return [
            ArgumentDefinition(FileSizeMeasurer.MIN_FILE_SIZE_KB, int, 512)
        ]

    def measure(self, full_path: str, arguments: Dict) -> Optional[PartialBigFileProperty]:
        size = os.path.getsize(full_path)
        if size > arguments[FileSizeMeasurer.MIN_FILE_SIZE_KB] * 1024:
            return PartialBigFileProperty(
                caption="ファイルサイズ",
                info=get_human_readable_filesize(size)
            )
        return None


def get_human_readable_filesize(size_byte: int):
    if size_byte == 0:
        return "0 Bytes"
    unit = ("Bytes", "KB", "MB", "GB", "TB")
    unit_index = int(math.log(size_byte, 1024))
    numeric = round(size_byte / 1024 ** unit_index, 2)
    return f"{numeric} {unit[unit_index]}"
