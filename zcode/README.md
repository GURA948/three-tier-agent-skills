# ZCode 版

安装内容位于 [three-tier-system](three-tier-system/)。

此版本使用 ZCode 自定义 `employee` 角色，默认单写；满足独立验收、写集合、资源和集成约束时可启用多写并行。监督采用员工完成/阻断事件、经理有界检查和真实磁盘证据，不启动常驻巡航、轮询脚本或后台终端。

## 安装

把下面这段话交给 ZCode：

```text
请安装这个 GitHub 子目录中的 Skill，只安装 ZCode 版。按照目录内的部署说明完成 employee profile 配置；如果已有同名角色或自定义配置，先报告冲突，不要直接覆盖。安装完成后验证 Skill 和角色可用，并告诉我如何触发它：
https://github.com/GURA948/three-tier-agent-skills/tree/main/zcode/three-tier-system
```

不要上传或直接分发自己的 `~/.zcode/agents/employee.md`；它可能包含本机模型、端点或其他个人设置。可分发维护源是 [profiles/employee.md](three-tier-system/profiles/employee.md)。

Agent 只需获取上面指定的子目录，无需下载 ZIP 或安装同仓库的 Codex 版。安装后重启 ZCode 或新开会话，然后说“启动三级体系”并描述任务。完整部署和换机检查见 [deployment.md](three-tier-system/references/deployment.md)。没有 PowerShell 的环境可按 [ui-setup.md](three-tier-system/references/ui-setup.md) 手工创建角色。
