# 员工档案与 UI 字段

`profiles/employee.md` 是唯一合同维护源。优先用文件同步；只有缺少文件或界面已有需保留的同名角色时才逐字段配置。

## 方式 A：同步文件（推荐）

```powershell
$sync = Join-Path $env:USERPROFILE ".zcode\skills\three-tier-system\tools\sync-employee-profile.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $sync -Check
# MISSING 时安装；CONFLICT/DRIFT 经确认后才加 -Replace（自动备份旧文件）
powershell -NoProfile -ExecutionPolicy Bypass -File $sync
powershell -NoProfile -ExecutionPolicy Bypass -File $sync -Check
```

维护源同步到 `~/.zcode/agents/employee.md`。角色在会话启动时加载，因此同步后须重启客户端/新开会话，再验证按名召唤。分发或大版本复检时必须重新 `-Check`，未检查不得宣称运行角色已是最新版。

## 方式 B：设置 → 子智能体

| 字段 | 值 |
|---|---|
| 名称 | `employee` |
| 颜色 | 粉色（仅视觉） |
| 模型 | 继承默认；仅用户明确选择且端点已配置时更改 |
| 描述 | `profiles/employee.md` frontmatter 的 `description` |
| 可用工具 | `Read Grep Glob Bash Edit Write TodoWrite` |
| 系统提示词 | profile 正文全文 |
| 注入 AGENTS.md | 开 |
| 轮数上限 | UI 无此项；文件中的 `maxTurns` 只是软护栏 |

工具列表是可见性过滤，不是路径或 Bash 内动作的权限隔离。不要勾 `Agent`；员工不能再派子 Agent。也不需 `SendMessage`，员工结束一轮后由经理接力。运行时可能摘除部分声明工具并追加协调者应答通道，以实际新会话探针为准。

同一个 `employee` 档案可创建多个实例；隔离依赖任务包中的 lane、worktree、分支、写租约和资源授权，不依赖角色名。

保存后重启并验证。若仍返回 `Agent type 'employee' not found`，经理把 profile 正文与 `employee-brief.md` 任务包拼接后交给 `general-purpose`；职责相同，但运行时白名单和轮数不同。

## 禁止

- 不把模型设为不可用端点。
- 不开放 `Agent`、`SendMessage` 或会话读取工具。
- 不靠回合数控制大包；用任务包停止线。
- 不在本页或派发卡复制第二份员工合同。
