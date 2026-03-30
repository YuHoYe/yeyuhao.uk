# yeyuhao.uk — 个人网站

## 项目概览

个人网站 + 博客，面向泛互联网用户。技术 + 生活混合内容，中英双语。

- **线上地址**: https://yeyuhao.uk
- **仓库**: https://github.com/YuHoYe/yeyuhao.uk
- **框架**: Astro 5.x + Tailwind CSS 4
- **部署**: Cloudflare Pages（push 自动构建）
- **图床**: Cloudflare R2（`img.yeyuhao.uk`，bucket: `site-images`）
- **评论**: Giscus（GitHub Discussions）
- **风格**: 极简克制，黑白灰，深色模式跟随系统

## 开发命令

```bash
npm run dev      # 同步 memos + 启动开发服务器 http://localhost:4321
npm run build    # 同步 memos + 生产构建到 dist/
npm run preview  # 预览生产构建
```

## 部署

```bash
git push   # 推送到 GitHub 后 Cloudflare Pages 自动构建部署
```

## 项目结构

```
src/
├── content.config.ts       # Content Collections schema（blog + projects + memos）
├── content/
│   ├── blog/               # 文章 Markdown（frontmatter: title, description, date, tags, lang, draft）
│   ├── projects/           # 项目数据 YAML（name, icon, description, tags, url, year）
│   └── memos/              # 碎片 Markdown（从 Obsidian vault 同步，frontmatter: date, origin, confirmed, tags）
├── components/
│   ├── Nav.astro           # 导航栏
│   ├── Footer.astro        # 页脚（版权 + 社交链接）
│   ├── PostCard.astro      # 首页文章卡片
│   ├── ProjectCard.astro   # 项目卡片
│   ├── Giscus.astro        # 评论组件
│   ├── MemoCard.astro      # 碎片卡片（flomo 风格）
│   ├── MemoHeatmap.astro   # 热力图（SVG）
│   └── MemoTagCloud.astro  # 标签云（可点击过滤）
├── layouts/
│   ├── BaseLayout.astro    # 基础布局（head + nav + main + footer）
│   └── PostLayout.astro    # 文章详情布局（元数据 + prose + 评论 slot）
├── plugins/
│   └── remark-wikilinks.mjs # Remark 插件：清除 Obsidian [[wikilinks]]
├── pages/
│   ├── index.astro         # 首页（介绍 + 最新文章 + 项目摘要）
│   ├── blog/
│   │   ├── index.astro     # 博客列表
│   │   └── [...slug].astro # 文章详情（动态路由，用 post.id）
│   ├── memos.astro         # 碎片页（flomo 风格：侧边栏 + 卡片流）
│   ├── projects.astro      # 项目页（卡片网格）
│   └── about.astro         # 关于页
└── styles/
    └── global.css          # Tailwind + 自定义主题变量 + prose 排版 + memo 样式
```

## 写文章

在 `src/content/blog/` 创建 Markdown 文件：

```markdown
---
title: "文章标题"
description: "一句话描述"
date: 2026-03-30
tags: ["Tag1", "Tag2"]
lang: "zh"        # "zh" | "en"
draft: false
---

正文内容...
```

## 添加项目

在 `src/content/projects/` 创建 YAML 文件：

```yaml
name: "项目名"
icon: "🔧"
description: "一句话描述"
tags: ["Tech1", "Tech2"]
url: "https://github.com/..."
year: 2026
```

## 碎片（Memos）

数据源是 Obsidian vault（`~/Developer/YuhoVault/Memos/notes/`），通过同步脚本复制 `confirmed: true` 的 memo 到 `src/content/memos/`。

```bash
./scripts/sync-memos.sh   # 手动同步（npm run dev/build 时自动执行）
```

- `npm run dev` 和 `npm run build` 会自动先执行 sync 脚本
- CI 环境（Cloudflare Pages）没有 vault，sync 自动跳过，用仓库中已提交的 memo 文件构建
- 页面风格参照 flomo：左侧边栏（统计 + 热力图 + 标签云）+ 右侧卡片流
- Obsidian `[[wikilinks]]` 由 remark 插件在构建时自动清除

## 上传图片到 R2

```bash
./scripts/upload-r2.sh photo.jpg                        # 自动放到 blog/YYYY/MM/
./scripts/upload-r2.sh photo.jpg blog/2026/03/photo.jpg  # 指定路径
# 输出 Markdown 格式的图片链接
```

首次使用需 `npx wrangler login` 认证。

## 设计决策

- **不用 i18n 框架**: 中英文各写独立文件，UI 保持英文
- **不用 @astrojs/tailwind**: Tailwind CSS 4 通过 `@tailwindcss/vite` 插件集成
- **Content Collections 用 glob loader**: Astro 5.x 的 `astro/loaders` API
- **CSS 变量做主题**: `--color-text` 等变量，深色模式通过 `prefers-color-scheme` 媒体查询切换
- **prose 样式手写**: 不用 `@tailwindcss/typography`，保持最小依赖
- **Memos 数据同步**: Obsidian vault 为唯一数据源，sync 脚本复制到仓库，CI 用已提交文件构建
- **Remark 插件处理 wikilinks**: 全局生效，清除 Obsidian `[[...]]` 语法

## 语言

总使用中文回复。
