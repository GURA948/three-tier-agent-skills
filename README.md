# Three-Tier Agent Skills

一套“用户—经理—员工”三级交付体系，分别适配 **Codex** 与 **ZCode**。两个版本共享目标和状态语义，但依赖不同宿主能力，请安装对应版本，不要混用目录。

## 选择版本

| 版本 | 安装目录 | 适用场景 | 关键差异 |
|---|---|---|---|
| [Codex 版](codex/README.md) | `~/.codex/skills/three-tier-system/` | Codex 桌面端中的持续代管开发 | 一个正式员工任务、一条写入线；使用可见任务和 worktree；不提供系统级巡航门 |
| [ZCode 版](zcode/README.md) | `~/.zcode/skills/three-tier-system/` | ZCode 中的经理—员工协作 | 自定义 `employee` 角色；支持有条件的多写并行；使用事件驱动监督，不启动巡航或轮询终端 |

## 仓库结构

```text
codex/three-tier-system/   Codex 可安装 Skill
zcode/three-tier-system/   ZCode 可安装 Skill、角色维护源与巡航工具
scripts/validate_release.py
```

## 快速安装

克隆仓库后，在 PowerShell 中执行对应版本：

```powershell
# Codex
Copy-Item -Recurse .\codex\three-tier-system "$env:USERPROFILE\.codex\skills\"

# ZCode
Copy-Item -Recurse .\zcode\three-tier-system "$env:USERPROFILE\.zcode\skills\"
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.zcode\skills\three-tier-system\tools\sync-employee-profile.ps1" -Check
# 返回 MISSING 时安装；返回 CONFLICT/DRIFT 时先检查现有角色，不要直接覆盖
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.zcode\skills\three-tier-system\tools\sync-employee-profile.ps1"
```

目标目录已存在时，先备份并比较差异。安装或更新后请重启客户端或新开会话。

## 验证

```powershell
python scripts\validate_release.py
```

当前发布内容不包含本机角色副本、模型 ID、密钥、任务运行状态或缓存。ZCode 版不启动常驻巡航、轮询脚本或后台终端。

## 兼容性

- Codex 版依赖支持任务、消息、等待和 worktree 的 Codex 宿主；缺失能力时按 Skill 内协议降级。
- ZCode 的 profile 同步助手使用 Windows PowerShell；其他平台可按 UI 对照手工创建角色。
- 两版都需要在目标宿主中实际验证任务派发、worktree、父会话恢复和验收流程。

## License

[MIT](LICENSE)
