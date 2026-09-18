# Codex 版

安装内容位于 [three-tier-system](three-tier-system/)。

此版本使用 Codex 的可见任务作为正式员工，固定一条活动写入线；会话内子 agent 只承担冻结输入上的只读调查或独立复核。它不包含 ZCode 的自定义角色、巡航门或门队脚本。

## 安装

```powershell
Copy-Item -Recurse .\codex\three-tier-system "$env:USERPROFILE\.codex\skills\"
```

安装或更新后重启 Codex 或新开任务。Skill 支持自动发现，也可显式使用 `$three-tier-system`。

## 要求

- 能创建和管理独立任务的 Codex 桌面宿主
- Git 项目使用应用管理的 worktree；非 Git 项目可使用本地目录
- 实际可用能力以宿主暴露的任务、等待、消息和可选 heartbeat 工具为准
