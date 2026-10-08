---
name: privacy-check
description: >-
  Redacts personal and child privacy before writing documents and before any
  git commit. Checks Chinese personal names, addresses, schools, class
  identifiers, companies, streets, bank card numbers, and national ID numbers.
  Use when creating or editing notes, Markdown, or other documents, and when
  the user asks to commit, stage, or push.
---

# Privacy check

Run this **before saving document text** and **again on the diff before `git add` / `git commit`**. A hit blocks the commit. Do not commit first and clean up later.

This repo publishes learning notes. Class numbers, school names, and real names can identify the child. Treat the tree as shareable.

## Allowed labels

Only these stand in for the family. Do not introduce other real personal names.

| Who | Allowed |
| --- | --- |
| Learner | **阿泽**，同事称呼 **泽哥** |
| Child | **不多**，英文名 **Celine** |

City-level **深圳** is allowed when the note is about daily life there. Do not add a district, community, street, or building that narrows it to a home.

## Block list

Strip or generalize. Do not leave the raw value in the file, the commit message, or the chat summary. For card numbers and ID numbers, report only the category and file, never the full number.

| Kind | Examples to catch | Write instead |
| --- | --- | --- |
| Chinese personal names | 真名、家人、老师、同学、同事的中文姓名 | 阿泽 / 泽哥 / 不多 / Celine，或「老师」「同学」 |
| Address | 省市区以下的住址、小区、楼栋、房号 | 「家里」「我们小区」 |
| School | 学校全名、校区名 | 「学校」 |
| Class | `四（2）班`、`四(2)班`、年级加班号 | 「本班」「本学期课表」 |
| Company | 雇主、客户、产品内部代号 | `Company A`，或只写角色 |
| Street | 路、街、道、巷、门牌 | 删掉 |
| Card number | 银行卡、信用卡连续数字 | 删掉 |
| National ID | 身份证号、护照号 | 删掉 |
| Also block | 手机号、邮箱、带 token 的 URL、学号、工号 | 删掉或换成 `user@example.com` |

Generic words are fine: **小学**、**学校**、**公司** as vocabulary, with no real proper name attached.

## When writing a document

1. Scan the text you are about to write, including filenames, link text, PDF names, and image alt text.
2. Replace hits before the file is written.
3. If the user pasted a secret, redact the document and do not repeat the secret back.

## Before a commit

1. Read the staged and unstaged diff (`git diff` and `git diff --cached`), plus untracked files you plan to add.
2. Run the pattern scan:

```bash
python3 .cursor/skills/privacy-check/scripts/scan_privacy.py
```

3. Also read the diff yourself for Chinese names, school names, company names, and streets. The script does not understand names.
4. If anything hits: do **not** commit. Fix the files, scan again, then commit only the cleaned diff.
5. Commit messages stay free of the same details.

Exit code 0 means the script found no pattern hits. It does not mean the name and school review is done.
