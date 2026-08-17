# 工作区外的文件编辑和网络访问需要审批
codex --ask-for-approval on-request

# 自动允许安全读操作；修改状态的命令需要审批
codex --ask-for-approval untrusted

# 禁用所有提示（谨慎使用）
codex --ask-for-approval never

网络访问控制
本地环境默认禁用网络访问。如需启用：
# ~/.codex/config.toml
[sandbox_workspace_write]
network_access = true


