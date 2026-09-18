# Three-Tier Agent Skills

面向 vibe coding 的“用户—经理—员工”三级交付体系，分别适配 **Codex** 与 **ZCode**。

两个版本共享目标和状态语义，但依赖不同宿主能力。**只选择与你使用的 Agent 对应的一个版本，不要同时安装。**

## 安装 Codex 版

把下面这段话交给 Codex：

```text
请安装这个 GitHub 子目录中的 Skill，只安装 Codex 版，不要安装同仓库里的 ZCode 版。安装完成后验证 Skill 可被发现，并告诉我如何触发它：
https://github.com/GURA948/three-tier-agent-skills/tree/main/codex/three-tier-system
```

[查看 Codex 版目录](https://github.com/GURA948/three-tier-agent-skills/tree/main/codex/three-tier-system)

Codex 版使用一个独立可见的员工任务和一条活动写入线；不包含 ZCode 自定义角色，也不启动系统级巡航或轮询终端。

## 安装 ZCode 版

把下面这段话交给 ZCode：

```text
请安装这个 GitHub 子目录中的 Skill，只安装 ZCode 版，不要安装同仓库里的 Codex 版。按照目录内的部署说明完成 employee profile 配置；如果已有同名角色或自定义配置，先报告冲突，不要直接覆盖。安装完成后验证 Skill 和角色可用，并告诉我如何触发它：
https://github.com/GURA948/three-tier-agent-skills/tree/main/zcode/three-tier-system
```

[查看 ZCode 版目录](https://github.com/GURA948/three-tier-agent-skills/tree/main/zcode/three-tier-system)

ZCode 版使用自定义 `employee` 角色，支持满足约束时的多写并行；监督由完成/阻断事件、经理有界检查和真实磁盘证据驱动，不启动常驻巡航、轮询脚本或后台终端。

## 使用

- Codex：直接描述需要持续代管的开发任务，或显式使用 `$three-tier-system`。
- ZCode：说“启动三级体系”并描述任务；经理会按 Skill 协议澄清、派工和验收。

两个版本都是独立的 Skill 目录，Agent 可以只获取上面指定的 GitHub 子目录，无需下载 ZIP 或安装整个仓库。

## 仓库结构

```text
codex/three-tier-system/   Codex 可安装 Skill
zcode/three-tier-system/   ZCode 可安装 Skill、employee 角色维护源与同步工具
scripts/validate_release.py
```

## 手工安装（备用）

只有 Agent 无法代为安装时，才需要克隆仓库并执行下面的 PowerShell。命令会明确创建完整目标路径，避免把 Skill 内容复制到错误层级。

```powershell
# Codex
$target = Join-Path $env:USERPROFILE '.codex\skills\three-tier-system'
if (Test-Path -LiteralPath $target) { throw "目标已存在，请先比较或备份：$target" }
[IO.Directory]::CreateDirectory((Split-Path $target -Parent)) | Out-Null
Copy-Item -Recurse -LiteralPath '.\codex\three-tier-system' -Destination $target

# ZCode
$target = Join-Path $env:USERPROFILE '.zcode\skills\three-tier-system'
if (Test-Path -LiteralPath $target) { throw "目标已存在，请先比较或备份：$target" }
[IO.Directory]::CreateDirectory((Split-Path $target -Parent)) | Out-Null
Copy-Item -Recurse -LiteralPath '.\zcode\three-tier-system' -Destination $target
$check = & "$target\tools\sync-employee-profile.ps1" -Check
$check
if ($check -like 'MISSING:*') {
    & "$target\tools\sync-employee-profile.ps1"
} elseif ($LASTEXITCODE -ne 0) {
    throw '现有 employee 角色与维护源不同，请先检查，不要直接覆盖。'
}
```

安装或更新后，请重启对应客户端或新开会话。

## 验证

```powershell
python scripts\validate_release.py
```

当前发布内容不包含本机角色副本、模型 ID、密钥、任务运行状态或缓存。

## 兼容性

- Codex 版依赖支持任务、消息、等待和 worktree 的 Codex 宿主；缺失能力时按 Skill 内协议降级。
- ZCode 的 profile 同步助手使用 Windows PowerShell；其他平台可按 UI 对照手工创建角色。
- 两版都需要在目标宿主中实际验证任务派发、worktree、父会话恢复和验收流程。

## License

[MIT](LICENSE)
