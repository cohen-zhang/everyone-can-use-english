#!/usr/bin/env bash
# 台词/课程文本按集拆分：
#   · S01Exx（如摩登家庭）→ 摩登家庭 S01/摩登家庭 S01-xx.txt
#   · Episode N（如 ESLPod）→ <源文件名去后缀>/Episode NN – 副标题.txt（遇「Table of Contents」后不再拆分）
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${1:-$SCRIPT_DIR/摩登家庭S1.txt}"

if [[ ! -f "$SRC" ]]; then
  echo "找不到源文件: $SRC" >&2
  exit 1
fi

detect_mode() {
  local f="$1"
  local line
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ "$line" =~ ^S01E[0-9][0-9] ]] && echo mf && return
    [[ "$line" =~ ^Episode[[:space:]]+[0-9]+ ]] && echo jeff && return
  done <"$f"
  echo "无法识别格式：未找到 S01Exx 或 Episode N 行首标记" >&2
  return 1
}

MODE="$(detect_mode "$SRC")" || exit 1

case "$MODE" in
mf)
  OUT_DIR="$SCRIPT_DIR/摩登家庭 S01"
  mkdir -p "$OUT_DIR"
  awk -v dir="$OUT_DIR" '
    /^S01E[0-9][0-9]/ {
      if (out != "") close(out)
      ep = substr($0, 5, 2)
      out = dir "/摩登家庭 S01-" ep ".txt"
    }
    out != "" { print > out }
  ' "$SRC"
  ;;
jeff)
  base="$(basename "$SRC")"
  base="${base%.txt}"
  OUT_DIR="$SCRIPT_DIR/$base"
  mkdir -p "$OUT_DIR"
  awk -v dir="$OUT_DIR" '
    /^Table of Contents$/ {
      if (out != "") close(out)
      out = ""
      toc = 1
      next
    }
    toc { next }
    /^Episode[[:space:]]+[0-9]+/ {
      if (out != "") close(out)
      line = $0
      sub(/^Episode[[:space:]]+/, "", line)
      ep = sprintf("%02d", line + 0)
      title = line
      sub(/^[0-9]+/, "", title)
      sub(/^[[:space:]]*[–—-][[:space:]]*/, "", title)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", title)
      gsub(/\//, "-", title)
      gsub(/:/, " -", title)
      if (title == "")
        out = dir "/Episode " ep ".txt"
      else
        out = dir "/Episode " ep " – " title ".txt"
    }
    out != "" { print > out }
  ' "$SRC"
  ;;
*)
  echo "内部错误: 未知模式 $MODE" >&2
  exit 1
  ;;
esac

echo "已写入目录: $OUT_DIR"
