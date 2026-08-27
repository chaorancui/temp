#!/usr/bin/env bash
# ============================================================
# convert_dir.sh — 批量转换目录下所有 PDF
# 用法:
#   ./convert_dir.sh <input_dir> [output_dir] [gpu_id]
#   API_URL=http://127.0.0.1:8000 ./convert_dir.sh <input_dir> [output_dir]
# ============================================================
set -euo pipefail
WORK_ROOT="TODO: modify/to/your/path"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONVERT_ONE="$SCRIPT_DIR/convert_one.sh"

# 继承超时修复
export MINERU_TASK_RESULT_TIMEOUT_SECONDS="${MINERU_TASK_RESULT_TIMEOUT_SECONDS:-21600}"

info() { printf "\033[36m[INFO]\033[0m %s\n" "$*"; }
ok()   { printf "\033[32m[ OK ]\033[0m %s\n" "$*"; }
err()  { printf "\033[31m[ERR ]\033[0m %s\n" "$*" >&2; }

INPUT_DIR="${1:-}"
[[ -z "$INPUT_DIR" ]] && { err "用法: $0 <input_dir> [output_dir] [gpu_id]"; exit 1; }
[[ ! -d "$INPUT_DIR" ]] && { err "输入目录不存在: $INPUT_DIR"; exit 1; }
[[ ! -x "$CONVERT_ONE" ]] && { err "找不到可执行的 convert_one.sh: $CONVERT_ONE"; exit 1; }

OUTPUT_DIR="${2:-$WORK_ROOT/md_output}"
GPU_ID="${3:-}"
mkdir -p "$OUTPUT_DIR"

mapfile -t PDFS < <(find "$INPUT_DIR" -maxdepth 1 -type f -iname '*.pdf' | sort)
COUNT=${#PDFS[@]}
[[ "$COUNT" -eq 0 ]] && { err "目录中无 PDF: $INPUT_DIR"; exit 1; }

info "找到 $COUNT 个 PDF，开始批量转换"
[[ -n "${API_URL:-}" ]] && info "  使用 API 模式: $API_URL"

SUCCESS=0; FAILED=0; FAILED_LIST=()
for pdf in "${PDFS[@]}"; do
    name=$(basename "$pdf" .pdf)
    info "[$((SUCCESS+FAILED+1))/$COUNT] 转换: $name"
    if "$CONVERT_ONE" "$pdf" "$OUTPUT_DIR/$name" "$GPU_ID"; then
        SUCCESS=$((SUCCESS+1))
        ok "  成功: $name"
    else
        FAILED=$((FAILED+1))
        FAILED_LIST+=("$name")
        err "  失败: $name"
    fi
done

echo "================================================================"
ok "完成: 成功 $SUCCESS / 失败 $FAILED / 总计 $COUNT"
if [[ "$FAILED" -gt 0 ]]; then
    err "失败列表:"
    printf '  - %s\n' "${FAILED_LIST[@]}"
    exit 1
fi
