# Cliff-skill

集中整理 222222222l 账号下以 Skill 为主体、迁移核验时 star 为 0 的公开仓库。各目录保存原仓库默认分支的当前文件快照。

## Skill 导航

| 原仓库 / 目录 | Skill 入口 | 文件数 | 来源提交（main） | star |
| --- | --- | ---: | --- | ---: |
| [market-signal-analysis-skill](market-signal-analysis-skill/) | [SKILL.md](market-signal-analysis-skill/SKILL.md) | 30 | [bd07ba5f41c7](https://github.com/222222222l/market-signal-analysis-skill/commit/bd07ba5f41c717073e523a2be55b967c21a6b02f) | 0 |
| [China-policy-analysis-skill](China-policy-analysis-skill/) | [SKILL.md](China-policy-analysis-skill/SKILL.md) | 5 | [436d2c325bc3](https://github.com/222222222l/China-policy-analysis-skill/commit/436d2c325bc3eba13788f45627fa277f96922e6f) | 0 |
| [Agent-Evaluation-Skill](Agent-Evaluation-Skill/) | [SKILL.md](Agent-Evaluation-Skill/agent-evaluation/SKILL.md) | 11 | [53948d49f5c9](https://github.com/222222222l/Agent-Evaluation-Skill/commit/53948d49f5c994fe750ad324d16157f5d4d238d6) | 0 |
| [AI-infra-optimize-skill](AI-infra-optimize-skill/) | [SKILL.md](AI-infra-optimize-skill/optimize-ai-infra/SKILL.md) | 10 | [f2c7804c91ff](https://github.com/222222222l/AI-infra-optimize-skill/commit/f2c7804c91ff1b08b77d4fe0bef4e7288ffdf41c) | 0 |
| [sync-project-state-skill](sync-project-state-skill/) | [SKILL.md](sync-project-state-skill/SKILL.md) | 6 | [405dc5c7fd68](https://github.com/222222222l/sync-project-state-skill/commit/405dc5c7fd6829fa18ad9e7de4c87215a8016252) | 0 |
| [model-causes-and-decisions-skill](model-causes-and-decisions-skill/) | [SKILL.md](model-causes-and-decisions-skill/model-causes-and-decisions/SKILL.md) | 5 | [0d123e500849](https://github.com/222222222l/model-causes-and-decisions-skill/commit/0d123e500849d3cb3296da512e410908e2064e0b) | 0 |

## 使用与目录结构

每个一级目录对应一个原仓库，内部层级保持原样。安装时按表中的 Skill 入口找到其所在目录，再遵循原文档进行配置；整个合集根目录并非单个 Skill。

保留来源中的文档、脚本、署名和已有许可证文件。没有另行添加统一许可证；未提供许可证的来源，其授权状态仍以原仓库和作者说明为准。

## 迁移记录

- 迁移时间（UTC）：`2026-10-17T15:16:39.449226+00:00`。
- 本次六个来源均公开，因此本仓库设为公开。没有导入私有仓库文件。
- 仅导入当前文件快照，不复制提交历史、嵌套 `.git` 或本机凭证。
- 原仓库不删除、不归档、不修改；本仓库不会自动跟踪来源更新。
- 导入的脚本和工作流均未执行。
- 完整来源链接、分支、SHA、star、文件模式与逐文件 SHA-256 / Git blob SHA 见 [迁移清单](MIGRATION-MANIFEST.json)。

## 筛选范围

检查了账号全部自有仓库的可见性、star、默认分支文件树及可用 README。只纳入 Skill 本身为主要交付物且 star 为 0 的仓库。名称不含 skill 的项目也已检查。

`Agentic-Project-Development` 为 Skill 主体仓库，但核验时有 5 star，排除；`Deepseek-persona-card` 有 2 star，同样排除。`Agent-Session-Manager`、`Terrarium-cliff`、`dsh-omni-automation` 等属于应用、框架或工具项目，不因附带 Skill 而整仓纳入。私有应用、游戏、训练和项目状态库亦未纳入；不在公开清单披露其内容和名称。

公开仓库排除清单：

| 仓库 | star | 排除原因 |
| --- | ---: | --- |
| [Agent-Session-Manager](https://github.com/222222222l/Agent-Session-Manager) | 0 | 普通应用、框架、插件或训练项目，非 Skill 主体仓库 |
| [Agentic-Project-Development](https://github.com/222222222l/Agentic-Project-Development) | 5 | star 不为 0 |
| [Akari-Bot](https://github.com/222222222l/Akari-Bot) | 0 | 普通应用、框架、插件或训练项目，非 Skill 主体仓库 |
| [ASA-Benchmark](https://github.com/222222222l/ASA-Benchmark) | 1 | star 不为 0 |
| [Comfyui-Cliff-nodes](https://github.com/222222222l/Comfyui-Cliff-nodes) | 1 | star 不为 0 |
| [ComfyUI-DshModel](https://github.com/222222222l/ComfyUI-DshModel) | 1 | star 不为 0 |
| [ComfyUI-Falcon-Perception](https://github.com/222222222l/ComfyUI-Falcon-Perception) | 0 | 普通应用、框架、插件或训练项目，非 Skill 主体仓库 |
| [comfyui-kaloscope](https://github.com/222222222l/comfyui-kaloscope) | 0 | 普通应用、框架、插件或训练项目，非 Skill 主体仓库 |
| [comfyui-krea2edit](https://github.com/222222222l/comfyui-krea2edit) | 0 | 普通应用、框架、插件或训练项目，非 Skill 主体仓库 |
| [Deepseek-persona-card](https://github.com/222222222l/Deepseek-persona-card) | 2 | star 不为 0 |
| [DLSSNR-Potplayer-Plugin](https://github.com/222222222l/DLSSNR-Potplayer-Plugin) | 1 | star 不为 0 |
| [dsh-omni-automation](https://github.com/222222222l/dsh-omni-automation) | 0 | 普通应用、框架、插件或训练项目，非 Skill 主体仓库 |
| [Preferred-ip-generator](https://github.com/222222222l/Preferred-ip-generator) | 4 | star 不为 0 |
| [qwen-image-edit-trainer](https://github.com/222222222l/qwen-image-edit-trainer) | 0 | 普通应用、框架、插件或训练项目，非 Skill 主体仓库 |
| [Terrarium-cliff](https://github.com/222222222l/Terrarium-cliff) | 0 | 普通应用、框架、插件或训练项目，非 Skill 主体仓库 |

## 验证及限制

- 67 个导入文件均与固定来源提交的 Git blob 逐字节一致，文件清单无遗漏或额外内容。
- 已检查 Markdown 相对链接，未发现失效目标；保持各目录内部结构。
- 已静态检查常见密钥格式及敏感文件名，未发现发布阻断项。此检查不能证明不存在任何形式的秘密。
- 未运行来源脚本、功能测试或工作流；不声明运行时兼容性。外部链接和本机绝对路径不属于内部相对链接验证。
- 文件验证结果见 [验证记录](VALIDATION.json)。
