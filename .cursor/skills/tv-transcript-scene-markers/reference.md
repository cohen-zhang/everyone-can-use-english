# Reference — S01E09 scene segmentation example

Canonical files:

- Transcript: `learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e09-transcript.txt`
- Config: `learning-notes/tv-series/modern-family/s01/transcript/modern-family-s01e09-scenes.yaml`

Episode: **Fizbo** (Luke birthday party; nonlinear hospital frame).

---

## YAML schema

```yaml
episode: S01E09
episode_arc: Luke 生日派对 / Fizbo
timeline_note: 片头/尾医院 + 中段派对闪回与交叉剪辑
scenes:
  - id: "01"
    place: 医院候诊区 · 片头（闪回框）
    plot: 卢克受伤送医；家人门外等医生。
    characters: Phil, Claire
    timeline: 派对事故之后（全集切入点，后文大量闪回）
    anchor: Do we know anything?
```

- `anchor`: match the English text after `- ` on the **first** subtitle block of the scene (whitespace-normalized).
- `id`: string, zero-padded recommended.

---

## S01E09 — 26 scenes (summary)

| ID | 地点 | 剧情要点 | Anchor (first English) |
| ---: | --- | --- | --- |
| 01 | 医院 | 片头候诊 | Do we know anything? |
| 02 | 邓菲家 | 生日愿望 | There he is. Big day's coming up. |
| 03 | 邓菲家 | 旁白 + 策划大派对 | Every year, Luke's birthday falls right around Thanksgiving, |
| 04 | 邓菲家 | 借卡拉 OK；小丑话题 | I feel terrible. We gotta do something. - Oh, yeah. |
| 05 | Mitch & Cam | 小丑/礼物之争 | Hey, Phil. Are, uh, you getting a clown for today? |
| 06 | Jay 家 | 十字弓礼物 | Hey, Gloria, |
| 07 | Jay 家 | 曼尼恋爱建议 | Hey, pal, how's it going? |
| 08 | 宠物店 | 租恐怖爬宠 | No, no, no. I want the most dangerous reptile you've got. |
| 09 | Cam 家 | Fizbo 上妆 | I couldn't get Luke out of my mind. |
| 10 | 邓菲后院 | 攀岩墙布置 | It all happened so fast. |
| 11 | 邓菲家/后院 | Dylan；梳套桌 | Mom, just so you know, Dylan cannot have mayonnaise. |
| 12 | Mitch & Cam | Fizbo 摊牌 | I'm home. |
| 13 | 邓菲后院 | 滑索事故 | If this tape is found in the future, |
| 14 | 邓菲后院 | 梳套被拒 | Hey, buddy, you having fun? |
| 15 | 车内→加油站 | Fizbo 护曼尼 | Did you remember to switch the whites to the dryer? |
| 16 | Jay 家 | Gloria 安慰曼尼 | Mind if I come in? |
| 17 | 邓菲后院 | 爬宠/蹦床 A 线 | Hey, Manny, wanna make a sweet comb sheath? |
| 18 | 邓菲后院 | 绳降；Phil 怕小丑 | Now comes the fun part. Rappel down. |
| 19 | 邓菲后院 | 曼尼 & Bianca | Look, I came on strong with that whole funny guy bit. |
| 20 | 邓菲后院 | 海莉吃醋 | So, do you keep these at a zoo or something? |
| 21 | 邓菲后院 | 蝎子出逃 | Hey, jungle lady? |
| 22 | 医院 | 交叉剪辑 | Is he okay? - Can we see him? |
| 23 | 邓菲后院 | 梳套翻红；姐弟谈心 | Come on. Ready? |
| 24 | 邓菲后院 | 连锁灾难 | Scorpion! Scorpion! Scorpion! |
| 25 | 医院 | 打石膏收尾 | Sweetie? Luke? |
| 26 | 尾声 | Fizbo 蛋糕 | Fizbo delivery! I brought the cake! |

---

## Correct boundary example (scenes 15 → 16)

From the transcript — marker sits **between** complete blocks:

```text
- Let's go. We're gonna be late.
 快走吧  要迟到了 

----------------------
【场景 16 / 26】Jay 家 · 客厅
★ 剧情：曼尼受挫；歌洛莉亚：做真实的自己。
★ 人物：Gloria, Manny
★ 时间线：派对中段
----------------------
- Mind if I come in?
 介意我也进来吗 
```

---

## Index table pattern (grouped rows)

```markdown
| 场景 | 地点 | 剧情要点 |
| ---: | --- | --- |
| 01 | 医院 | 片头：卢克受伤候诊 |
| 02–04 | 邓菲家 | 生日愿望、策划派对、借设备 |
| 05 | Mitch & Cam | 小丑 / 礼物之争 |
```

Use en-dash `02–04` for scanned ranges; keep ≤12 rows when possible.
