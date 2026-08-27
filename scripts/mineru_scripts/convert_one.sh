#!/usr/bin/env bash
# ============================================================
# convert_one.sh — MinerU 单文件 PDF 转 Markdown (timeout fix + TCP health check)
# 用法:
#   ./convert_one.sh <input.pdf> [output_dir] [gpu_id]
#   API_URL=http://127.0.0.1:8000 ./convert_one.sh <input.pdf> [output_dir]
#   START_PAGE=0 END_PAGE=229 ./convert_one.sh <input.pdf> [output_dir] [gpu_id]
# ============================================================
set -euo pipefail

# ============== 可修改的配置 ==============
WORK_ROOT="TODO: modify/to/your/path"
CONFIG_JSON="$WORK_ROOT/mineru.json"
DEFAULT_OUTPUT="$WORK_ROOT/md_output"

BACKEND="pipeline"
METHOD="auto"
LANG="ch"
FORMULA="true"
TABLE="true"
START_PAGE="${START_PAGE:-}"
END_PAGE="${END_PAGE:-}"

# === 关键修复：客户端轮询超时（秒）===
export MINERU_TASK_RESULT_TIMEOUT_SECONDS="${MINERU_TASK_RESULT_TIMEOUT_SECONDS:-21600}"

# === --api-url 模式 ===
API_URL="${API_URL:-}"

# === API 健康检查等待（仅 API_URL 模式；TCP 端口探测，不依赖 curl 或特定 HTTP 端点）===
API_WAIT_TIMEOUT="${API_WAIT_TIMEOUT:-300}"   # 最多等 5 分钟
API_WAIT_INTERVAL="${API_WAIT_INTERVAL:-3}"   # 每 3 秒探一次
# =========================================================

info() { printf "\033[36m[INFO]\033[0m %s\n" "$*"; }
ok()   { printf "\033[32m[ OK ]\033[0m %s\n" "$*"; }
err()  { printf "\033[31m[ERR ]\033[0m %s\n" "$*" >&2; }

# 从 URL 提取 host 和 port（用于 TCP 探测）
parse_host_port() {
    local url="$1" host port
    url="${url#http://}"; url="${url#https://}"
    url="${url%%/*}"
    if [[ "$url" == *:* ]]; then
        host="${url%%:*}"; port="${url##*:}"
    else
        host="$url"; port="${url:+80}"
    fi
    echo "$host $port"
}

INPUT="${1:-}"
[[ -z "$INPUT" ]] && { err "用法: $0 <input.pdf> [output_dir] [gpu_id]"; exit 1; }
[[ ! -f "$INPUT" ]] && { err "文件不存在: $INPUT"; exit 1; }

OUTPUT_DIR="${2:-$DEFAULT_OUTPUT}"
GPU_ID="${3:-}"

export MINERU_TOOLS_CONFIG_JSON="$CONFIG_JSON"
export MINERU_MODEL_SOURCE=local
export MINERU_DEVICE_MODE=cuda

if [[ -z "$API_URL" ]]; then
    if [[ -z "$GPU_ID" ]]; then
        GPU_ID=$(nvidia-smi --query-gpu=index,memory.free --format=csv,nounits,noheader \
                | sort -t',' -k2 -nr | head -1 | awk -F',' '{gsub(/ /,"",$1); print $1}')
        info "未指定 GPU，自动选择空闲最多的: GPU $GPU_ID"
    fi
    export CUDA_VISIBLE_DEVICES="$GPU_ID"
else
    # === API_URL 模式：提交前用 TCP 探测等端口就绪 ===
    read -r API_HOST API_PORT <<< "$(parse_host_port "$API_URL")"
    info "等待 API 就绪: ${API_HOST}:${API_PORT} (最多 ${API_WAIT_TIMEOUT}s)"
    waited=0
    until timeout 2 bash -c "echo > /dev/tcp/${API_HOST}/${API_PORT}" 2>/dev/null; do
        sleep "$API_WAIT_INTERVAL"
        waited=$((waited + API_WAIT_INTERVAL))
        if [[ "$waited" -ge "$API_WAIT_TIMEOUT" ]]; then
            err "API 在 ${API_WAIT_TIMEOUT}s 内未就绪: ${API_HOST}:${API_PORT}"
            err "请检查 start_api.sh 是否已启动且端口正确"
            exit 1
        fi
    done
    ok "API 已就绪 (等待了 ${waited}s)"
fi

ARGS=(-p "$INPUT" -o "$OUTPUT_DIR" -b "$BACKEND" -m "$METHOD" -l "$LANG" -f "$FORMULA" -t "$TABLE")
[[ -n "$START_PAGE" ]] && ARGS+=(-s "$START_PAGE")
[[ -n "$END_PAGE"   ]] && ARGS+=(-e "$END_PAGE")
[[ -n "$API_URL"    ]] && ARGS+=(--api-url "$API_URL")

mkdir -p "$OUTPUT_DIR"
info "开始转换"
info "  输入: $INPUT"
info "  输出: $OUTPUT_DIR"
if [[ -n "$API_URL" ]]; then
    info "  模式: 常驻服务 (--api-url=$API_URL)  ← 超时不会丢进度"
else
    info "  GPU:  $GPU_ID  (旧模式，长 PDF 建议用 --api-url)"
fi
info "  超时上限: ${MINERU_TASK_RESULT_TIMEOUT_SECONDS}s  后端: $BACKEND  方法: $METHOD  语言: $LANG"

START_TS=$(date +%s)
if mineru "${ARGS[@]}"; then
    ok "完成 (耗时 $(($(date +%s) - START_TS))s)"
else
    err "转换失败"
    [[ -n "$API_URL" ]] && err "服务端任务仍在跑，可稍后用同一命令重试取回结果"
    exit 1
fi
