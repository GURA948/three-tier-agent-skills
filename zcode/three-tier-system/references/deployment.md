# 部署与分发

仅在安装到另一台 ZCode、换机或大版本复检时读取。

## 1. 安装

| 部件 | 目标 | 要求 |
|---|---|---|
| 技能目录（含 `SKILL.md/references/profiles/tools`） | `~/.zcode/skills/three-tier-system/` | 必需，整目录复制 |
| 员工加载副本 | `~/.zcode/agents/employee.md` | 必需；由同步脚本生成，或按 `ui-setup.md` 手工创建 |
| 每任务指导文档 | 项目知识库、所有 worktree 外 | 按模板随任务生成，不随技能分发 |

安装顺序：

1. 复制整个技能目录。
2. 运行 `tools/sync-employee-profile.ps1 -Check`。
3. `MISSING` 时安装；`CONFLICT/DRIFT` 时先检查已有角色，确认替换后才用 `-Replace`（脚本会备份）。
4. 重启客户端/新开会话，使技能和角色重新加载。
5. 完成下方自检。

## 2. 机器特定值

- `profiles/employee.md` 默认不写 `model`；仅用户明确选择且端点已配置时添加，并重新同步。
- 项目约束由目标项目 `AGENTS.md` 提供。
- 指导文档必须放在所有参与者可访问、且位于源码 worktree 外的位置。

## 3. 安装验收

按顺序通过，证据使用目标机器的实际输出：

1. 新会话说“启动三级体系”可加载 `SKILL.md`。
2. profile 检查返回 `MATCH`，且不静默覆盖既有角色；`Agent(subagent_type:"employee", run_in_background:true)` 成功。角色不可用时验证 `general-purpose` + 正式合同/任务包的退化路径。
3. 单写场景：员工只能修改获授范围，形成固定 candidate 后停止，由经理独立验收。
4. 多写场景：写集合重叠时拒绝第二写入者；设备、依赖/缓存和集成槽单持有；验收队列满时背压。
5. 恢复场景：父会话终止后，新会话从指导文档、worktree、提交和进程恢复，不向旧 agentId 续派，不清理未知结果。

## 4. 分发边界

`profiles/employee.md` 是合同维护源，`~/.zcode/agents/employee.md` 是本机加载副本，`employee-brief.md` 只存创建方式和任务包。任务指导文档、个人模型设置、运行日志和本机角色副本不随技能包分发。
