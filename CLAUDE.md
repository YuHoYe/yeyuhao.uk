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
npm run dev      # 启动开发服务器 http://localhost:4321
npm run build    # 生产构建到 dist/
npm run preview  # 预览生产构建
```

## 部署

```bash
git push   # 推送到 GitHub 后 Cloudflare Pages 自动构建部署
```

## 项目结构

```
src/
├── content.config.ts       # Content Collections schema（blog + projects）
├── content/
│   ├── blog/               # 文章 Markdown（frontmatter: title, description, date, tags, lang, draft）
│   └── projects/           # 项目数据 YAML（name, icon, description, tags, url, year）
├── components/
│   ├── Nav.astro           # 导航栏
│   ├── Footer.astro        # 页脚（版权 + 社交链接）
│   ├── PostCard.astro      # 首页文章卡片
│   ├── ProjectCard.astro   # 项目卡片
│   └── Giscus.astro        # 评论组件
├── layouts/
│   ├── BaseLayout.astro    # 基础布局（head + nav + main + footer）
│   └── PostLayout.astro    # 文章详情布局（元数据 + prose + 评论 slot）
├── pages/
│   ├── index.astro         # 首页（介绍 + 最新文章 + 项目摘要）
│   ├── blog/
│   │   ├── index.astro     # 博客列表
│   │   └── [...slug].astro # 文章详情（动态路由，用 post.id）
│   ├── projects.astro      # 项目页（卡片网格）
│   └── about.astro         # 关于页
└── styles/
    └── global.css          # Tailwind + 自定义主题变量 + prose 排版
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

## 语言

总使用中文回复。
