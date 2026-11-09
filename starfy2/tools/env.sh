# Optional; build.sh sources this before running Atlas/lzss.
# WINE_BIN=/path/to/wine/bin   use a portable wine build that is not on PATH (optional)
# WINEPREFIX=/path             wine prefix to use (default: tools/wineprefix)
_STAFY_TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${WINE_BIN:-}" && -x "$WINE_BIN/wine" ]]; then
  case ":$PATH:" in *":$WINE_BIN:"*) ;; *) export PATH="$WINE_BIN:$PATH";; esac
fi
export WINEPREFIX="${WINEPREFIX:-$_STAFY_TOOLS/wineprefix}"
export WINEDEBUG=-all
export WINEDLLOVERRIDES="mscoree,mshtml=;winedbg.exe=d"
unset DISPLAY
# Keep one wineserver alive; warm up once so the first Atlas call does not hang.
if command -v wineserver >/dev/null 2>&1; then
  wineserver -p 300 2>/dev/null || true
fi
if command -v wine >/dev/null 2>&1 && [[ "${STAFY_WINE_WARMED:-}" != 1 ]]; then
  wine cmd /c echo ok >/dev/null 2>&1 || true
  export STAFY_WINE_WARMED=1
fi
unset _STAFY_TOOLS
