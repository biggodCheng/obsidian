# OpenClaw 完整技能手册

> 版本：2026.3.2 | 本文档为纯技能参考，不含任何业务数据或个人记忆

---

## 一、OpenClaw 是什么

OpenClaw 是一个开源的个人 AI 助手平台，核心能力：
- **多渠道统一收发消息**（Telegram、飞书、WhatsApp、Slack、Discord 等 30+ 平台）
- **多 Agent 协作**（不同 Agent 负责不同任务，互不干扰）
- **浏览器自动化**（控制 Chrome 完成网页操作）
- **定时任务**（Cron Job 自动执行，无需人工干预）
- **语音通话**（支持 macOS/iOS/Android 唤醒词 + 电话呼入呼出）
- **设备联动**（macOS/iOS/Android 配对，远程执行命令、拍照、定位）
- **插件/技能系统**（65+ 内置技能，可扩展）

架构：`用户消息 → 渠道 → Gateway → Agent → 工具执行 → 回复`

---

## 二、核心命令速查

### 2.1 Gateway（控制中心）

Gateway 是 OpenClaw 的核心进程，所有消息、Agent、Cron 都通过它调度。

```bash
# 安装/启动/停止 Gateway 服务
openclaw gateway install      # 安装为系统服务（launchd/systemd）
openclaw gateway start        # 启动
openclaw gateway stop         # 停止
openclaw gateway restart      # 重启
openclaw gateway status       # 查看运行状态
openclaw gateway health       # 健康检查

# 调试
openclaw gateway run          # 前台运行（看实时日志）
openclaw gateway probe        # 全面探测（网络+服务+健康）
openclaw gateway discover     # Bonjour 发现局域网内其他 Gateway
openclaw gateway usage-cost   # 查看 token 用量和费用
```

**常见问题**：Gateway 卡死 → `openclaw gateway stop; sleep 5; openclaw gateway install`

### 2.2 Agent（员工管理）

每个 Agent 是一个独立的 AI 助手，有自己的身份、工作空间和路由规则。

```bash
# 创建 Agent
openclaw agents add <agent-id> \
  --workspace /path/to/workspace \
  --model "claude-cli/opus-4.6" \
  --non-interactive

# 设置身份（名字+emoji）
openclaw agents set-identity --agent <agent-id> --name "岗位名" --emoji "🎯"

# 查看所有 Agent
openclaw agents list
openclaw agents list --bindings   # 含路由绑定详情

# 删除 Agent
openclaw agents delete <agent-id>

# 路由绑定（指定渠道/账号的消息路由到特定 Agent）
openclaw agents bind <agent-id> --channel telegram --account <bot-id> --peer <chat-id>
openclaw agents unbind <agent-id> --channel telegram --account <bot-id>
openclaw agents bindings          # 查看所有绑定
```

**Agent 身份文件**：`~/.openclaw/agents/<agent-id>/agent/IDENTITY.md`

**手动触发 Agent 执行**：
```bash
openclaw agent --agent <agent-id> --message "你的任务指令" --thinking medium
```

### 2.3 Cron（定时任务）

```bash
# 创建定时任务
openclaw cron add \
  --name "任务名称" \
  --agent <agent-id> \              # 指定哪个 Agent 执行
  --cron "0 9 * * *" \              # cron 表达式（分 时 日 月 周）
  --tz "Asia/Shanghai" \            # 时区
  --session isolated \              # 隔离 session，不污染主会话
  --timeout-seconds 900 \           # 超时秒数
  --thinking medium \               # 思考深度：off/minimal/low/medium/high
  --message "执行指令内容" \
  --channel telegram \              # 结果投递渠道
  --account <bot-id> \              # 投递用的 bot
  --to <chat-id> \                  # 投递目标
  --announce                        # 投递摘要（不投递用 --no-deliver）

# 管理
openclaw cron list                  # 查看所有任务
openclaw cron list --json           # JSON 格式（含详细配置）
openclaw cron edit <job-id> --name "新名称"   # 编辑任务
openclaw cron enable <job-id>       # 启用
openclaw cron disable <job-id>      # 禁用
openclaw cron rm <job-id>           # 删除
openclaw cron run <job-id>          # 立即执行（调试用）
openclaw cron runs                  # 查看执行历史
openclaw cron status                # 调度器状态

# 一次性任务
openclaw cron add --at "+20m" --message "20分钟后执行" --delete-after-run
openclaw cron add --at "2026-03-15T09:00:00" --message "指定时间执行"

# 循环任务
openclaw cron add --every "2h" --message "每2小时执行"
```

**Session 策略**：
- `isolated`：每次执行创建独立 session，不污染主会话（推荐用于 cron）
- `main`：共享主会话（有上下文，但会膨胀）

**投递模式**：
- `--announce`：执行完后发送摘要到指定渠道
- `--no-deliver`：不投递，只执行

### 2.4 Channel（消息渠道）

```bash
# 添加渠道
openclaw channels add telegram --account <bot-id>   # 添加 Telegram bot
openclaw channels add feishu --account <name>        # 添加飞书 bot
openclaw channels add whatsapp                       # 添加 WhatsApp

# 登录/登出
openclaw channels login telegram --account <bot-id>
openclaw channels logout telegram --account <bot-id>

# 查看状态
openclaw channels list                # 列出所有渠道
openclaw channels status              # 健康状态
openclaw channels status --probe      # 实时探测
openclaw channels capabilities        # 各渠道能力对比

# 查找联系人/群组
openclaw directory peers list --channel telegram     # 列出联系人
openclaw directory groups list --channel telegram    # 列出群组
openclaw directory groups members <group-id> --channel telegram  # 群成员
```

**支持的渠道**（30+）：
Telegram, 飞书(Feishu), WhatsApp, Slack, Discord, Signal, iMessage(BlueBubbles), IRC, Microsoft Teams, Matrix, LINE, Google Chat, Mattermost, Nostr, Twitch, WebChat, macOS, iOS, Android 等

### 2.5 Message（消息收发）

```bash
# 发送消息
openclaw message send \
  --channel telegram \
  --account <bot-id> \
  --target <chat-id> \
  -m "消息内容"

# 发送媒体
openclaw message send --channel telegram --target <id> -m "看图" --media /path/to/image.png

# 读取消息
openclaw message read --channel telegram --target <chat-id> --limit 20

# 搜索消息
openclaw message search --channel telegram --query "关键词"

# 广播（群发）
openclaw message broadcast --channel telegram --targets "<id1>,<id2>" -m "群发内容"

# 其他
openclaw message edit --channel telegram --id <msg-id> -m "修改后的内容"
openclaw message delete --channel telegram --id <msg-id>
openclaw message react --channel telegram --id <msg-id> --emoji "👍"
openclaw message pin --channel telegram --id <msg-id>
openclaw message poll --channel telegram --target <id> --question "投票" --options "A,B,C"
```

### 2.6 Browser（浏览器自动化）

OpenClaw 内置 Chrome/Chromium 控制，支持完整的网页操作。

```bash
# 启动/停止浏览器
openclaw browser start
openclaw browser stop
openclaw browser status

# 导航
openclaw browser navigate "https://example.com"
openclaw browser open "https://example.com"     # 新标签页打开

# 截图/快照
openclaw browser snapshot --format ai            # AI 可读格式（含元素 ref）
openclaw browser screenshot                      # 全页截图
openclaw browser screenshot --path /tmp/shot.png # 保存到文件

# 页面交互
openclaw browser click --ref "<element-ref>"                      # 点击元素
openclaw browser type --ref "<element-ref>" --text "输入内容"      # 输入文字
openclaw browser fill --fields '[{"ref":"<ref>","value":"内容"}]'  # 填表单
openclaw browser press --key "Enter"                              # 按键
openclaw browser hover --ref "<element-ref>"                      # 悬停
openclaw browser select --ref "<ref>" --values '["option1"]'      # 下拉选择
openclaw browser upload --ref "<ref>" --files '["/path/to/file"]' # 上传文件

# 滚动
openclaw browser scroll --direction down
openclaw browser scrollintoview --ref "<element-ref>"

# 执行 JavaScript
openclaw browser evaluate --fn "() => { document.title }"
openclaw browser evaluate --fn "() => { window.scrollBy(0, 2000); return 'done'; }"

# 等待
openclaw browser wait --time 3000                    # 等3秒
openclaw browser wait --selector ".my-class"         # 等元素出现
openclaw browser wait --url "**/dashboard"           # 等URL匹配
openclaw browser wait --js "() => document.readyState === 'complete'"  # 等条件满足

# 标签页管理
openclaw browser tabs                   # 列出标签页
openclaw browser focus --tab <index>    # 切换标签页
openclaw browser close --tab <index>    # 关闭标签页

# 弹窗处理
openclaw browser dialog --action accept             # 确认弹窗
openclaw browser dialog --action dismiss             # 取消弹窗
openclaw browser dialog --action accept --text "输入" # 输入型弹窗

# 下载/PDF
openclaw browser pdf --path /tmp/page.pdf
openclaw browser download --url "https://example.com/file.zip"

# Cookie/存储
openclaw browser cookies --url "https://example.com"
openclaw browser storage --type local --url "https://example.com"

# 浏览器配置
openclaw browser set --viewport "1920x1080"
openclaw browser resize --width 1920 --height 1080

# Profile 管理（多账号）
openclaw browser create-profile --name "work"
openclaw browser list                    # 列出所有 profile
openclaw browser delete-profile --name "work"
```

**snapshot 的 ref 机制**：
- `snapshot --format ai` 返回的每个可交互元素都有一个 `ref` 标识
- 后续的 click/type/fill 等操作通过 ref 精准定位元素
- ref 在页面变化后会失效，需要重新 snapshot

**CDP 直连（高级用法）**：
浏览器暴露了 Chrome DevTools Protocol 端口（默认 18800），可以直接用 WebSocket 操作：
```python
import websocket, json
# 获取页面列表
# curl http://127.0.0.1:18800/json
ws = websocket.create_connection('ws://127.0.0.1:18800/devtools/page/<PAGE_ID>', suppress_origin=True)
# 执行 JS
ws.send(json.dumps({'id':1, 'method':'Runtime.evaluate', 'params':{'expression':'document.title'}}))
# 鼠标点击
ws.send(json.dumps({'id':2, 'method':'Input.dispatchMouseEvent', 'params':{'type':'mousePressed','x':100,'y':200,'button':'left','clickCount':1}}))
# 键盘输入（逐字符，适用于 contenteditable）
ws.send(json.dumps({'id':3, 'method':'Input.dispatchKeyEvent', 'params':{'type':'keyDown','key':'你','text':'你'}}))
# 截图
ws.send(json.dumps({'id':4, 'method':'Page.captureScreenshot', 'params':{'format':'jpeg','quality':50}}))
```

**CDP 踩坑记录**：
- WebSocket 连接必须设置 `suppress_origin=True`，否则被 CORS 拒绝
- 普通 `<input>` 用 `Input.insertText` 即可
- `contenteditable` 元素必须用逐字符 `Input.dispatchKeyEvent`（keyDown + keyUp），`insertText` / `execCommand` / clipboard 对某些框架无效
- 某些弹窗按钮 JS `.click()` 无效，必须用 `Input.dispatchMouseEvent` 鼠标事件
- 页面坐标需要注意缩放比例

### 2.7 Session（会话管理）

```bash
# 查看会话
openclaw sessions list                   # 列出所有会话
openclaw sessions list --active 24h      # 最近24小时活跃的
openclaw sessions list --agent <id>      # 指定 Agent 的会话
openclaw sessions list --json            # JSON 格式

# 清理
openclaw sessions cleanup                         # 常规清理
openclaw sessions cleanup --enforce --fix-missing  # 强制清理 + 修复缺失
```

**Session 文件位置**：`~/.claude/projects/<workspace-hash>/<session-id>.jsonl`

**常见问题**：
- Session 膨胀导致 resume 超时 → 删除对应 .jsonl 文件 + `openclaw sessions cleanup`
- "No conversation found" → `openclaw sessions cleanup --enforce --fix-missing`

### 2.8 Skills（技能系统）

```bash
openclaw skills list              # 列出所有可用技能
openclaw skills info <skill-name> # 查看技能详情
openclaw skills check             # 检查技能就绪状态
```

**常用内置技能**：
| 技能 | 功能 |
|------|------|
| feishu-doc | 飞书云文档创建/编辑 |
| feishu-wiki | 飞书知识库操作 |
| feishu-drive | 飞书网盘操作 |
| feishu-perm | 飞书权限管理 |
| prose | OpenProse 工作流编排（VM 模式） |
| coding-agent | 委派编码任务 |
| gh-issues / github | GitHub 操作 |
| gog | Google Workspace（Gmail/Calendar/Drive） |
| himalaya | IMAP/SMTP 邮件收发 |
| nano-banana-pro | AI 图片生成/编辑 |
| obsidian | Obsidian 笔记管理 |
| peekaboo | macOS UI 自动化（截图+操控） |
| session-logs | 搜索历史对话 |
| summarize | URL/PDF/音频摘要 |
| weather | 天气查询（免 API key） |
| xurl | X/Twitter API 操作 |
| voice-call | 语音通话 |
| apple-reminders | Apple 提醒事项 |
| apple-notes | Apple 备忘录 |
| camsnap | RTSP/ONVIF 摄像头截图 |

### 2.9 Nodes（设备联动）

```bash
# 查看已配对设备
openclaw nodes status
openclaw nodes list

# 配对管理
openclaw nodes pending              # 查看待配对请求
openclaw nodes approve <node-id>    # 批准配对
openclaw nodes reject <node-id>     # 拒绝
openclaw nodes rename <node-id> --name "我的手机"

# 远程操作
openclaw nodes invoke <node-id> --command "ls ~/Desktop"  # 远程执行命令
openclaw nodes run <node-id> --command "echo hello"       # macOS 远程 shell
openclaw nodes camera <node-id> --action snap             # 远程拍照
openclaw nodes screen <node-id> --action record           # 录屏
openclaw nodes location <node-id>                         # 获取位置
openclaw nodes notify <node-id> --title "提醒" --body "内容"  # 推送通知
openclaw nodes push <node-id> --title "标题" --body "内容"    # APNs iOS 推送
```

### 2.10 Voice（语音）

```bash
# 语音通话
openclaw voicecall call --to "+8613800138000"    # 拨出电话
openclaw voicecall speak --text "你好"            # 语音播报
openclaw voicecall continue --text "请说"         # 说完等回复
openclaw voicecall end                            # 挂断
openclaw voicecall status                         # 通话状态

# Tailscale 暴露（接收来电 webhook）
openclaw voicecall expose --enable
```

### 2.11 Memory（记忆搜索）

```bash
openclaw memory search --query "关键词"     # 语义搜索记忆
openclaw memory index                       # 重建索引
openclaw memory status                      # 索引状态

# LanceDB 底层
openclaw ltm list                           # 列出记忆条目
openclaw ltm search --query "关键词"        # 向量搜索
openclaw ltm stats                          # 统计信息
```

### 2.12 Config（配置管理）

```bash
openclaw config get <dot.path>              # 读取配置项
openclaw config set <dot.path> <value>      # 设置配置项
openclaw config unset <dot.path>            # 删除配置项
openclaw config file                        # 配置文件路径
openclaw config validate                    # 验证配置

# 交互式配置
openclaw configure                          # 引导式配置
openclaw onboard                            # 初始化向导
openclaw setup                              # 工作空间初始化
```

**配置文件位置**：`~/.openclaw/openclaw.json`

**常用配置路径**：
```
agents.defaults.model.primary          # 默认模型
agents.defaults.workspace              # 默认工作空间
agents.defaults.cliBackends[0]         # CLI 后端配置
session.dmScope                        # DM 会话范围（main/isolated）
gateway.auth.mode                      # Gateway 认证模式
browser.profiles                       # 浏览器 Profile 配置
```

### 2.13 Plugin（插件管理）

```bash
openclaw plugins list                       # 列出已安装插件
openclaw plugins install <path-or-npm>      # 安装插件
openclaw plugins uninstall <name>           # 卸载
openclaw plugins update <name>              # 更新
openclaw plugins enable <name>              # 启用
openclaw plugins disable <name>             # 禁用
openclaw plugins info <name>                # 详情
openclaw plugins doctor                     # 诊断插件问题
```

### 2.14 Security（安全）

```bash
# 安全审计
openclaw security audit            # 审计配置安全
openclaw security audit --deep     # 含 Gateway 实时探测
openclaw security audit --fix      # 自动修复安全问题

# DM 配对（新用户首次对话需要配对）
openclaw pairing list              # 查看待配对请求
openclaw pairing approve <code>    # 批准配对码

# 设备管理
openclaw devices list              # 已配对设备
openclaw devices approve <id>      # 批准设备
openclaw devices remove <id>       # 移除设备
openclaw devices rotate            # 轮换 token
openclaw devices revoke            # 撤销 token

# 执行审批
openclaw approvals get                          # 查看当前审批策略
openclaw approvals allowlist --agent <id>       # 编辑 Agent 白名单

# 沙箱
openclaw sandbox list              # 列出沙箱容器
openclaw sandbox explain           # 查看当前 session 的沙箱策略

# 密钥管理
openclaw secrets configure         # 交互式配置
openclaw secrets audit             # 审计明文密钥
openclaw secrets reload            # 重新加载密钥
```

### 2.15 Maintenance（运维）

```bash
# 健康检查
openclaw doctor                    # 快速诊断
openclaw doctor --deep             # 深度扫描
openclaw doctor --fix              # 自动修复
openclaw doctor --force            # 强力修复

# 状态总览
openclaw status                    # 渠道+会话概览
openclaw status --all              # 全面诊断
openclaw status --deep             # 含实时探测
openclaw status --usage            # 用量统计
openclaw health                    # Gateway 健康

# 日志
openclaw logs                      # 查看日志
openclaw logs --follow             # 实时跟踪
openclaw logs --limit 100          # 最近100条

# 更新
openclaw update status             # 当前版本信息
openclaw update wizard             # 交互式更新
openclaw update --channel beta     # 切换到 beta 频道
openclaw update --tag v2026.3.3    # 指定版本

# 重置
openclaw reset --scope config      # 仅重置配置
openclaw reset --scope full        # 完全重置（慎用）

# 卸载
openclaw uninstall --service       # 仅卸载服务
openclaw uninstall --all           # 完全卸载
```

---

## 三、Agent 协作架构设计

### 3.1 多 Agent 分工模式

```
老板（真人）
  │
  ├── 🦞 主 Agent（main）— CEO，总调度+实时对话
  │     ├── 📝 Agent A — 岗位1
  │     ├── 📊 Agent B — 岗位2
  │     └── 🎨 Agent C — 岗位3
  │
  └── 🕐 Cron Jobs — 定时自动执行
        ├── 定时任务1（Agent A 执行）
        ├── 定时任务2（Agent B 执行）
        └── 定时任务3（无指定 Agent）
```

### 3.2 Agent 间协作方式

Agent 之间不能直接对话，通过**文件交接**实现协作：
1. Agent A 执行完任务，把结果写入指定文件
2. Agent B 的 Cron 设定晚于 A，启动后读取 A 的输出文件
3. 文件末尾标注完成时间，B 可以检查 A 是否已完成

### 3.3 Session 策略

| 场景 | session 设置 | 说明 |
|------|------------|------|
| 实时对话 | `main` | 共享上下文，有连续记忆 |
| 定时任务 | `isolated` | 独立 session，不污染主会话 |
| 一次性任务 | `isolated` + `--delete-after-run` | 执行完自动清理 |

### 3.4 投递策略

| 场景 | 设置 | 说明 |
|------|------|------|
| 需要通知用户 | `--announce --channel telegram --to <id>` | 发送摘要 |
| 静默执行 | `--no-deliver` | 不通知 |
| 多渠道通知 | 用 Agent 内部 `openclaw message send` | Agent 在执行中主动发消息 |

---

## 四、飞书 API 集成

### 4.1 获取 Token

```bash
# 用 app_id + app_secret 获取 tenant_access_token
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"<APP_ID>","app_secret":"<APP_SECRET>"}'
```

### 4.2 创建云文档

```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"folder_token":"<FOLDER_TOKEN>","title":"文档标题"}'
```

创建后用 `docx/v1/documents/<doc_id>/blocks/<block_id>/children` 批量写入内容块。

### 4.3 设置文档权限

```bash
# 设置链接分享为"任何人可阅读"
curl -X PATCH "https://open.feishu.cn/open-apis/drive/v1/permissions/<token>/public?type=docx" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"external_access_entity":"anyone_can_read","link_share_entity":"anyone_readable"}'
```

### 4.4 发送群消息

```bash
# 发送文本/富文本/卡片消息到群
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "<CHAT_ID>",
    "msg_type": "post",
    "content": "{\"zh_cn\":{\"title\":\"标题\",\"content\":[[{\"tag\":\"text\",\"text\":\"内容\"}]]}}"
  }'

# 发送卡片消息
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "<CHAT_ID>",
    "msg_type": "interactive",
    "content": "{\"header\":{\"title\":{\"content\":\"标题\",\"tag\":\"plain_text\"}},\"elements\":[{\"tag\":\"div\",\"text\":{\"content\":\"内容\",\"tag\":\"lark_md\"}}]}"
  }'
```

---

## 五、微信公众号后台自动化

通过浏览器自动化操控微信公众号后台（mp.weixin.qq.com），实现关键词回复等设置。

### 5.1 关键词回复设置流程

1. **导航**：`https://mp.weixin.qq.com/advanced/autoreply?action=smartreply&t=ivr/keywords&token={TOKEN}&lang=zh_CN`
2. **点"添加回复"**：JS `.click()`
3. **填规则名称**：focus input → `Input.insertText`
4. **填关键词**：focus 默认关键词 input → `Input.insertText`（不要点 ⊕ 添加额外关键词）
5. **添加回复内容**：点"添加"按钮 → 点"文字"
6. **输入回复文字**：弹窗中的 `div.edit_area`（contenteditable）必须用逐字符 `Input.dispatchKeyEvent`
7. **确认弹窗**：必须用 `Input.dispatchMouseEvent` 鼠标事件（JS click 无效）
8. **保存**：JS `.click()` 保存按钮

### 5.2 关键技术点

- `contenteditable` 只认 `dispatchKeyEvent` 逐字符输入
- 弹窗确认按钮只认鼠标事件，不认 JS click
- token 从当前 session URL 提取，每次登录不同
- 找可见按钮：检查 `offsetHeight > 0` + `getBoundingClientRect()`

---

## 六、电源管理（macOS 防休眠）

OpenClaw 需要持续在线，macOS 熄屏后会断网。

```bash
# 禁止休眠 + 保持网络
sudo pmset -c sleep 0
sudo pmset -c networkoversleep 1
```

不设置会导致：熄屏 → 网络断开 → Gateway 所有连接中断 → 消息丢失。

---

## 七、常见问题排查

| 问题 | 解决方案 |
|------|---------|
| "No conversation found" | `openclaw sessions cleanup --enforce --fix-missing` |
| Session 膨胀/resume 挂死 | 删除 `~/.claude/projects/<hash>/<session-id>.jsonl` + cleanup |
| Gateway 卡死 | `openclaw gateway stop; sleep 5; openclaw gateway install` |
| "CLI produced no output for 180s" | 调大 watchdog timeout：`agents.defaults.cliBackends[0].reliability.watchdog` 设为 600s |
| 浏览器连接超时 | 杀残留进程 `pkill -f "node.*playwright"` 后重试 |
| Cron 不执行 | `openclaw cron status` 检查调度器 + `openclaw gateway health` 检查 Gateway |
| 渠道消息收不到 | `openclaw channels status --probe` 检查连接状态 |
| 定期清理 | isolated session 完成后无用，定期删 2 天前的 .jsonl 文件 |

---

## 八、目录结构参考

```
~/.openclaw/
├── openclaw.json               # 主配置文件
├── agents/                     # Agent 工作空间
│   ├── main/agent/             #   主 Agent（IDENTITY.md）
│   ├── <agent-id>/agent/       #   其他 Agent
├── browser/                    # 浏览器 Profile + 状态
├── credentials/                # 渠道凭证
├── cron/                       # Cron 任务配置 + 执行记录
│   ├── jobs.json
│   └── runs/
├── logs/                       # Gateway 日志
├── memory/                     # LanceDB 向量记忆
├── plugins/                    # 插件
├── sessions/                   # 会话索引
├── skills/                     # 自定义技能
└── workspace -> <path>         # 工作空间软链接
```

---

## 九、最佳实践

1. **Agent 隔离**：每个岗位一个 Agent，用 `isolated` session 执行 cron，避免上下文污染
2. **文件交接**：Agent 间通过文件传递数据，不要共享 session
3. **浏览器复用**：所有 Agent 共享同一个浏览器实例，提前登录好所有平台
4. **投递分级**：重要任务 announce 到 Telegram，日常任务 no-deliver
5. **超时设置**：cron timeout 设为预估时间的 2-3 倍，留足余量
6. **定期清理**：isolated session 产生的 .jsonl 文件定期清理
7. **Skills 文件**：每个 Agent 的技能写在独立文件里，cron prompt 指向文件路径，改技能不用改 cron
8. **Heartbeat 慎用**：心跳会注入消息导致 session 膨胀，长期运行建议关闭
9. **错误容忍**：cron prompt 中写明容错规则（浏览器卡住跳过、投递失败重试等）
10. **凭证集中管理**：所有 API key、token 放在一个凭证文件里，Agent 按需读取

## 十、配置Telegram机器人bot
1. BotFather 创建 bot → 拿 token                                                                                     
  2. CC 里 /plugin install 或插件市场搜 "telegram"                                                                      
  3. /telegram:configure <token> 配置                                                                                   
  4. claude --channels plugin:telegram@claude-plugins-official 启动                                                     
  5. 私聊 bot → 拿 pairing code → /telegram:access pair <code>                                                          
  6. /telegram:access policy allowlist 锁定只允许你的账号


 ## 十一 小龙虾必装skills
Skill	用途
planning-with-files	复杂任务规划，自动创建 task_plan.md、findings.md、progress.md
simplify	代码审查，自动检查代码质量、复用性和效率问题
skill-vetter	安装第三方 skill 前的安全检查，防止恶意代码
claude-api	使用 Claude API/Anthropic SDK 构建应用
superpowers-developing-for-claude-code	开发 Claude Code 插件/hooks/MCP 服务器
wechatskill	撰写/优化微信公众号文章
tanweai/pua PUA它你会发现，干活确实不一样了
ClawRouter 智能LLM路由器——节省92%的成本，41+ 种模型，<1毫秒路径规划，自动成本优化。https://github.com/BlockRunAI/ClawRouter