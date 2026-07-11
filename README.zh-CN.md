# seer-export-audit（中文说明）

面向登记数据库导出表及其数据字典的轻量质量控制工具。它不读取 SEER 数据库，不上传数据，也不替代官方变量说明。

工具可检查：列名为空或重复、行列数不一致、各变量缺失率，以及导出表与数据字典之间的字段不匹配；随后生成 JSON 审计结果和 Markdown 审阅报告。

适用于 SEER*Stat 工作流中的“导出后、统计前”核对环节，也可用于任何带表头的分隔文本文件。

## 使用

```bash
python -m pip install -e .
seer-export-audit audit \
  --data examples/synthetic_export.txt \
  --dictionary examples/synthetic_dictionary.dic \
  --output reports/example
```

## 数据安全

仓库仅含合成示例。禁止提交患者级数据、受限登记数据、真实导出文件、稿件或机构文件。真实研究文件应放在已被 `.gitignore` 排除的 `data/` 目录中；详情见 [NOTICE.md](NOTICE.md)。

## 数据字典格式

使用 UTF-8 编码的逗号、制表符、竖线或分号分隔文件。首行必须有 `variable`；可选列为 `label`、`type`、`allowed_values`。

### 重要说明：原生 `.dic` 文件

本工具**不能直接解析所有**原生或厂商特有的 SEER*Stat `.dic` 文件。审计前，请先将需要核对的字段定义导出或转换为下述通用分隔文本格式；转换文件首行必须包含 `variable`，分隔符可为逗号、制表符、竖线或分号。本限制是有意保留的，以确保审计输入格式透明、可复核。

```text
variable|label|type|allowed_values
diagnosis_year|诊断年份|integer|2000-2026
```

本项目不声称能解析所有厂商特有的字典格式；它采用可审核的通用交换格式。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

本项目与 NCI、SEER 和 SEER*Stat 无隶属关系。
