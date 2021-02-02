import math
import os
from typing import Union, TextIO, BinaryIO, Optional

from src.core.measurer.abst_measurer import AbstractMeasurer
from src.core.type.argument import Argument
from src.core.type.bigfileproperty import PartialBigFileProperty


class FileSizeMeasurer(AbstractMeasurer):
    def measure(self, full_path: str, argument: Argument) -> Optional[PartialBigFileProperty]:
        size = os.path.getsize(full_path)
        if size > argument.min_file_size_kb * 1024:
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
