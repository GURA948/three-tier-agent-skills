# ZCode 版

安装内容位于 [three-tier-system](three-tier-system/)。

此版本使用 ZCode 自定义 `employee` 角色，默认单写；满足独立验收、写集合、资源和集成约束时可启用多写并行。监督采用员工完成/阻断事件、经理有界检查和真实磁盘证据，不启动常驻巡航、轮询脚本或后台终端。

## 安装

```powershell
Copy-Item -Recurse .\zcode\three-tier-system "$env:USERPROFILE\.zcode\skills\"
$sync = "$env:USERPROFILE\.zcode\skills\three-tier-system\tools\sync-employee-profile.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $sync -Check
# MISSING 时运行安装；CONFLICT/DRIFT 时先检查现有角色
powershell -NoProfile -ExecutionPolicy Bypass -File $sync
```

不要上传或直接分发自己的 `~/.zcode/agents/employee.md`；它可能包含本机模型、端点或其他个人设置。可分发维护源是 [profiles/employee.md](three-tier-system/profiles/employee.md)。

安装后重启 ZCode 或新开会话。完整部署和换机检查见 [deployment.md](three-tier-system/references/deployment.md)。没有 PowerShell 的环境可按 [ui-setup.md](three-tier-system/references/ui-setup.md) 手工创建角色。
