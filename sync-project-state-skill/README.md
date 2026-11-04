# 跨设备项目状态同步 Skill

[English](README.en.md)

> 这是 Cliff-skill 集合中的模块副本。以下相对路径与命令均以 `sync-project-state-skill/` 为工作目录；历史来源见集合根目录的迁移清单。

`sync-project-state` 通过私有项目记忆索引、不可变检查点与环境要求，辅助 Git 项目的跨设备继续和交接。项目源码由各自仓库同步；本 Skill 记录恢复所需的非敏感控制信息。

它不会迁移 Codex 侧栏、对话历史、认证、浏览器状态或完整机器环境，也不能把未提交/未推送的工作变成可恢复状态。

## 行为

- `start`：快进同步记忆仓库；获取项目更新；只在工作区干净且严格落后时快进。
- `finish`：记录本轮结果、准确下一步、测试与阻塞；追加检查点。
- `register`：声明项目必需的 Skill、插件等环境要求。
- `bootstrap` / `install-skills`：检查环境、安装缺失的仓库内 Skill；不同版本的替换需显式授权并备份。

分叉历史不得自动合并。阻塞与警告应在继续工作前明确报告；缺失插件或权限不能被“恢复成功”掩盖。

## 使用

需要 Python 3.11+、Git，以及已授权的项目/记忆远端。记忆目录使用 `CODEX_MEMORY_HOME`，或由 `memory-config.json` / 本地指针发现。先阅读 [SKILL.md](SKILL.md)。

在本仓库根目录：

```bash
python scripts/project_memory.py --json start /absolute/path/to/project
python scripts/project_memory.py register /absolute/path/to/project --require-skill agentic-project-development
python scripts/project_memory.py finish /absolute/path/to/project --summary "Completed work" --next-action "Exact next step" --test "Command and result" --push-memory
```

`--push-memory` 会提交并推送记忆仓库，应在已授权且认证可用时使用。先确认项目代码已提交并推送；否则检查点必须明确不可移植。

## 数据与验证

状态契约见 [state-contract.md](references/state-contract.md)，已有测试见 [test_project_memory.py](scripts/test_project_memory.py)。检查点只追加，不重写历史来掩盖并发差异。

不要把认证文件、密钥、原始会话、数据库、浏览器资料或未经许可的公司/客户数据放进记忆仓库。文件存在与环境匹配只能支持限定范围的恢复声明；完整跨设备验收仍需在目标设备实际执行。

将本仓库含 `SKILL.md` 的目录安装到宿主支持的 Skill 位置即可调用 `$sync-project-state`。本仓库当前未提供顶层 `LICENSE`。
