---
title: "AI 时代的技术平权：30 分钟，我逆向了一个闭源空气净化器并接入了智能家居"
description: "用 AI 逆向 Airproce 艾泊斯空气净化器的闭源 API，接入 Home Assistant，全程只花了 2 分钟主动操作。"
date: 2026-03-28
tags: ["AI", "Home Assistant", "IoT"]
lang: "zh"
---

## 引子

前天晚上，我花了 30 分钟，把一台完全闭源、不支持任何第三方平台的空气净化器接入了 Home Assistant。

这是 MyAirProce APP 的界面——只有自家 APP 能控制，不支持米家、HomeKit 或任何第三方平台。而且 APP 本身也很鸡肋：没有定时自动切换模式的功能（每天晚上手动切睡眠，早上手动切回来），历史数据只保留最近几小时，过了就没了：

| ![MyAirProce APP 主界面](https://img.yeyuhao.uk/airproce-app-main.jpg) | ![APP 详情页](https://img.yeyuhao.uk/airproce-app-detail.jpg) |
|:---:|:---:|
| *APP 主界面 - 只能用自家 APP 控制* | *传感器数据、趋势图和设置* |

现在，我全程只做了这几件事：

- 跟 AI 说了几句话
- 在手机 APP 上点了几下
- 导出了一个文件

剩下的全部是 AI 自己完成的。

## 我说了什么，AI 做了什么

完整还原我和 Claude Code 的协作过程：

### 第一阶段：调研（2 分钟）

> 我：「AirProce 600 空气净化器能接入米家吗？」

AI 搜索后告诉我：不能，只有自家 APP。

> 我：「调研一下 HA 可以接入吗？」

AI 搜索后告诉我：没有现成集成，没有社区方案，但可以尝试抓包逆向 API。

### 第二阶段：抓包（5 分钟）

> 我：「你控制一下我手机的 Surge，捕获一下」

接下来的事情我几乎没有参与。AI 自己做了这些：

1. 读取我 Mac 上的 Surge 配置文件，找到 HTTP API 端口和密码
2. 连接 iPhone 上的 Surge HTTP API（试了好几个端口，最终找到 6171 可用）
3. 远程开启了 iPhone 的 MITM 和 Capture 功能

> AI：「Capture 和 MITM 都已开启。现在请你在手机上打开 MyAirProce APP 操作一下，操作完告诉我。」

> 我：随便点了几下，说了句「操作了」

AI 立刻从 Surge API 拉取了请求列表，发现了 4 个 `aph.airproce.com` 的 API 端点，拿到了认证 Token。

然后 AI 想获取请求的 body 内容——**这里它自己循环尝试了十多分钟**。先后试了 `/v1/requests/{id}/body`、`/v1/requests/{id}/request_body`、`/v1/requests/{id}/response_body`、`/v1/capture/body/{id}` 等各种路径，全部返回 `unknown path`。它甚至去爬了 Surge 的官方文档，最终得出结论：**Surge HTTP API 不支持读取 request/response body**。

然后它换了思路：

> AI：「需要你在 iPhone Surge 里导出 HAR 文件，AirDrop 到 Mac」

> 我：导出，AirDrop。30 秒搞定。

### 第三阶段：逆向 API（3 分钟）

AI 解析 HAR 文件后，一次性提取了所有 API 的完整请求和响应。然后它直接从电脑上用 curl 重放这些请求来验证——成功了。

4 个接口、认证方式、所有参数格式，全部搞清楚。

但还有些参数不知道含义。AI 的做法很聪明：

> AI：「能在 APP 上点一下睡眠模式吗？」

> 我：「点了」

> AI：「能点一下关机吗？」

> 我：「关了」

每次我在 APP 上操作后，AI 立刻调用 `get_status` 接口观察状态变化，反推出参数值。就这样，它用「操作-观察」的方式把所有模式值都搞清楚了：1=手动、2=自动、11=关机、21=睡眠。

### 第四阶段：接入 HA（10 分钟）

> 我：「在 HA 中集成这个设备，可以控制所有功能，以及在仪表盘增加所有数据展示」

一句话。AI 自己完成了：

1. 连接 HA 的 REST API 和 WebSocket API，发现已有的 SSH addon
2. 通过 SSH 登录 HA 虚拟机，读取现有的 `configuration.yaml`
3. 编写完整的 REST sensor（7 个传感器）、REST command（2 个控制命令）、input_select（模式和风速选择器）
4. 编写 4 条 automation 实现双向同步
5. 上传配置，验证语法，重启 HA
6. 通过 WebSocket API 创建 Lovelace 仪表盘
7. 验证所有实体正常工作

最终效果——Home Assistant 仪表盘。之前 APP 做不到的事现在都能做了：晚上 11 点自动切睡眠模式、早上 8 点自动切智能模式（通过 automation），历史数据保留 360 天（HA 的 recorder 每 30 秒记录一次，不依赖 AirProce 云端）：

| ![HA 仪表盘 - 状态与控制](https://img.yeyuhao.uk/airproce-ha-dashboard-top.jpg) | ![HA 仪表盘 - 仪表盘](https://img.yeyuhao.uk/airproce-ha-dashboard-gauges.jpg) | ![HA 仪表盘 - 趋势图](https://img.yeyuhao.uk/airproce-ha-dashboard-trends.jpg) |
|:---:|:---:|:---:|
| *设备状态与控制面板* | *PM2.5 / VOC / 温度 / 湿度仪表盘* | *24 小时空气质量与温湿度趋势* |

## 这意味着什么

两年前，「逆向一个闭源设备的 API 并接入智能家居」这件事，属于少数有经验的开发者才能完成的技术活。你需要懂网络协议、会分析 HTTP 请求、会写 YAML、了解 Home Assistant 的各种 platform——知识门槛很高。

现在，**门槛几乎降到了零**。你只需要能描述你想做什么，AI 会自己去探索、尝试、失败、调整、最终完成。它甚至会在遇到死路时自己换方向——比如发现 Surge API 不能读 body 时，它没有卡住，而是立刻建议我导出 HAR 文件。

这就是技术平权。不是说技术不重要了，而是 AI 把「会做」和「能做」之间的鸿沟填平了。你不需要记住 Home Assistant 的 REST sensor 怎么写，不需要知道 automation 的 YAML 语法，不需要理解 WebSocket API 的调用方式——你只需要说「我想把空气净化器接入智能家居」，然后在手机上点几下。

**真正稀缺的不再是技术能力，而是知道「可以做什么」的想象力。**
