#!/bin/zsh
# 停止 serve_notes.sh 启动的本地英语学习笔记网站。
set -euo pipefail
PORT="${NOTES_PORT:-8766}"
PIDS="$(lsof -ti "tcp:${PORT}" -sTCP:LISTEN 2>/dev/null || true)"
if [[ -z "${PIDS}" ]]; then
  echo "笔记网站未在运行（端口 ${PORT}）"
  exit 0
fi
kill ${=PIDS}
echo "已停止笔记网站（端口 ${PORT}，PID ${PIDS//$'\n'/ }）"
