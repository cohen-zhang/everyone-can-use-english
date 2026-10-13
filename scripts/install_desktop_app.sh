#!/bin/zsh
# 在桌面生成「英语学习笔记.app」：双击后台启动本地笔记网站并打开浏览器。
#   zsh scripts/install_desktop_app.sh            # -> ~/Desktop/英语学习笔记.app
#   APP_DIR=/Applications zsh scripts/install_desktop_app.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR="${APP_DIR:-${HOME}/Desktop}"
APP_NAME="英语学习笔记"
APP="${APP_DIR}/${APP_NAME}.app"
ICON_PNG="${ROOT}/scripts/assets/notes-icon.png"
SERVE="${ROOT}/scripts/serve_notes.sh"

WORK="$(mktemp -d)"
trap 'rm -rf "${WORK}"' EXIT

# AppleScript 字符串里的反斜杠和双引号需要转义。
SERVE_AS="${SERVE//\\/\\\\}"
SERVE_AS="${SERVE_AS//\"/\\\"}"
cat >"${WORK}/main.applescript" <<EOF
try
	do shell script "/bin/zsh " & quoted form of "${SERVE_AS}"
on error errMsg
	display dialog "笔记网站启动失败：" & return & errMsg buttons {"好"} default button 1 with icon caution
end try
EOF
osacompile -o "${WORK}/${APP_NAME}.app" "${WORK}/main.applescript"

ICONSET="${WORK}/notes.iconset"
mkdir -p "${ICONSET}"
for size in 16 32 128 256 512; do
  sips -z "${size}" "${size}" "${ICON_PNG}" --out "${ICONSET}/icon_${size}x${size}.png" >/dev/null
  double=$((size * 2))
  sips -z "${double}" "${double}" "${ICON_PNG}" --out "${ICONSET}/icon_${size}x${size}@2x.png" >/dev/null
done
iconutil -c icns "${ICONSET}" -o "${WORK}/${APP_NAME}.app/Contents/Resources/applet.icns"
rm -f "${WORK}/${APP_NAME}.app/Contents/Resources/Assets.car"
/usr/libexec/PlistBuddy -c "Delete :CFBundleIconName" "${WORK}/${APP_NAME}.app/Contents/Info.plist" 2>/dev/null || true
codesign --force --deep --sign - "${WORK}/${APP_NAME}.app" 2>/dev/null

rm -rf "${APP}"
mkdir -p "${APP_DIR}"
cp -R "${WORK}/${APP_NAME}.app" "${APP}"
touch "${APP}"
echo "已生成 ${APP}"
