#!/usr/bin/env python3
"""vibeUsage's website: a home page, Helper download, privacy, terms and support,
in English (/) and Chinese (/cn/). Plain static HTML, generated from the text
below so both languages share the same structure.

    python3 vibeusage-site/build.py         # writes public/vibeusage/

The output is committed: Cloudflare Pages only runs the Astro build, which
copies public/ as it is, so https://yeyuhao.uk/vibeusage/ is exactly these
files. Every link in them is relative. The app links to /vibeusage/privacy/
and /vibeusage/terms/, and App Store Connect to those and /vibeusage/support/,
so those three paths must keep working.
"""
import html
import pathlib
import shutil
import sys

# The address printed on every page. It must be a mailbox that is read.
CONTACT = "yuhoye@gmail.com"
UPDATED = {"en": "October 28, 2026", "cn": "2026 年 10 月 28 日"}
APP_STORE = ""  # The App Store link, once the app is live; empty hides the button.
HELPER_VERSION = "1.0.1"
HELPER_ARCHIVE = f"vibeUsage-Helper-{HELPER_VERSION}.zip"

CSS = """
:root{--bg:#0D100F;--card:#171C1A;--card2:#212927;--text:#EEF2EF;--sec:rgba(238,242,239,.66);
--ter:rgba(238,242,239,.52);--hair:rgba(238,242,239,.10);--accent:#5FD9A3;--accent-text:#5FD9A3;
--accent-soft:rgba(95,217,163,.14);--warn:#FFB454;--on-accent:#06130D}
@media (prefers-color-scheme: light){:root{--bg:#F3F6F4;--card:#FFFFFF;--card2:#EDF1EE;--text:#141A17;
--sec:rgba(20,26,23,.70);--ter:rgba(20,26,23,.62);--hair:rgba(20,26,23,.09);--accent:#1FA36B;
--accent-text:#13754B;--accent-soft:rgba(31,163,107,.13);--warn:#D9821B}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;
font:16px/1.65 -apple-system,"SF Pro Text",system-ui,"PingFang SC","Helvetica Neue",sans-serif}
a{color:var(--accent-text);text-decoration:none}a:hover{text-decoration:underline}
.num{font-family:ui-rounded,"SF Pro Rounded",-apple-system,system-ui,sans-serif;font-variant-numeric:tabular-nums}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.top{display:flex;align-items:center;justify-content:space-between;height:64px}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);font-weight:700;font-size:17px}
.brand img{width:30px;height:30px;border-radius:8px}
.lang{font-size:14px;color:var(--sec)}
.hero{text-align:center;padding:56px 0 24px}
.hero img.icon{width:96px;height:96px;border-radius:24px}
.hero h1{margin:20px 0 0;font-size:clamp(34px,6vw,52px);line-height:1.1;letter-spacing:-.5px}
.hero p{margin:14px auto 0;max-width:620px;font-size:18px;color:var(--sec);text-wrap:pretty}
.cta{display:inline-flex;align-items:center;height:50px;padding:0 26px;margin-top:26px;border-radius:25px;
background:var(--accent);color:var(--on-accent);font-weight:700}
.cta:hover{text-decoration:none;filter:brightness(1.05)}
.soon{display:inline-block;margin-top:26px;padding:8px 16px;border-radius:18px;background:var(--accent-soft);
color:var(--accent-text);font-size:14px;font-weight:600}
.shots{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:40px auto 0;max-width:880px}
.shots img{width:100%;border-radius:28px;border:1px solid var(--hair);display:block}
h2{font-size:26px;letter-spacing:-.2px;margin:72px 0 8px;text-align:center}
.lead{text-align:center;color:var(--sec);max-width:640px;margin:0 auto 28px;text-wrap:pretty}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.cardx{background:var(--card);border-radius:22px;padding:22px}
.cardx h3{margin:0 0 6px;font-size:17px}
.cardx p{margin:0;color:var(--sec);font-size:15px;text-wrap:pretty}
.pro{margin-top:14px;background:var(--card);border-radius:26px;padding:28px;display:grid;
grid-template-columns:1.2fr 1fr;gap:28px;align-items:center}
.pro h3{margin:0;font-size:22px;display:flex;align-items:center;gap:8px}
.badge{display:inline-flex;align-items:center;height:22px;padding:0 8px;border-radius:11px;background:var(--accent-soft);
color:var(--accent-text);font-size:12px;font-weight:700;letter-spacing:.4px}
.pro ul{margin:14px 0 0;padding:0;list-style:none}
.pro li{padding:9px 0;border-top:1px solid var(--hair);color:var(--sec);font-size:15px}
.pro li b{color:var(--text);font-weight:600}
.free{background:var(--card2);border-radius:18px;padding:18px;font-size:15px;color:var(--sec)}
.free b{display:block;color:var(--text);margin-bottom:4px}
footer{margin-top:88px;border-top:1px solid var(--hair);padding:28px 0 44px;color:var(--ter);font-size:14px;
display:flex;flex-wrap:wrap;gap:8px 22px;justify-content:space-between}
footer nav{display:flex;gap:18px;flex-wrap:wrap}
.doc{max-width:760px;margin:0 auto;padding:24px 0 0}
.doc h1{font-size:34px;line-height:1.2;margin:18px 0 4px}
.doc .date{color:var(--ter);font-size:14px;margin:0 0 28px}
.doc h2{font-size:20px;text-align:left;margin:36px 0 10px}
.doc p,.doc li{color:var(--sec)}
.doc ul{padding-left:20px;margin:8px 0}
.doc li{margin:6px 0}
.doc ol{padding-left:24px}
.doc ol li{padding-left:4px;margin:14px 0}
.helper-promo{margin-top:32px;background:var(--card);border-radius:26px;padding:28px;text-align:center}
.helper-promo h2{margin:0 0 8px;font-size:24px}
.helper-promo p{max-width:620px;margin:0 auto;color:var(--sec)}
.helper-promo .cta{margin-top:18px}
.helper-meta{font-size:14px;color:var(--ter)!important;margin-top:12px!important}
.helper-links{display:flex;flex-wrap:wrap;gap:10px 20px;margin-top:16px}
.doc b{color:var(--text);font-weight:600}
.note{background:var(--accent-soft);border-radius:16px;padding:16px 18px;margin:18px 0;color:var(--text)}
details{background:var(--card);border-radius:16px;padding:14px 18px;margin:10px 0}
summary{cursor:pointer;font-weight:600}
details p{margin:10px 0 2px}
@media (max-width:720px){.shots{grid-template-columns:1fr 1fr}.shots img:nth-child(3){display:none}
.pro{grid-template-columns:1fr}.hero{padding-top:36px}}
"""


def page(lang, depth, title, description, body, section=""):
    """One full document. `depth` is how far below the site root it sits."""
    root = "../" * depth
    home = (root + ("cn/" if lang == "cn" else "")) or "./"
    other = (root + ("" if lang == "cn" else "cn/")) or "./"
    if section:
        other = other + section + "/"
    t = TEXT[lang]
    store = f'<a href="{APP_STORE}">App Store</a>' if APP_STORE else ""
    return f"""<!doctype html>
<html lang="{'zh-Hans' if lang == 'cn' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="color-scheme" content="dark light">
<link rel="icon" href="{root}assets/icon.png">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
<div class="wrap">
<header class="top">
<a class="brand" href="{home}"><img src="{root}assets/icon.png" alt="">vibeUsage</a>
<a class="lang" href="{other}">{t['other_language']}</a>
</header>
{body}
<footer>
<span>© 2026 vibeUsage</span>
<nav>{store}<a href="{home}helper/">{t['helper_nav']}</a><a href="{home}privacy/">{t['privacy']}</a><a href="{home}terms/">{t['terms']}</a><a href="{home}support/">{t['support']}</a></nav>
</footer>
</div>
</body>
</html>
"""


def doc(lang, title, sections):
    parts = [f'<main class="doc"><h1>{title}</h1><p class="date">{TEXT[lang]["updated"]} {UPDATED[lang]}</p>']
    for heading, blocks in sections:
        if heading:
            parts.append(f"<h2>{heading}</h2>")
        for block in blocks:
            if isinstance(block, list):
                parts.append("<ul>" + "".join(f"<li>{item}</li>" for item in block) + "</ul>")
            elif block.startswith("!"):
                parts.append(f'<div class="note">{block[1:]}</div>')
            else:
                parts.append(f"<p>{block}</p>")
    parts.append("</main>")
    return "\n".join(parts)


MAIL = f'<a href="mailto:{CONTACT}">{CONTACT}</a>'

TEXT = {
    "en": {
        "other_language": "简体中文", "privacy": "Privacy", "terms": "Terms", "support": "Support",
        "updated": "Last updated:",
        "home_title": "vibeUsage - every AI coding quota in one place",
        "home_description": "See how much of your Claude, Codex, Cursor, Kimi, Grok and DeepSeek quota is left, "
                            "when it refills, and whether you are burning through it too fast. iPhone, iPad and Mac.",
        "tagline": "Every AI coding quota, in one place",
        "sub": "How much of Claude, Codex, Cursor, Kimi, Grok and DeepSeek is left, when each window refills, "
               "and whether you are spending faster than the clock. On iPhone, iPad and the Mac menu bar.",
        "soon": "Coming soon to the App Store", "download": "Download on the App Store",
        "features_title": "Built around one question: can I keep going?",
        "features_lead": "Not a dashboard of everything. The reading, the reset, and the pace.",
        "features": [
            ("The pace bar", "Every window shows what you have used against how much of the period has passed. "
                             "Ahead of the clock turns amber, with when you would run out."),
            ("One refill timeline", "All accounts on a single seven-day axis, in the order their windows come back."),
            ("Menu bar, widgets, lock screen", "The tightest account sits in the Mac menu bar; iPhone and iPad get "
                                               "home screen and lock screen widgets."),
            ("Token statistics", "Reads the token usage vibe-usage uploads to vibecafe.ai, by day, agent and "
                                 "model. Sign in to vibecafe once and your other devices connect through iCloud."),
            ("Your own iCloud", "Accounts and readings sync through your private iCloud database. "
                                "There is no vibeUsage server and no vibeUsage account."),
            ("Plugins", "A service that is not built in can be added as a small script, written by the AI you "
                        "already use from a prompt the app provides."),
        ],
        "pro_title": "vibeUsage", "pro_lead": "All features are free, including unlimited accounts and alerts.",
        "pro_points": [
            ("Unlimited accounts", "several of the same service too, all on one refill timeline."),
            ("Alerts", "spending too fast, nearly out, refilled - one notification each, with quiet hours."),
            ("Optional coffee", "support the developer from Settings. No features are unlocked and nothing renews automatically."),
        ],
        "free_title": "Always free",
        "free_text": "Statistics, widgets, the menu bar, iCloud sync, themes, and used / remaining readings.",
        "helper_nav": "Helper for Mac",
        "helper_promo_title": "Keep Claude readings up to date",
        "helper_promo_text": "Enable Active Refresh in vibeUsage, then open the downloaded Helper once. "
                             "It installs automatically and returns to the app.",
        "helper_promo_action": "Get the Helper",
    },
    "cn": {
        "other_language": "English", "privacy": "隐私政策", "terms": "用户协议", "support": "技术支持",
        "updated": "最后更新：",
        "home_title": "vibeUsage - AI 编码额度，一处看全",
        "home_description": "Claude、Codex、Cursor、Kimi、Grok、DeepSeek 还剩多少额度、什么时候回血、是不是用得太快。iPhone、iPad 与 Mac。",
        "tagline": "AI 编码额度，一处看全",
        "sub": "Claude、Codex、Cursor、Kimi、Grok、DeepSeek 还剩多少、每个窗口什么时候回血、是不是用得比时间还快。"
               "在 iPhone、iPad 和 Mac 菜单栏上。",
        "soon": "即将上架 App Store", "download": "在 App Store 下载",
        "features_title": "只回答一个问题：还能不能接着用",
        "features_lead": "不是什么都有的仪表盘。读数、重置时间、节奏。",
        "features": [
            ("节奏条", "每个窗口都把「已用」和「时间过了多少」画在同一条上。用得比时间快就变琥珀色，并告诉你按这个速度什么时候用完。"),
            ("一条回血时间轴", "所有账号排进同一条七天时间轴，按窗口恢复的先后。"),
            ("菜单栏、小组件、锁屏", "最紧张的账号常驻 Mac 菜单栏；iPhone 和 iPad 有主屏幕与锁屏小组件。"),
            ("Token 统计", "从 vibecafe.ai 读取 vibe-usage 上传的 Token 用量，按天、Agent、模型汇总。登录一次 vibecafe，其他设备通过 iCloud 自动连上。"),
            ("你自己的 iCloud", "账号和读数通过你的 iCloud 私有数据库同步。没有 vibeUsage 服务器，也没有 vibeUsage 账号。"),
            ("插件", "没有内置的服务可以用一段小脚本接入，由你已经在用的 AI 按 App 提供的提示词写出来。"),
        ],
        "pro_title": "vibeUsage", "pro_lead": "全部功能免费，包括不限数量的账号和提醒。",
        "pro_points": [
            ("账号数量不限", "同一家也能连多个，全部排进一条回血时间轴。"),
            ("提醒", "用得偏快、快用完、回血了，各发一条通知，可设安静时段。"),
            ("请开发者喝咖啡", "在设置里自愿支持开发者，不解锁任何功能，也不会自动续费。"),
        ],
        "free_title": "始终免费",
        "free_text": "统计、小组件、菜单栏、iCloud 同步、主题，以及已用 / 剩余两种读数。",
        "helper_nav": "Mac 助手",
        "helper_promo_title": "让 Claude 的额度读数保持更新",
        "helper_promo_text": "在 vibeUsage 中启用主动刷新，打开下载的助手一次，即可自动安装并返回 App。",
        "helper_promo_action": "获取助手",
    },
}


def home(lang):
    t = TEXT[lang]
    button = f'<a class="cta" href="{APP_STORE}">{t["download"]}</a>' if APP_STORE else f'<span class="soon">{t["soon"]}</span>'
    features = "".join(f'<div class="cardx"><h3>{a}</h3><p>{b}</p></div>' for a, b in t["features"])
    points = "".join(f"<li><b>{a}</b> - {b}</li>" if lang == "en" else f"<li><b>{a}</b>：{b}</li>" for a, b in t["pro_points"])
    depth = 1 if lang == "cn" else 0
    root = "../" * depth
    body = f"""<main>
<section class="hero">
<img class="icon" src="{root}assets/icon.png" alt="vibeUsage">
<h1>{t['tagline']}</h1>
<p>{t['sub']}</p>
{button}
<div class="shots">
<img src="{root}assets/detail.png" alt="" loading="lazy">
<img src="{root}assets/statistics.png" alt="" loading="lazy">
<img src="{root}assets/alerts.png" alt="" loading="lazy">
</div>
</section>
<h2>{t['features_title']}</h2>
<p class="lead">{t['features_lead']}</p>
<div class="grid">{features}</div>
<section class="pro">
<div>
<h3>{t['pro_title']} <span class="badge">PRO</span></h3>
<p style="color:var(--sec);margin:10px 0 0">{t['pro_lead']}</p>
<ul>{points}</ul>
</div>
<div class="free"><b>{t['free_title']}</b>{t['free_text']}</div>
</section>
<section class="helper-promo">
<h2>{t['helper_promo_title']}</h2>
<p>{t['helper_promo_text']}</p>
<a class="cta" href="helper/">{t['helper_promo_action']}</a>
</section>
</main>"""
    return page(lang, depth, t["home_title"], t["home_description"], body)


PRIVACY = {
    "en": ("Privacy Policy", [
        (None, [
            "vibeUsage shows how much of your AI coding quotas is left. It is built so that the developer never "
            "sees your data: there is no vibeUsage server, no vibeUsage account, no analytics and no advertising.",
            "!<b>In short:</b> your sign-ins and readings stay on your devices and in your own iCloud. The app talks "
            "only to the services you connect, to Apple, and to nothing else."]),
        ("What the app handles", [[
            "<b>Sign-in credentials</b> - the OAuth tokens or API keys for the services you connect (such as "
            "Claude, Codex, Cursor, Kimi, Grok, DeepSeek, or a plugin's own credential). Stored in the system "
            "Keychain on your device.",
            "<b>Quota readings</b> - the percentages, reset times, plan names and balances those services return.",
            "<b>Account labels</b> - the name or e-mail a service reports for the account, and any note you type.",
            "<b>Token statistics</b> - the vibecafe.ai API key you get by signing in to vibecafe, kept in the "
            "system Keychain, and the daily token totals by agent and model the app reads with it, cached on your "
            "device. The app reads no local logs, prompts, replies or code.",
            "<b>Coffee records</b> - transaction IDs and purchase dates, stored locally and synced through your private "
            "iCloud database when sync is available and enabled. The count is a thank-you, not a feature entitlement.",
            "<b>Settings</b> - theme, refresh interval, alert preferences, and which alerts have already been sent.",
        ]]),
        ("Where it goes", [[
            "<b>To the services you connect.</b> To read a quota the app sends that service your credential for it, "
            "directly from your device, the same way the service's own tools do. Each service handles that request "
            "under its own privacy policy.",
            "<b>To your iCloud (optional).</b> With iCloud sync on, accounts, credentials, readings, plugin scripts, "
            "your vibecafe API key and alert settings are stored in your private iCloud database so your "
            "devices stay in step. Credentials are written to CloudKit encrypted fields. The developer has no "
            "access to your iCloud data. You can turn sync off in Settings.",
            "<b>To vibecafe.ai.</b> Once you sign in to vibecafe, the app uses your API key to read your token usage "
            "from vibecafe.ai - data you uploaded yourself with vibe-usage. vibecafe.ai handles those requests under "
            "its own privacy policy. Signing out of vibecafe removes the key from every device and the cached statistics.",
            "<b>To Apple.</b> Coffee purchases are handled by the App Store. The app receives transaction IDs and "
            "purchase dates to count your coffees, never your payment details. Alerts are local notifications; the silent push that wakes the "
            "iPhone comes from your own iCloud database through Apple's push service.",
            "<b>To a plugin's service.</b> A plugin you install can make network requests to the service it was "
            "written for. Plugins cannot read your home folder; they receive only the credentials you import for them.",
        ], "Nothing is sent to the developer. Nothing is shared with, or sold to, third parties."]),
        ("Notifications", [
            "Alerts are scheduled and posted on your device. The app asks for notification permission only when you "
            "open the Alerts page, or switch an alert on. You can withdraw it in system settings at any time."]),
        ("Keeping and deleting", [[
            "Removing an account deletes its credential from the Keychain and from your iCloud record.",
            "Deleting the app removes everything stored on that device. Data in your iCloud can be removed under "
            "Settings &gt; Apple Account &gt; iCloud &gt; Manage Storage.",
            "The developer holds no copy of anything, so there is nothing for the developer to delete or export.",
        ]]),
        ("Children", ["vibeUsage is not directed at children under 13 and does not knowingly collect personal "
                      "information from them."]),
        ("Changes", ["If this policy changes, the new version is published here with a new date, and material "
                     "changes are mentioned in the app's release notes."]),
        ("Contact", [f"Questions about privacy: {MAIL}"]),
    ]),
    "cn": ("隐私政策", [
        (None, [
            "vibeUsage 用来查看你的 AI 编码额度还剩多少。它的设计目标是开发者永远看不到你的数据：没有 vibeUsage 服务器，"
            "没有 vibeUsage 账号，没有统计分析，也没有广告。",
            "!<b>一句话：</b>你的登录信息和读数只留在你的设备和你自己的 iCloud 里。App 只和你连接的服务、以及 Apple 通信，除此之外不联系任何人。"]),
        ("App 会处理哪些信息", [[
            "<b>登录凭据</b>：你连接的服务（如 Claude、Codex、Cursor、Kimi、Grok、DeepSeek，或插件自己的凭据）的 OAuth 令牌或 API Key，保存在设备的系统钥匙串中。",
            "<b>额度读数</b>：这些服务返回的百分比、重置时间、套餐名称和余额。",
            "<b>账号标签</b>：服务返回的账号名称或邮箱，以及你自己填写的备注。",
            "<b>Token 统计</b>：登录 vibecafe 后得到的 vibecafe.ai API Key 保存在系统钥匙串；App 用它读取按 Agent 和模型汇总的每日 Token 用量，缓存在本机。"
            "App 不读取任何本机日志、提示词、回复或代码。",
            "<b>咖啡记录</b>：交易 ID 和购买时间保存在本机，并在 iCloud 同步可用且开启时同步到你的私有数据库。杯数只是感谢记录，不代表任何功能权限。",
            "<b>设置</b>：主题、刷新间隔、提醒偏好，以及哪些提醒已经发过。",
        ]]),
        ("信息去向", [[
            "<b>发给你连接的服务。</b>为了读取额度，App 会把该服务对应的凭据从你的设备直接发给该服务，方式与它的官方工具相同。各服务按其自己的隐私政策处理这些请求。",
            "<b>存入你的 iCloud（可选）。</b>开启 iCloud 同步后，账号、凭据、读数、插件脚本、vibecafe 的 API Key 和提醒设置会保存在你的 iCloud 私有数据库里，"
            "用于多设备保持一致。凭据写入 CloudKit 的加密字段。开发者无法访问你的 iCloud 数据。你可以在设置里关闭同步。",
            "<b>发给 vibecafe.ai。</b>登录 vibecafe 后，App 用你的 API Key 从 vibecafe.ai 读取 Token 用量，这些数据是你自己用 vibe-usage 上传的。"
            "vibecafe.ai 按其自己的隐私政策处理这些请求。退出 vibecafe 会删除所有设备上的 Key 和本机缓存的统计。",
            "<b>发给 Apple。</b>购买完全由 App Store 处理；App 接收交易 ID 和购买时间，用于记录咖啡杯数，不会接触你的付款信息。提醒是本地通知；"
            "唤醒 iPhone 的静默推送来自你自己的 iCloud 数据库，经 Apple 的推送服务送达。",
            "<b>发给插件对应的服务。</b>你安装的插件可以向它所对接的服务发起网络请求。插件读不到你的主目录，只能拿到你为它导入的凭据。",
        ], "不会向开发者发送任何数据，也不会与第三方共享或出售任何数据。"]),
        ("通知", ["提醒在你的设备上排期并发出。只有当你打开「提醒」页、或打开某个提醒开关时，App 才会申请通知权限。你可以随时在系统设置里撤销。"]),
        ("保存与删除", [[
            "移除账号会同时从钥匙串和你的 iCloud 记录里删除它的凭据。",
            "删除 App 会清除该设备上保存的全部内容。iCloud 中的数据可在「设置 › Apple 账户 › iCloud › 管理储存空间」中删除。",
            "开发者不持有任何副本，因此没有需要开发者代为删除或导出的内容。",
        ]]),
        ("儿童隐私", ["vibeUsage 不面向 13 岁以下儿童，也不会有意收集他们的个人信息。"]),
        ("政策变更", ["本政策如有变更，新版本会连同新的日期发布在本页，重要变更会写进 App 的更新说明。"]),
        ("联系我们", [f"关于隐私的任何问题：{MAIL}"]),
    ]),
}

TERMS = {
    "en": ("Terms of Use", [
        (None, [
            "These terms apply to the vibeUsage apps for iPhone, iPad and Mac. They add to Apple's "
            '<a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Licensed Application End '
            "User License Agreement</a>, which also applies. By using the app you agree to both."]),
        ("What the app is", [
            "vibeUsage reads the usage figures that AI services report for your own accounts and presents them. "
            "It is an independent tool. It is not affiliated with, endorsed by or sponsored by Anthropic, OpenAI, "
            "Cursor, Moonshot AI, xAI, DeepSeek or any other service it can display; their names and marks belong "
            "to their owners."]),
        ("Your accounts", [[
            "Connect only accounts that are yours, or that you are authorised to use.",
            "You remain bound by each service's own terms. If a service changes or withdraws the interface the app "
            "relies on, that reading may stop working, and the developer cannot promise otherwise.",
            "Keep your devices secure: the credentials live in your Keychain and your iCloud.",
        ]]),
        ("Accuracy", [
            "Readings come from the services and may be delayed, rounded, or wrong at the source. Pace and "
            "“runs out at” figures are estimates. Alerts, background refresh and push delivery depend on the "
            "system and may arrive late or not at all. Do not rely on the app as the only safeguard against "
            "exceeding a limit or a budget."]),
        ("Optional coffee purchases", [[
            "All vibeUsage features are free, including unlimited accounts, alerts, statistics, widgets and iCloud sync.",
            "You can optionally buy the developer a coffee in Settings. Each coffee is a consumable in-app purchase "
            "that you may buy again. It is not a subscription and never renews automatically.",
            "A coffee does not unlock features, remove limits or provide extra services. The price and currency "
            "shown by the App Store at purchase apply.",
            "Payment, tax and refund requests are handled by Apple under the App Store's terms. Refund requests go to "
            '<a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.',
            "Consumable purchases cannot be restored through Restore Purchases. The app keeps a thank-you count "
            "and syncs its records through your private iCloud when available and enabled; this is not an App Store "
            "purchase-restoration service. Refunds do not change feature access, and the thank-you count is not reduced.",
        ]]),
        ("Plugins", [
            "Plugins are scripts that you choose to install, usually written by an AI assistant. They run with the "
            "credentials you give them and can contact the network. You are responsible for the plugins you "
            "install; review them before use."]),
        ("No warranty", [
            "The app is provided “as is”, without warranties of any kind, to the fullest extent the law allows. "
            "The developer is not liable for indirect or consequential loss, including charges from an AI service, "
            "lost work, or missed alerts. Nothing here limits rights you have under mandatory consumer law."]),
        ("Changes", ["These terms may be updated; the current version and its date are always on this page. "
                     "Continuing to use the app after a change means you accept it."]),
        ("Contact", [MAIL]),
    ]),
    "cn": ("用户协议", [
        (None, [
            "本协议适用于 iPhone、iPad 与 Mac 上的 vibeUsage。它是对 Apple "
            '<a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">《许可应用程序最终用户许可协议》</a>'
            "的补充，后者同样适用。使用本 App 即表示你同意这两份协议。"]),
        ("这个 App 是什么", [
            "vibeUsage 读取各 AI 服务为你自己的账号返回的用量数据并加以展示。它是一个独立工具，"
            "与 Anthropic、OpenAI、Cursor、月之暗面、xAI、DeepSeek 及其能够显示的任何其他服务均无隶属、背书或赞助关系；相关名称和标识归各自所有者所有。"]),
        ("你的账号", [[
            "只连接属于你、或你有权使用的账号。",
            "你仍需遵守各服务自己的条款。如果某个服务修改或关闭了 App 所依赖的接口，对应的读数可能失效，开发者无法对此作出保证。",
            "请保管好你的设备：凭据保存在你的钥匙串和你的 iCloud 里。",
        ]]),
        ("数据的准确性", [
            "读数来自各服务，可能有延迟、被取整，或在源头就不准确。「节奏」和「预计用完时间」都是估算。"
            "提醒、后台刷新和推送的送达取决于系统，可能延迟或不送达。请不要把本 App 当作防止超出限额或预算的唯一手段。"]),
        ("请开发者喝咖啡", [[
            "vibeUsage 全部功能免费，包括不限数量的账号、提醒、统计、小组件和 iCloud 同步。",
            "你可以在设置里自愿请开发者喝咖啡。每杯咖啡都是消耗型 App 内购买，可以重复购买；不是订阅，不会自动续费。",
            "购买咖啡不解锁任何功能，不解除任何限制，也不提供额外服务。价格和币种以购买时 App Store 显示的金额为准。",
            '付款、税费和退款申请由 Apple 按 App Store 的条款处理。退款请前往 <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a> 申请。',
            "消耗型购买不能通过「恢复购买」恢复。App 会记录感谢杯数，并在 iCloud 同步可用且开启时同步记录；这不属于 App Store 的购买恢复服务。退款不会影响功能使用，感谢杯数也不会因此减少。",
        ]]),
        ("插件", ["插件是你自行选择安装的脚本，通常由 AI 助手编写。它们使用你提供的凭据运行，并可以访问网络。你需要对自己安装的插件负责，使用前请先审阅。"]),
        ("免责声明", [
            "在法律允许的最大范围内，本 App 按「现状」提供，不附带任何形式的保证。对于间接或后果性损失，包括 AI 服务产生的费用、工作成果的损失或错过的提醒，"
            "开发者不承担责任。本协议不限制你依据强制性消费者保护法律享有的权利。"]),
        ("协议变更", ["本协议可能更新，当前版本及其日期始终以本页为准。变更后继续使用 App 即表示你接受变更。"]),
        ("联系我们", [MAIL]),
    ]),
}

SUPPORT = {
    "en": ("Support", "Answers to the questions that come up most, and how to reach a person.", [
        ("A reading says it needs re-authorisation.", "The sign-in for that service expired or was revoked. Open the "
         "account, choose Re-authorise, and sign in again; the account and its history stay."),
        ("My iPhone shows fewer accounts than my Mac.", "Accounts travel through iCloud. Check that both devices use "
         "the same iCloud account, that iCloud sync is on in the Mac's Settings, and tap Sync Now on the iPhone."),
        ("Do I need to pay to add more accounts or use alerts?", "No. All features are free. Buying the developer "
         "a coffee in Settings is optional and does not unlock anything."),
        ("Can I buy another coffee, and does it renew?", "You can buy another whenever you choose. Each purchase "
         "is consumable and never renews automatically. Coffee records sync through your private iCloud when "
         "available and enabled; consumable purchases cannot be restored through Restore Purchases."),
        ("An alert arrived late, or not at all.", "Refill alerts are scheduled ahead and are punctual. Too-fast and "
         "nearly-out alerts need a fresh reading: the Mac notices while it is running; an iPhone in your pocket "
         "depends on background refresh and silent push, both of which iOS throttles. Also check that "
         "notifications are allowed in system settings and that it is not inside your quiet hours."),
        ("How do I get a refund?", 'Refunds are handled by Apple at <a href="https://reportaproblem.apple.com">'
         "reportaproblem.apple.com</a>."),
        ("Does the developer see my tokens or conversations?", 'No. See the <a href="../privacy/">privacy policy</a>.'),
    ], "Still stuck? Write to", "Please include your device, system version and what you expected to see. "
       "Never send a token or an API key."),
    "cn": ("技术支持", "最常遇到的问题，以及怎么联系到人。", [
        ("某个账号提示需要重新授权。", "该服务的登录已过期或被撤销。打开这个账号，选择「重新授权」并重新登录；账号和历史数据都会保留。"),
        ("iPhone 上的账号比 Mac 上少。", "账号通过 iCloud 同步。请确认两台设备登录的是同一个 iCloud 账号、Mac 的设置里 iCloud 同步已打开，然后在 iPhone 上点「立即同步」。"),
        ("添加更多账号或使用提醒需要付费吗？", "不需要，全部功能免费。设置里的「请开发者喝咖啡」是自愿支持，不解锁任何功能。"),
        ("咖啡可以重复购买吗？会自动续费吗？", "可以按自己的意愿再次购买，每次都是消耗型购买，不会自动续费。咖啡记录会在 iCloud 同步可用且开启时同步；消耗型购买不能通过「恢复购买」恢复。"),
        ("提醒来晚了，或者没来。", "回血提醒是预先排好的，会准时。偏快和快用完需要最新读数：Mac 开着时由它发现；放在口袋里的 iPhone 依赖后台刷新和静默推送，"
         "这两者都会被 iOS 限流。也请检查系统设置里是否允许通知，以及当时是否处于安静时段。"),
        ("怎么退款？", '退款由 Apple 处理，请前往 <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>。'),
        ("开发者能看到我的令牌或对话吗？", '不能。详见<a href="../privacy/">隐私政策</a>。'),
    ], "还没解决？请写信到", "请附上设备型号、系统版本，以及你原本期望看到的结果。请不要发送任何令牌或 API Key。"),
}


HELPER = {
    "en": {
        "title": "vibeUsage Helper for Mac",
        "description": "Refresh your local Claude quota with the optional vibeUsage Helper for Mac.",
        "lead": "In vibeUsage, choose Enable Active Refresh to download the Helper directly. Open it once "
                "to finish setup. You can also download it here.",
        "download": "Download for Mac",
        "pending": "Download is being prepared",
        "ready_note": "Version {version} · macOS 13 or later · Apple silicon and Intel",
        "pending_note": "The download will appear here when the release is ready.",
        "before_title": "Before you begin",
        "before_text": "Install a version of vibeUsage with Active Refresh settings on this Mac. Claude Code must also be installed and signed in "
                       "with the Claude subscription you want to monitor.",
        "claude_link": "Claude Code installation guide",
        "steps_title": "Start in vibeUsage",
        "steps": [
            ("Download from the app", "In your local Claude account's Active Refresh settings, choose Enable Active Refresh. "
             "Your browser downloads the ZIP directly. If you downloaded from this page, continue with the next step."),
            ("Open the Helper once", "Open the ZIP, then double-click the vibeUsage Helper inside. Confirm opening "
             "if macOS asks. The Helper installs automatically and returns to vibeUsage. If Claude Code cannot be "
             "found or is not signed in, the Helper shows settings to resolve it."),
            ("Get your first reading", "Setup started from vibeUsage connects automatically. If you started from this page, "
             "confirm enabling active refresh in the app. A successful first reading confirms setup."),
        ],
        "after_text": "Once setup is complete, you can delete the downloaded installation copy. "
                      "vibeUsage's manual and automatic refresh will use the installed Helper.",
        "privacy_title": "Your existing sign-in stays with Claude",
        "privacy_text": "You do not need to copy a password, token or API key into the Helper. It uses "
                        "Claude Code's existing sign-in to refresh your quota and does not submit a chat prompt.",
        "remove_title": "Turn off or remove the Helper",
        "remove_text": "To return to cached readings, turn off active refresh in the Claude account's "
                       "settings in vibeUsage. To remove the Helper from this Mac, open the downloaded Helper, "
                       "switch back to its window and choose Uninstall helper. Your Claude Code sign-in and configuration stay in place.",
        "help": "Need help?",
        "home": "About vibeUsage",
    },
    "cn": {
        "title": "vibeUsage Mac 助手",
        "description": "安装可选的 vibeUsage Mac 助手，主动刷新本机 Claude 额度。",
        "lead": "在 vibeUsage 中点「启用主动刷新」即可直接下载助手，打开一次就能完成设置。这里也提供备用下载。",
        "download": "下载 Mac 助手",
        "pending": "下载包准备中",
        "ready_note": "版本 {version} · macOS 13 或更新版本 · Apple 芯片与 Intel",
        "pending_note": "发布包准备完成后，下载入口会显示在这里。",
        "before_title": "安装前",
        "before_text": "请先在这台 Mac 安装带有“主动刷新设置”入口的 vibeUsage 版本，并安装官方 Claude Code，登录你想查看额度的 Claude 订阅账号。",
        "claude_link": "Claude Code 安装说明",
        "steps_title": "从 vibeUsage 开始",
        "steps": [
            ("在 App 中下载", "在本机 Claude 账号的主动刷新设置中点「启用主动刷新」，浏览器会直接下载 ZIP。若已从本页下载，继续下一步即可。"),
            ("打开助手一次", "打开 ZIP 文件，再双击里面的 vibeUsage 助手。如果 macOS 提示是否打开，请确认。助手会自动安装并返回 vibeUsage；找不到 Claude Code 或尚未登录时，才会显示设置供你处理。"),
            ("取得首次读数", "从 vibeUsage 发起的安装会自动连接。从本页直接下载的用户，需要在 App 中确认启用主动刷新。首次额度读取成功后，设置就完成了。"),
        ],
        "after_text": "设置完成后，可以删除下载的安装副本。vibeUsage 的手动和自动刷新会使用已安装的助手。",
        "privacy_title": "沿用 Claude 的现有登录",
        "privacy_text": "不需要向助手复制密码、令牌或 API Key。助手沿用官方 Claude Code 的登录来刷新额度，不会发起对话。",
        "remove_title": "停用或卸载助手",
        "remove_text": "在 vibeUsage 的 Claude 账号设置中停用主动刷新，即可恢复读取缓存。要从这台 Mac 移除助手，打开下载的助手，切回助手窗口并选择「卸载助手」。你的 Claude Code 登录和配置会保留。",
        "help": "需要帮助？",
        "home": "了解 vibeUsage",
    },
}


def helper(lang, available):
    t = HELPER[lang]
    depth = 1 if lang == "en" else 2
    root = "../" * depth
    if available:
        action = f'<a class="cta" href="{root}downloads/{HELPER_ARCHIVE}" download>{t["download"]}</a>'
        note = t["ready_note"].format(version=HELPER_VERSION)
    else:
        action = f'<span class="soon" role="status">{t["pending"]}</span>'
        note = t["pending_note"]
    steps = "".join(f"<li><b>{title}</b><br>{text}</li>" for title, text in t["steps"])
    body = f"""<main class="doc">
<h1>{t['title']}</h1>
<p>{t['lead']}</p>
{action}
<p class="helper-meta">{note}</p>
<h2>{t['before_title']}</h2>
<p>{t['before_text']}</p>
<p><a href="https://code.claude.com/docs/en/setup">{t['claude_link']}</a></p>
<h2>{t['steps_title']}</h2>
<ol>{steps}</ol>
<p>{t['after_text']}</p>
<h2>{t['privacy_title']}</h2>
<p>{t['privacy_text']}</p>
<h2>{t['remove_title']}</h2>
<p>{t['remove_text']}</p>
<nav class="helper-links"><a href="../support/">{t['help']}</a><a href="../">{t['home']}</a></nav>
</main>"""
    return page(lang, depth, t["title"], t["description"], body, section="helper")


def support(lang):
    title, lead, faq, reach, hint = SUPPORT[lang]
    items = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)
    body = f"""<main class="doc"><h1>{title}</h1><p class="date">{lead}</p>
{items}
<h2>{TEXT[lang]['support'] if lang == 'en' else '联系我们'}</h2>
<p>{reach} {MAIL}</p><p>{hint}</p></main>"""
    return page(lang, 1 if lang == "en" else 2, f"{title} - vibeUsage", lead, body)


def build(out):
    if out.exists():
        # Release archives are copied here after signing and notarization.
        # Rebuilding the static pages must not remove a published download.
        for child in out.iterdir():
            if child.name == "downloads":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    shutil.copytree(pathlib.Path(__file__).parent / "assets", out / "assets")
    (out / "assets" / "site.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    archive = out / "downloads" / HELPER_ARCHIVE
    helper_available = archive.is_file() and archive.stat().st_size > 0
    for lang in ("en", "cn"):
        base = out / "cn" if lang == "cn" else out
        depth = 2 if lang == "cn" else 1
        base.mkdir(parents=True, exist_ok=True)
        (base / "index.html").write_text(home(lang), encoding="utf-8")
        for name, source in (("privacy", PRIVACY), ("terms", TERMS)):
            title, sections = source[lang]
            (base / name).mkdir(exist_ok=True)
            (base / name / "index.html").write_text(
                page(lang, depth, f"{title} - vibeUsage", title, doc(lang, title, sections)), encoding="utf-8")
        (base / "support").mkdir(exist_ok=True)
        (base / "support" / "index.html").write_text(support(lang), encoding="utf-8")
        (base / "helper").mkdir(exist_ok=True)
        (base / "helper" / "index.html").write_text(helper(lang, helper_available), encoding="utf-8")
    if CONTACT.startswith("TODO"):
        print("WARN the contact address is still a placeholder; set CONTACT before publishing")
    print(f"built {sum(1 for _ in out.rglob('index.html'))} pages into {out}")


if __name__ == "__main__":
    build(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent.parent / "public" / "vibeusage")
