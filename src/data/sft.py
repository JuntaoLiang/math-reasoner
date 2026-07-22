"""
SFT数据集加载模块
功能:读取JSON Lines(.jsonl)格式监督微调训练数据,完成数据校验并封装为结构化样本对象SFTItem

数据文件格式规范：
1. 文件为jsonl格式:每行一条独立JSON对象
2. 每条记录必须包含三个字段：
    id: str    样本唯一编号
    problem: str 用户输入Prompt/问题
    response: str 模型期望输出答案
3. 禁止空行、非法JSON、缺失字段、字段内容为空字符串

执行校验项：
✅ 文件存在性检查
✅ 跳过空行
✅ JSON语法合法性校验
✅ 强制每条记录为JSON对象(dict)
✅ 必填字段完整性校验
✅ id/problem/response非空校验
✅ 自动去除字段首尾空白字符

输出:"list[SFTItem]，供上游 build_sft_dataset 函数进行分词、构建HuggingFace Dataset
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SFTItem:
    id: str
    problem: str
    response: str


def load_sft_items(file_path: str | Path) -> list[SFTItem]:
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"SFT file not found: {path}")

    items: list[SFTItem] = []
    required_fields = {"id", "problem", "response"}

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: {error}"
                ) from error

            if not isinstance(record, dict):
                raise ValueError(
                    f"SFT record at line {line_number} must be a JSON object."
                )

            missing_fields = required_fields - record.keys()

            if missing_fields:
                missing_text = ", ".join(sorted(missing_fields))
                raise ValueError(
                    f"Missing required fields at line {line_number}: "
                    f"{missing_text}"
                )

            item = SFTItem(
                id=str(record["id"]).strip(),
                problem=str(record["problem"]).strip(),
                response=str(record["response"]).strip(),
            )

            if not item.id:
                raise ValueError(f"Empty id at line {line_number}.")

            if not item.problem:
                raise ValueError(f"Empty problem at line {line_number}.")

            if not item.response:
                raise ValueError(f"Empty response at line {line_number}.")

            items.append(item)

    if not items:
        raise ValueError(f"SFT file is empty: {path}")

    return items