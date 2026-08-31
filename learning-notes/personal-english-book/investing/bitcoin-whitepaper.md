---
tags:
  - personal-english-book
  - english-learning
  - peb/investing
  - topic/investing
  - topic/crypto
  - topic/bitcoin
  - vocabulary/finance-investing
aliases:
  - Bitcoin 白皮书
  - BTC 白皮书
  - Bitcoin whitepaper
  - Satoshi Nakamoto paper
---
# Bitcoin: A Peer-to-Peer Electronic Cash System — BTC 白皮书

Satoshi Nakamoto published this nine-page paper on 31 October 2008. It is the design memo for **Bitcoin (BTC)** — not a trading pitch.

中本聪于 2008 年 10 月 31 日发表这篇九页论文。它是 **比特币（BTC）** 的设计备忘录，不是交易推销文。

**原文 PDF：** [bitcoin.org/bitcoin.pdf](https://bitcoin.org/bitcoin.pdf) · [HTML](https://bitcoin.org/en/bitcoin-paper)

**索引：** [[learning-notes/personal-english-book/investing/README|投资英语场景索引]] · [[learning-notes/personal-english-book/README|个人英文材料书索引]]

**相关（扩展）：**
- [[learning-notes/personal-english-book/investing/crypto-exchange-app-scenarios|加密货币 — 交易所 APP 常用场景]] — 充提币、现货、链上确认（白皮书原理 ↔ App 操作英语）
- [[learning-notes/personal-english-book/work/finance-business-stories|金融和商务主题故事集]] — B 节 **crypto** / **Bitcoin** / **hedge** 行情故事
- [[learning-notes/personal-english-book/work/金融和商务💰_20260514_2037|金融和商务词表（149）]] — Bitcoin 作为 **hedge against inflation**、**speculative** 等笔记句
- [[learning-notes/personal-english-book/work/专业术语|工作专业术语]] — **asymmetric algorithm** / **public-key crypto**（与本文数字签名对照）

**本文按白皮书原章节朗读。** 每句英文下用 **—** 给简中。术语加粗；后半是词汇表。**泽哥**读原文或跟别人讲 BTC 原理时，可以直接念这些句子。

> **提示**：这是学习笔记，不是白皮书全文，也不构成投资建议。原文很短，读完再对照本页。论文里几乎不用后来的口头禅 **blockchain** / **miner**——它写的是 **chain of proof-of-work** 与 **nodes**。

---

## Abstract — 摘要

The pitch in one breath: send **electronic cash** **peer-to-peer**, skip the bank, and still stop **double-spending**.

一句话：点对点寄出电子现金，跳过银行，还能挡住「同一笔钱花两次」。

- **A purely peer-to-peer version of electronic cash would allow online payments without a financial institution.** — 纯点对点的电子现金，可以不经金融机构就完成网上付款。
- **Digital signatures help, but you still need a way to stop double-spending.** — 数字签名有用，但还得挡住双花。
- **The network timestamps transactions by hashing them into a chain of proof-of-work.** — 网络把交易哈希进一条工作量证明链，从而盖上时间戳。
- **The longest chain is the record of what happened — and proof it came from the most CPU power.** — 最长链就是事件记录，也证明它来自最多的 CPU 算力。
- **As long as honest nodes hold most CPU power, they outpace attackers.** — 只要诚实节点掌握大部分算力，就能跑赢攻击者。

---

## 1. Introduction — 引言

Internet commerce leans on banks as **trusted third parties**. That model is expensive, reversible, and leaky.

互联网商务把银行当可信第三方。这套模型贵、可撤销、还容易泄露信息。

- **Commerce on the Internet has come to rely on financial institutions as trusted third parties.** — 互联网商务已经习惯把金融机构当可信第三方。
- **Mediation costs raise the minimum practical transaction size.** — 调解成本把最小可行交易额抬高了。
- **Merchants collect more customer data than they really need.** — 商户收集的客户数据，比真正需要的多。
- **We need an electronic payment system based on cryptographic proof instead of trust.** — 我们需要一套靠密码学证明、而不是靠信任的电子支付系统。
- **The hard problem is double-spending — spending the same coin twice.** — 真正的难题是双花：同一枚币花两次。
- **The paper proposes a peer-to-peer distributed timestamp server.** — 论文提出一个点对点的分布式时间戳服务器。

---

## 2. Transactions — 交易

An electronic coin is a **chain of digital signatures**. Ownership moves when you sign.

电子币是一串数字签名。所有权靠签名转移。

- **An electronic coin is a chain of digital signatures.** — 电子币就是一串数字签名。
- **The owner signs a hash of the previous transaction plus the next owner's public key.** — 持有者对「上一笔交易的哈希 + 下家公钥」签名。
- **The payee can verify the chain of ownership.** — 收款人可以核验这条所有权链。
- **The payee still cannot see whether a previous owner double-spent the coin.** — 收款人仍看不见上一任有没有双花。
- **A mint can check every spend — but that puts a trusted party back in the middle.** — 造币厂可以审查每笔花费——但又把可信方请回来了。
- **The only way to confirm no earlier spend is to know all transactions.** — 要确认没有更早的花费，就得知道全部交易。
- **All transactions must be publicly announced.** — 所有交易必须公开广播。
- **Participants need one agreed history of the order they were received.** — 参与者需要就「收到顺序」达成一份公认历史。

---

## 3. Timestamp Server — 时间戳服务器

A **timestamp server** hashes a block of items and publishes that hash. Each stamp includes the last one.

时间戳服务器给一批条目做哈希并公布。每一戳都咬住上一戳。

- **A timestamp server takes a hash of a block of items and widely publishes it.** — 时间戳服务器对一批条目取哈希，再广而告之。
- **The timestamp proves the data must have existed at that time.** — 时间戳证明数据在那个时刻已经存在。
- **Each timestamp includes the previous timestamp in its hash.** — 每个时间戳都把上一个时间戳写进自己的哈希。
- **That forms a chain — change one block, and every later hash breaks.** — 这就形成一条链——改一块，后面的哈希全裂。

---

## 4. Proof-of-Work — 工作量证明

To run the timestamp server without a newspaper, nodes hunt for a **proof-of-work** — in the spirit of Hashcash.

不靠报纸也能跑时间戳服务器：节点去找工作量证明，思路接近 Hashcash。

- **Proof-of-work means scanning for a hash that starts with a run of zero bits.** — 工作量证明就是扫出一个以一串零比特开头的哈希。
- **Bitcoin uses SHA-256 for that hunt.** — 比特币用 SHA-256 来做这场搜寻。
- **The average work grows exponentially with the number of zero bits.** — 零比特越多，平均工作量指数上升。
- **Once found, the proof is cheap to verify.** — 一旦找到，验证却很便宜。
- **Proof-of-work is one-CPU-one-vote.** — 工作量证明等于一 CPU 一票。
- **The majority decision is the longest chain.** — 多数决定体现为最长链。
- **To rewrite a past block, an attacker must redo that work and all work after it.** — 要改过去的块，攻击者必须重做那块以及之后全部工作。
- **Difficulty adjusts so blocks keep arriving on a steady beat.** — 难度会调节，好让出块节奏稳住。

---

## 5. Network — 网络

The network is messy on purpose. Little coordination. Nodes come and go.

网络故意很松散。几乎不协调。节点来去自由。

1. **New transactions are broadcast to all nodes.** — 新交易广播给所有节点。
2. **Each node collects new transactions into a block.** — 每个节点把新交易收进一个区块。
3. **Each node works on finding a difficult proof-of-work for its block.** — 每个节点为自己的区块寻找高难度工作量证明。
4. **When a node finds it, it broadcasts the block to all nodes.** — 找到后，就把该区块广播给所有节点。
5. **Nodes accept the block only if every transaction is valid and unspent.** — 只有每笔交易都有效且未花费，节点才接受该块。
6. **Nodes show acceptance by working on the next block, using this hash as the previous hash.** — 节点用这块的哈希当下一块的「前哈希」，以此表示接受。

- **Nodes always treat the longest chain as the correct one.** — 节点永远把最长链当作正确链。
- **If two nodes broadcast different next blocks, work continues on the first one they saw.** — 若两个节点广播了不同的下一块，各自先接着自己先看到的那条干。
- **The tie breaks when the next proof-of-work makes one branch longer.** — 下一份工作量证明让其中一条更长，平局就解开。
- **A new transaction does not need to reach every node on the first hop.** — 新交易不必第一跳就传到每一个节点。

---

## 6. Incentive — 激励

The first transaction in a block mints a **new coin** for the block's creator. Fees can take over later.

区块里的第一笔交易给创建者铸造一枚新币。手续费以后可以接班。

- **The first transaction in a block is a special one that starts a new coin.** — 区块第一笔是特殊交易，开出一枚新币。
- **That incentive gets nodes to support the network.** — 这份激励让节点愿意撑住网络。
- **It also spreads coins with no central issuer.** — 它也在没有中央发行方的情况下把币散出去。
- **The incentive can also come from transaction fees.** — 激励也可以来自交易手续费。
- **If outputs are worth less than inputs, the difference is a fee.** — 若输出面值小于输入，差额就是手续费。
- **Once a preset number of coins exist, the incentive can shift entirely to fees.** — 预定数量的币发完后，激励可以完全改成手续费。
- **That would be inflation-free.** — 那样就没有通胀。
- **Attacking the chain is usually dumber than playing by the rules and collecting new coins.** — 攻击链条，通常还不如守规矩、去领新币划算。

---

## 7. Reclaiming Disk Space — 回收磁盘空间

Old spent transactions can be dropped. A **Merkle tree** keeps the block hash intact.

花掉的旧交易可以丢掉。默克尔树让区块哈希仍然站得住。

- **Once a coin's latest spend sits under enough blocks, earlier spent transactions can go.** — 一枚币的最近一笔花费被足够多的块埋住后，更早的已花费交易可以删。
- **Transactions are hashed in a Merkle tree; only the root sits in the block header.** — 交易在默克尔树里哈希；区块头只留树根。
- **Old blocks can be compacted by stubbing off branches of the tree.** — 砍掉树的枝桠，旧块就能压瘦。
- **A header without transactions is about eighty bytes.** — 不含交易的区块头大约八十字节。
- **At one block every ten minutes, that is a few megabytes a year.** — 按每十分钟一块算，一年也就是几兆字节。

---

## 8. Simplified Payment Verification — 简易支付验证

You can check a payment without running a full node. Later people call this **SPV**.

不必跑全节点也能核对一笔付款。后人称之为 SPV。

- **A user only needs the block headers of the longest proof-of-work chain.** — 用户只需保存最长工作量证明链的区块头。
- **He also needs the Merkle branch that links his transaction to its block.** — 他还需要把这笔交易连到所属区块的默克尔分支。
- **He cannot audit the transaction himself — he sees that the network accepted it.** — 他自己审不了这笔交易——他看到的是网络已经接受了它。
- **Later blocks stacked on top make the payment more convincing.** — 后面再叠上的块，让这笔付款更令人信服。
- **This is reliable while honest nodes control the network.** — 只要诚实节点掌控网络，这一套就可靠。
- **For extra safety, a business can run its own node.** — 为了更稳，商家可以自己跑一个节点。

---

## 9. Combining and Splitting Value — 合并与拆分价值

Coins are not handled one by one. A transaction has **inputs** and **outputs**.

币不会一枚一枚单独伺候。一笔交易有输入和输出。

- **Handling coins one by one would be unwieldy.** — 一枚一枚处理会笨拙得要命。
- **A transaction typically has several inputs and one or two outputs.** — 一笔交易通常有多个输入，以及一到两个输出。
- **Inputs can combine smaller amounts, or take a slice from a larger previous output.** — 输入可以拼小额，也可以从上一笔较大输出里切一块。
- **One output pays the recipient; the other returns change to the sender.** — 一个输出付给收款人；另一个把找零退给付款人。

---

## 10. Privacy — 隐私

The ledger is public. Identity does not have to be.

账本是公开的。身份不必公开。

- **Traditional banks keep privacy by hiding the ledger from the public.** — 传统银行靠对公众隐藏账本来保护隐私。
- **Bitcoin cannot hide the ledger — every transaction is announced.** — 比特币藏不住账本——每笔交易都要公布。
- **Privacy still works if public keys stay anonymous.** — 只要公钥保持匿名，隐私仍然成立。
- **The public sees that someone sent an amount to someone else — not who.** — 公众看见「有人给了某人一笔钱」——看不见是谁。
- **That is a bit like a stock-exchange tape: size and time, not names.** — 有点像交易所行情带：有数量和时间，没有名字。
- **Use a new key pair for each transaction as an extra firewall.** — 每笔交易换一对新密钥，当作额外防火墙。
- **Multi-input transactions still leak that those inputs had the same owner.** — 多输入交易仍会泄露：这些输入曾属于同一人。
- **If one key gets tied to a person, other linked spends can leak too.** — 若一把密钥对上了真人，其他关联花费也可能露馅。

---

## 11. Calculations — 计算

Can an attacker catch up from behind? The paper treats it like **Gambler's Ruin**.

攻击者能不能从落后位置追上来？论文把它当成赌徒破产问题。

- **Let p be the chance an honest node finds the next block.** — 设 p 为诚实节点挖出下一块的概率。
- **Let q be the chance the attacker finds the next block.** — 设 q 为攻击者挖出下一块的概率。
- **If p is greater than q, the attacker's odds of ever catching up drop exponentially.** — 若 p 大于 q，攻击者追上的概率会指数下降。
- **The recipient waits for z blocks to pile on after the payment.** — 收款人等这笔付款上面再叠上 z 个块。
- **Six confirmations became the later street rule of thumb — the paper is more careful.** — 「六次确认」后来成了街头经验法则——论文本身算得更细。
- **If the attacker has far less than half the CPU power, waiting a few blocks is enough.** — 若攻击者远不到一半算力，再等几个块就够了。

---

## 12. Conclusion — 结论

The last page restates the bet: signatures for ownership, proof-of-work for history, no trusted party.

末页重申这个赌注：签名管所有权，工作量证明管历史，不靠可信第三方。

- **The paper proposes electronic transactions that do not rely on trust.** — 论文提出不依赖信任的电子交易。
- **Digital signatures give strong control of ownership.** — 数字签名对所有权控制很强。
- **That is incomplete without a way to stop double-spending.** — 若挡不住双花，这套仍不完整。
- **A peer-to-peer network records a public history with proof-of-work.** — 点对点网络用工作量证明记下公开历史。
- **If honest nodes hold most CPU power, changing that history soon becomes impractical.** — 若诚实节点掌握大部分算力，改历史很快就不现实。
- **The network is robust in its unstructured simplicity.** — 网络靠「结构很松」反而稳健。
- **Nodes work at once with little coordination.** — 节点几乎不协调，却能一起干活。
- **They do not need to be identified, and they can leave and rejoin.** — 它们不必亮身份，也可以离开再回来。
- **They vote with CPU power, expressing acceptance of valid blocks.** — 它们用 CPU 算力投票，表示接受有效区块。

---

## 术语表 — Vocabulary

论文原词优先；括号里是后来圈内口头禅，方便和 [[learning-notes/personal-english-book/investing/crypto-exchange-app-scenarios|交易所 APP]] 对照。

| 英文 | IPA（美） | 简中 | 记忆 / 例句 |
|------|-----------|------|-------------|
| **peer-to-peer** `术语` | /ˌpɪr tə ˈpɪr/ | 点对点 | **Peer-to-peer** cash skips the bank. 点对点现金跳过银行。 |
| **electronic cash** `术语` | /ɪˌlekˈtrɑːnɪk kæʃ/ | 电子现金 | Bitcoin is **electronic cash**, not a company share. 比特币是电子现金，不是公司股票。 |
| **trusted third party** `术语` | /ˈtrʌstɪd θɜːrd ˈpɑːrti/ | 可信第三方 | Banks act as a **trusted third party**. 银行充当可信第三方。 |
| **double-spending** `术语` | /ˈdʌbl ˈspendɪŋ/ | 双花 | **Double-spending** is spending the same coin twice. 双花就是同一枚币花两次。 |
| **digital signature** `术语` | /ˈdɪdʒɪtl ˈsɪɡnətʃər/ | 数字签名 | A **digital signature** proves you authorized the spend. 数字签名证明你授权了这笔花费。 |
| **public key** `术语` | /ˈpʌblɪk kiː/ | 公钥 | The **public key** is the address others can see. 公钥是别人能看见的地址。 |
| **private key** `术语` | /ˈpraɪvət kiː/ | 私钥 | Never leak your **private key**. 私钥绝不能泄露。 |
| **hash** `术语` | /hæʃ/ | 哈希 | A **hash** fingerprints a chunk of data. 哈希给一段数据按指纹。 |
| **SHA-256** `术语` | /ʃɔː tuː ˈfɪfti sɪks/ | SHA-256 哈希算法 | Bitcoin's proof-of-work hunts a **SHA-256** hash. 比特币的工作量证明在找 SHA-256 哈希。 |
| **timestamp** `术语` | /ˈtaɪmstæmp/ | 时间戳 | A **timestamp** proves the data already existed. 时间戳证明数据当时已存在。 |
| **proof-of-work** `术语` | /pruːf əv wɜːrk/ | 工作量证明（PoW） | **Proof-of-work** is one-CPU-one-vote. 工作量证明是一 CPU 一票。 |
| **block** `术语` | /blɑːk/ | 区块 | Nodes collect transactions into a **block**. 节点把交易收进一个区块。 |
| **chain of proof-of-work** `术语` | /tʃeɪn əv pruːf əv wɜːrk/ | 工作量证明链 | The paper says **chain of proof-of-work**, not “blockchain.” 原文写工作量证明链，不是 blockchain。 |
| **node** `术语` | /noʊd/ | 节点 | A **node** can leave and rejoin the network. 节点可以离开再回来。 |
| **broadcast** `术语` | /ˈbrɔːdkæst/ | 广播 | New transactions are **broadcast** to nodes. 新交易向节点广播。 |
| **longest chain** `术语` | /ˈlɔːŋɡɪst tʃeɪn/ | 最长链 | Nodes treat the **longest chain** as truth. 节点把最长链当真相。 |
| **CPU power** `术语` | /siː piː juː ˈpaʊər/ | CPU 算力 | Honest **CPU power** must stay in the majority. 诚实算力必须占多数。 |
| **incentive** `术语` | /ɪnˈsentɪv/ | 激励 | The **incentive** is a new coin plus fees. 激励是新币加手续费。 |
| **transaction fee** `术语` | /trænˈzækʃn fiː/ | 交易手续费 | Input minus output is the **transaction fee**. 输入减输出就是手续费。 |
| **Merkle tree** `术语` | /ˈmɜːrkəl triː/ | 默克尔树 | A **Merkle tree** lets old blocks shrink. 默克尔树让旧块能瘦身。 |
| **block header** `术语` | /blɑːk ˈhedər/ | 区块头 | The **block header** holds the Merkle root. 区块头装着默克尔根。 |
| **simplified payment verification** `术语` | /ˈsɪmplɪfaɪd ˈpeɪmənt ˌverɪfɪˈkeɪʃn/ | 简易支付验证（SPV） | **SPV** checks a payment with headers only. SPV 只靠区块头核对付款。 |
| **Merkle branch** `术语` | /ˈmɜːrkəl bræntʃ/ | 默克尔分支 | A **Merkle branch** links a tx to its block. 默克尔分支把交易连到所属块。 |
| **input** `术语` | /ˈɪnpʊt/ | 交易输入 | Several **inputs** can fund one payment. 多个输入可以凑成一笔付款。 |
| **output** `术语` | /ˈaʊtpʊt/ | 交易输出 | One **output** pays; another returns change. 一个输出付款，另一个找零。 |
| **change** `术语` | /tʃeɪndʒ/ | 找零（输出） | The leftover goes back as **change**. 剩余以找零回去。 |
| **key pair** `术语` | /kiː per/ | 密钥对 | Use a fresh **key pair** per payment. 每笔付款换一对新密钥。 |
| **anonymous** `术语` | /əˈnɑːnɪməs/ | 匿名的 | Public keys can stay **anonymous**. 公钥可以保持匿名。 |
| **confirmation** `术语` | /ˌkɑːnfərˈmeɪʃn/ | 确认（后续区块） | Wait for more **confirmations** before you trust a big payment. 大额付款先等多几个确认。 |
| **attacker** `术语` | /əˈtækər/ | 攻击者 | An **attacker** must catch up from behind. 攻击者必须从落后位置追上来。 |

---

## 一分钟小结 — One-Minute Summary

- **Problem** — 网上付款靠银行当可信第三方；贵、可撤销、还怕双花。 — 白皮书要去掉中间人。
- **Coin** — 电子币 = 数字签名链；所有权可验证，双花仍要全网看见。 — 签名管「是谁的」，广播管「有没有花过」。
- **Clock** — 时间戳服务器把哈希串成链。 — 改过去的一块，后面全裂。
- **Vote** — 工作量证明 = 一 CPU 一票；最长链算数。 — 诚实算力占多数，攻击者追不上。
- **Pay** — 新币 + 手续费养活节点。 — 没有中央发行方。
- **Light** — 默克尔树瘦身；SPV 只拿区块头核对。 — 不全跑节点也能看付款。
- **Privacy** — 账本公开，公钥尽量匿名，最好每笔换钥。 — 透明的是金额，不是身份证。

---

## 朗读串联记忆 · Read-aloud chain

*约 1 分钟 · 按白皮书逻辑跟读 · 先英后对照简中*

### A. 分句场景链（按正文顺序朗读）

- **Bitcoin is peer-to-peer electronic cash — no bank in the middle.** — 比特币是点对点电子现金，中间没有银行。
- **The hard problem is double-spending.** — 真正的难题是双花。
- **An electronic coin is a chain of digital signatures.** — 电子币就是一串数字签名。
- **Proof-of-work is one-CPU-one-vote.** — 工作量证明等于一 CPU 一票。
- **Nodes always treat the longest chain as the correct one.** — 节点永远把最长链当作正确链。
- **Honest CPU power must stay in the majority.** — 诚实算力必须占多数。

### B. 一段串联（连续口语）

**Bitcoin is peer-to-peer electronic cash — no bank in the middle. The hard problem is double-spending. An electronic coin is a chain of digital signatures. Proof-of-work is one-CPU-one-vote. Nodes always treat the longest chain as the correct one. Honest CPU power must stay in the majority.**

**简中：** 比特币是点对点电子现金，中间没有银行。真正的难题是双花。电子币就是一串数字签名。工作量证明等于一 CPU 一票。节点永远把最长链当作正确链。诚实算力必须占多数。

### C. 一分钟复盘（5 句）

1. **Skip the trusted third party — send cash peer-to-peer.** — 跳过可信第三方，点对点寄现金。
2. **Signatures prove ownership; the chain stops double-spending.** — 签名证明所有权；链条挡住双花。
3. **Proof-of-work timestamps the public history.** — 工作量证明给公开历史盖时间戳。
4. **The longest chain wins if honest nodes have more CPU.** — 诚实节点算力更多，最长链就赢。
5. **New coins and fees keep the nodes working.** — 新币和手续费让节点继续干活。
