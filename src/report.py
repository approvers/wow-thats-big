import os
import re
import unicodedata
from datetime import datetime
from typing import Optional, List

from src.type.big_file_property import BigFileProperty


def get_visible_length(string: str):
    count = 0
    for char in string:
        if unicodedata.east_asian_width(char) in "FWA":
            count += 2
        else:
            count += 1

    return count


def padding(base: str, length: int, character: str = " "):
    return f"{base}{character * (length - get_visible_length(base))}"


def normalize_path(path, root_dir):
    file_path = path.replace(root_dir, "", 1).replace(os.sep, "", 1)
    file_path = re.sub(f"\\{os.sep}+", os.sep, file_path)

    return file_path


def generate_tag(file_path, text, anchor=False):
    tag = "wow_thats_big_result_" + file_path.replace(os.sep, "_").replace(".", "_")
    if anchor:
        return f"<a id='{tag}'></a>\n{text}"

    return f"<a href='#{tag}'>{text}</a>"


def __generate_report_message(root_dir: str, property: Optional[List[BigFileProperty]]):
    if property is None:
        return "" \
               ":boom: 判定に失敗しました!! (おそらくバグです)\n" \
               "よろしければ、 https://github.com/approvers/wow-thats-big にバグを報告してください :pray:"

    if len(property) == 0:
        return ":raised_hands: おっきいファイルは見つかりませんでした!"

    report_text = "# すごい……おっきい……\n\n" \
                  f"{len(property)} 個のファイルに対して **すごい……おっきい……** と感じました。\n\n" \

    report_text += "## ファイル一覧\n"
    report_text += "\n".join(
        [f"- {generate_tag(x.path, f'`{normalize_path(x.path, root_dir)}`')}" for x in property]
    )

    report_text += "\n## 詳細\n<details>\n"
    for file in property:
        report_text += f"\n{generate_tag(file.path, f'### `{normalize_path(file.path, root_dir)}`', True)}\n"

        max_caption_len = max([get_visible_length(x.caption) for x in file.info_list])
        max_info_len = max([get_visible_length(x.info) for x in file.info_list])
        report_text += "" \
                       f"| {padding('項目', max_caption_len)} | {padding('内容', max_info_len)} |\n" \
                       f"|:{'-' * (max_caption_len + 1)}|:{'-' * (max_info_len + 1)}|\n"
        for info in file.info_list:
            report_text += f"| {padding(info.caption, max_caption_len)} | {padding(info.info, max_info_len)} |\n"

    report_text += "</details>\n\n"

    return report_text


def generate_report_message(root_dir: str, property: Optional[List[BigFileProperty]]):
    return "" \
           f"{ __generate_report_message(root_dir, property)}\n" \
           f"-----------------------\n" \
           f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')} に生成完了しました\n" \
           f"By: https://github.com/approvers/wow-thats-big"
