import dataclasses
from typing import Dict, List, Tuple


@dataclasses.dataclass
class PartialBigFileProperty:
    """
    "すごいおっき"かったファイルの1つの情報。

    Attributes
    ----------
        caption:    情報の名前。
        info:       情報の内容。
    """
    caption: str
    info: str


@dataclasses.dataclass
class BigFileProperty:
    """
    "すごいおっき"かったファイルについての情報。

    Attributes
    ----------
        path:       ファイルのパス。
        file_size:   ファイルの大きさ [byte]。
        line_count:   [Optional; ファイルがバイナリの場合None] ファイルの行数。
    """
    path: str
    info_list: List[PartialBigFileProperty]

    @property
    def info(self) -> Tuple[Tuple[str, str]]:
        return tuple(((x.caption, x.info) for x in self.info_list))
