# Typst Render

AstrBot 插件, 支持使用将信息中的 Typst 代码渲染为 png 发送.

## 使用

- 数学公式, 设置为居中, 且页面更小更适中

```
\tym $pi times A$
```

- 纯Typst, 无前置样式

```
\typ $pi times A$
```

- [OurChat Create chat interfaces in Typst with ease](https://github.com/QuadnucYard/ourchat-typ/tree/main), 感谢 QuadnucYard/ourchat-typ ! 

```
\yau #wechat.chat(
  theme: "dark",
  ..oc.with-side-user(
    left,
    yau,
    oc.time[5月16日 上午10:23],
    oc.free-message[
      已經到了無恥的地步。
    ],
    oc.time[6月18日 凌晨00:06],
    oc.free-message[
      我宣布他已經不是我的學生了
    ],
    oc.time[14:00],
    oc.free-message[
      這種成績，使人汗顏！如此成績，如何招生？
    ],
  ),
  oc.message(right, yau)[
    我沒有説過這種話！

    ——發自我的手機
  ],
)
```

# 支持

[帮助文档](https://astrbot.app)
