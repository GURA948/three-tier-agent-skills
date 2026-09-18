# three-tier-system

面向 ZCode 的“用户—经理—员工”三级交付 Skill。经理负责澄清需求、维护唯一规格、派发工作包、事件驱动监督、验收和集成；员工只完成获派的一棒。

核心能力：

- 用轻量访谈把模糊想法收敛成可验收规格。
- 以 `READ` / `WRITE` 工作包和单写默认值控制范围；只有确有收益时才启用多写并行。
- 用唯一指导文档、冻结证据、写租约、candidate 和串行集成支持恢复与审计。
- 不启动常驻巡航、轮询脚本或后台终端；监督依靠员工事件、经理有界检查和真实磁盘证据。

## 使用

入口和按需路由见 [SKILL.md](SKILL.md)。安装、换机和发布前自检见 [references/deployment.md](references/deployment.md)。

## 目录

- `profiles/`：员工角色的可分发维护源。
- `references/`：经理按当前动作读取的协议和模板。
- `tools/sync-employee-profile.ps1`：安全同步或检查员工角色副本。
