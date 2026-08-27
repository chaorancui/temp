#!/usr/bin/env bash
# ============================================================
# start_api.sh — 启动常驻 mineru-api 服务（终端1运行，长开不退出）
# 用法: ./start_api.sh [gpu_id] [port]
#   默认: gpu_id=自动选空闲最多的, port=8000
# ============================================================
set -euo pipefail
WORK_ROOT="TODO: /modify/to/your/path"
GPU_ID="${1:-}"; PORT="${2:-8000}"

export MINERU_TOOLS_CONFIG_JSON="$WORK_ROOT/mineru.json"
export MINERU_MODEL_SOURCE=local
export MINERU_DEVICE_MODE=cuda
# 关键：服务端任务保留 24 小时，客户端轮询超时 6 小时
export MINERU_TASK_RESULT_TIMEOUT_SECONDS=21600
export MINERU_API_TASK_RETENTION_SECONDS=86400

if [[ -z "$GPU_ID" ]]; then
    GPU_ID=$(nvidia-smi --query-gpu=index,memory.free --format=csv,nounits,noheader \
            | sort -t',' -k2 -nr | head -1 | awk -F',' '{gsub(/ /,"",$1); print $1}')
fi
export CUDA_VISIBLE_DEVICES="$GPU_ID"

echo "[INFO] 启动 mineru-api on 127.0.0.1:$PORT  (GPU $GPU_ID)"
echo "[INFO] 此窗口须保持打开。转换用另一窗口提交。"
echo "[INFO] 按 Ctrl+C 退出服务。"

if command -v mineru-api >/dev/null 2>&1; then
    exec mineru-api --host 127.0.0.1 --port "$PORT"
elif mineru api --help >/dev/null 2>&1; then
    exec mineru api --host 127.0.0.1 --port "$PORT"
else
    echo "[ERR] 既无 mineru-api 也无 'mineru api' 子命令，请检查 MinerU 安装" >&2
    exit 1
fi
