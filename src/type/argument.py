import dataclasses


@dataclasses.dataclass
class Argument:
    """
    プログラム実行時に渡された引数。

    Attributes:
        min_file_size_kb:   "おっきぃ"と判定するまでのファイルサイズ。
        min_line:           "おっきぃ"と判定するまでのテキストファイル内の行数。
        directory:          判定対象のディレクトリ。
    """

    min_file_size_kb: int
    min_line: int
    directory: str
