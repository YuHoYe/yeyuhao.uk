---
title: "为了门口摄像头的信号，买了个 Unifi U6+"
description: "门口的 TP-Link 门铃摄像头老是掉线，加了一个 Unifi U6+ AP 解决问题。选型翻车、POE 供电踩坑、接入体验记录。"
date: 2026-03-31
tags: ["Unifi", "智能家居"]
lang: "zh"
---

## 起因

家里的 TP-Link 门铃摄像头装在门外，隔了一道铁门，WiFi 信号一直很差。时不时掉线，有人按门铃的时候经常收不到通知。

看了一圈，决定在门口加一个 AP，给摄像头提供稳定的 WiFi 信号。

## 选型

家里网络全套 Unifi，所以新 AP 也只考虑 Unifi。

本来想一步到位买 U7 Pro，WiFi 7，性能拉满。看了一眼价格，没舍得。转头看了 U6+，WiFi 6，2x2 MIMO，价格只有 U7 的三分之一。给一个门铃摄像头供信号，U6+ 绰绰有余。

下单。

## 翻车

拿到手才想起来，U6+ 只支持 POE 供电，没有 DC 电源口。家里门口那个位置只有一根网线，交换机那边没有 POE 口。

又下单了 Unifi 的 POE 电源适配器。

这个适配器是真的大。一头插电，一头 RJ45 进，一头 RJ45 出（带 POE），体积快赶上 U6+ 本体了。

![U6+ 和 POE 适配器全貌](https://img.yeyuhao.uk/blog/2026/03/unifi-u6-overview.jpg)

![POE 适配器特写，确实不小](https://img.yeyuhao.uk/blog/2026/03/unifi-u6-poe-adapter.jpg)

## 接入

吐槽归吐槽，Unifi 的设备接入体验是真的好。

网线插上，电源通上，打开 Unifi 管理页面，新设备已经自己出现在列表里了。点一下「接管」，等几秒钟固件更新完，就可以用了。

![管理页面，U6+ 等待接管](https://img.yeyuhao.uk/blog/2026/03/unifi-devices.png)

接管之后自动加入 Mesh 网络，信道分配、SSID 同步都不用管。

![U6+ 详情，WiFi 6 双频 Mesh](https://img.yeyuhao.uk/blog/2026/03/unifi-u6-detail.png)

## 结果

门铃摄像头在线了，WiFi 体验评分 88%，信号稳定，不再掉线。

![TP-Link 门铃 WiFi 体验 88%](https://img.yeyuhao.uk/blog/2026/03/unifi-doorbell-wifi.png)

一个 AP 加一个 POE 适配器，解决了困扰了好久的问题。早该买了。
