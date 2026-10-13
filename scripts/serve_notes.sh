#!/bin/zsh
# 启动本地英语学习笔记网站（MkDocs Material）并在浏览器打开；已在运行则直接打开。
#   zsh scripts/serve_notes.sh            # 后台启动 + 打开浏览器
#   zsh scripts/serve_notes.sh --no-open  # 只启动
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PATH="${HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${PATH}"

PORT="${NOTES_PORT:-8766}"
URL="http://127.0.0.1:${PORT}/"
VENV="${NOTES_VENV:-${HOME}/.venvs/english-notes}"
LOG_DIR="${ROOT}/logs"
LOG="${LOG_DIR}/notes-site.log"
mkdir -p "${LOG_DIR}"

open_browser() {
  [[ "${1:-}" == "--no-open" ]] || open "${URL}"
}

if curl -fsS -o /dev/null "${URL}" 2>/dev/null; then
  open_browser "${1:-}"
  exit 0
fi

if [[ ! -x "${VENV}/bin/mkdocs" ]]; then
  echo "首次运行：安装笔记网站依赖到 ${VENV}" >>"${LOG}"
  uv venv "${VENV}" --python 3.12 >>"${LOG}" 2>&1
  uv pip install --python "${VENV}" -r "${ROOT}/requirements-docs.txt" >>"${LOG}" 2>&1
fi

echo "===== $(date '+%Y-%m-%d %H:%M:%S') serve on ${URL} =====" >>"${LOG}"
nohup "${VENV}/bin/mkdocs" serve -f "${ROOT}/mkdocs.yml" -a "127.0.0.1:${PORT}" --dirty \
  >>"${LOG}" 2>&1 </dev/null &

# 全站首次构建较慢（字幕页、jieba 分词），最多等 3 分钟。
for _ in {1..360}; do
  if curl -fsS -o /dev/null "${URL}" 2>/dev/null; then
    open_browser "${1:-}"
    exit 0
  fi
  sleep 0.5
done

echo "笔记网站 3 分钟内未就绪，查看日志：${LOG}" >&2
exit 1
