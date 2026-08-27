[TOC]

## MinerU 部署与使用

📋 关键事实（研究结论）

| 项         | 值                                                                      | 说明                                                 |
| ---------- | ----------------------------------------------------------------------- | ---------------------------------------------------- |
| 包名       | mineru（非 magic-pdf）                                                  | 2025-06-13 已改名；magic-pdf 1.3.12 是最后一个旧版   |
| 当前稳定版 | mineru 3.4.5（2026-08-14）                                              | 需要 Python ≥3.10, <3.14                             |
| 配置文件   | ~/mineru.json（非 magic-pdf.json）                                      | 路径可用 MINERU_TOOLS_CONFIG_JSON 环境变量覆盖       |
| 默认后端   | hybrid-engine（pipeline+vlm）                                           | 纯 PDF→MD 用 pipeline 后端即可（更轻、CPU/GPU 通用） |
| 模型包     | HF opendatalab/PDF-Extract-Kit-1.0 / MS OpenDataLab/PDF-Extract-Kit-1.0 | ✅ 与你下载的包名一致                                |
| GPU 选择   | 环境变量 MINERU_DEVICE_MODE=cuda 或 CUDA_VISIBLE_DEVICES=0 前缀         | 自动检测亦可                                         |
| 旧依赖     | 不再需要 paddleocr / paddlepaddle-gpu                                   | v3+ 改用 onnxruntime + PyTorch OCR                   |

## P1 - MinerU 安装与配置

**一、安装 MinerU 及其完整依赖**

```bash
# 1. 创建隔离环境 mineru
conda create -n mineru python=3.10 -y
conda activate mineru

# 2. 安装 MinerU 及其完整依赖
pip install -U "mineru[all]"

# 3. 安装匹配服务器 CUDA 12.2 的 PyTorch (使用 cu121)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 确保 huggingface-hub 在 transformers 要求的区间
pip install -U "huggingface-hub>=0.34.0,<1.0"


#### uv pip 加速安装 ####
# 2. 安装 uv 加速包管理（配置 uv 源）
pip install --upgrade pip uv

# 3. 安装 MinerU 及其所有功能模块
uv pip install -U "mineru[all]"

# 4. 安装适合你服务器（CUDA 12.2 驱动）的 PyTorch
uv pip uninstall torch torchvision
uv pip install -U torch==2.6.0 torchvision==0.21.0 \
    --index-url https://pypi.org/simple \
    --extra-index-url https://download.pytorch.org/whl/cu121

# 确保 huggingface-hub 在 transformers 要求的区间
uv pip install -U "huggingface-hub>=0.34.0,<1.0"
```

**二、下载模型权重（推荐 ModelScope 国内镜像）**

MinerU 3.x 需要仓库 PDF-Extract-Kit-1.0/models/ 下的模型。

```bash
#### 国内推荐 modelscope；海外用 huggingface
# 1. modelscope
pip install modelscope
modelscope download --model OpenDataLab/PDF-Extract-Kit-1.0 --local_dir ./

# 2. huggingface_hub
pip install huggingface_hub
from huggingface_hub import snapshot_download
snapshot_download(repo_id='opendatalab/pdf-extract-kit-1.0', local_dir='./', max_workers=20)


#### 下载后确认下面 6 个子模型存在
MODELS_ROOT=<TODO: modify to your path>/PDF-Extract-Kit-1.0
# 必须存在的 6 个路径（MinerU 3.x 实际加载的）
ls "$MODELS_ROOT/models/Layout/PP-DocLayoutV2/"                       # 版面布局（替代了旧的 layoutreader）
ls "$MODELS_ROOT/models/MFR/unimernet_hf_small_2503/"                  # 公式识别（默认 MFR）
ls "$MODELS_ROOT/models/MFR/pp_formulanet_plus_m/"                    # 公式识别（中文，可选）
ls "$MODELS_ROOT/models/OCR/paddleocr_torch/"                         # OCR（PyTorch 后端，非 paddle）
ls "$MODELS_ROOT/models/TabRec/SlanetPlus/slanet-plus.onnx"            # 无线表格识别
ls "$MODELS_ROOT/models/TabRec/UnetStructure/unet.onnx"                # 有线表格识别
ls "$MODELS_ROOT/models/TabCls/paddle_table_cls/PP-LCNet_x1_0_table_cls.onnx"  # 表格分类

# 如果以上路径缺失（尤其是 PP-DocLayoutV2、unimernet_hf_small_2503、paddleocr_torch），说明下载的是旧版模型包，需要更新：
mineru-models-download -s modelscope -m pipeline
```

**三、创建配置文件 mineru.json**

你的个人目录不在家目录下，建议把配置放到个人目录，用环境变量指向它：

```bash
# 创建配置文件
cat > <TODO: modify to your path>/mineru.json <<'EOF'
{
      "models-dir": {
         "pipeline": "<TODO: modify to your path>/PDF-Extract-Kit-1.0",
         "vlm": ""
      },
      "model-source": "local",
      "latex-delimiter-config": {
         "display": { "left": "$$", "right": "$$" },
         "inline":  { "left": "$",  "right": "$"  }
      },
      "llm-aided-config": {
         "title_aided": { "enable": false }
      },
      "config_version": "1.3.2"
}
EOF
```

关键字段说明：

- models-dir.pipeline = PDF-Extract-Kit-1.0 的根目录（包含 models/ 的那一层，不是 models/ 本身）
- model-source: "local" = 使用本地已下载模型，不联网下载
- models-dir.vlm 留空 = 不启用 VLM 后端（纯 PDF→MD 用不到）

**四、设置环境变量（建议写进 ~/.bashrc 或 conda env 的 activate 脚本）**

```bash
# 配置文件路径
export MINERU_TOOLS_CONFIG_JSON=<TODO: modify to your path>/mineru.json

# 强制使用本地模型（覆盖 config 的 model-source）
export MINERU_MODEL_SOURCE=local

# GPU 设备（可选；不设则自动检测 cuda）
export MINERU_DEVICE_MODE=cuda

# 如果公式以中文为主，启用中文公式识别模型（可选）
# export MINERU_FORMULA_CH_SUPPORT=true

# 指定某张 GPU（多卡时）
# export CUDA_VISIBLE_DEVICES=0
# 应用环境变量：
source ~/.bashrc
conda activate mineru
```

验证安装：

```bash
# 查看 CLI 帮助
mineru --help

# 查看版本
mineru --version
```

## P2 — PDF 转 MD

### 脚本

> 注意：直接转换大文件时可能会失败。
> mineru CLI 客户端有个硬编码的 60 分钟轮询超时，时间一到就放弃，导致已完成的部分全部丢失。推荐使用如下常驻服务的方式。

#### 启动服务

**`start_api.sh` - 启动常驻 mineru-api 服务**

```bash
#!/usr/bin/env bash
# ============================================================
# start_api.sh — 启动常驻 mineru-api 服务（终端1运行，长开不退出）
# 用法: ./start_api.sh [gpu_id] [port]
#   默认: gpu_id=自动选空闲最多的, port=8000
# ============================================================
set -euo pipefail
WORK_ROOT="<TODO: modify to your path>"
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

```

#### 单文件脚本

**`convert_one.sh` - 单文件脚本**

```bash
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
WORK_ROOT="<TODO: modify to your path>"
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

```

#### 整个目录脚本

```bash
#!/usr/bin/env bash
# ============================================================
# convert_dir.sh — 批量转换目录下所有 PDF
# 用法:
#   ./convert_dir.sh <input_dir> [output_dir] [gpu_id]
#   API_URL=http://127.0.0.1:8000 ./convert_dir.sh <input_dir> [output_dir]
# ============================================================
set -euo pipefail
WORK_ROOT="<TODO: modify to your path>"
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

```

### 使用流程

#### 启动常驻 API

**(1) 终端 1 — 启动常驻 API（保持窗口开着不关）**

```bash
conda activate mineru
# 自动选最空闲GPU，默认端口 8000
./mineru_scripts/start_api.sh
# 手动指定
./mineru_scripts/start_api.sh 7 8000
```

参数说明：

- 7 = 用 GPU 7（看你 Block 1 的 nvidia-smi 输出，选空闲最多的那块；被 healthLora 占的就别选）
- 8000 = API 端口

预期输出：

```log
[INFO] 启动 mineru-api on 127.0.0.1:8000  (GPU 7)
[INFO] 此窗口须保持打开。转换用另一窗口提交。
[INFO] 按 Ctrl+C 退出服务。
INFO:     Uvicorn running on http://127.0.0.1:8000
```

看到 Uvicorn running 后不要关这个窗口，打开终端 2。

#### 提交转换任务

**(2) 终端 2 — 提交转换任务**

```bash
conda activate mineru

API_URL=http://127.0.0.1:8000 \
  ./mineru_scripts/convert_one.sh \
  "pdf_input/DaVinci AIC V510 ISA User Guide for Guangzhou AIC.pdf"
```

预期流程：

1. 等待 API 就绪: 127.0.0.1:8000 (最多 300s) → 几秒后 API 已就绪
2. 开始转换 → 输入/输出路径打印
3. 模式: 常驻服务 (--api-url=...) ← 超时不会丢进度
4. MinerU 加载模型（约 2-5 分钟，期间 GPU 显存涨到 ~10-15GB）
5. 开始处理 PDF（920 页，约 1-6 小时，看 GPU 利用率）
6. 完成 (耗时 XXXXs)

关键：即使终端 2 的 mineru 客户端因为某些原因退出，服务端任务还在跑。 你可以稍后用同一条命令再取回结果（如果服务端任务还在 MINERU_API_TASK_RETENTION_SECONDS=86400 秒保留期内）。

#### 分批跑（可选）

**(3) 分批跑 — 如果 920 页单次还是失败（可选）**

```bash
# 终端 2 - 第 1 批: 0-229 页
API_URL=http://127.0.0.1:8000 START_PAGE=0 END_PAGE=229 \
  ./mineru_scripts/convert_one.sh "pdf_input/DaVinci AIC V510 ISA User Guide for Guangzhou AIC.pdf" md_output_part1

# 等 part1 完成后再跑第 2 批
API_URL=http://127.0.0.1:8000 START_PAGE=230 END_PAGE=459 \
  ./mineru_scripts/convert_one.sh "pdf_input/DaVinci AIC V510 ISA User Guide for Guangzhou AIC.pdf" md_output_part2

# 以此类推，4 批跑完 920 页
```

注意：-s 和 -e 是 0 索引页 ID（不是页码），即第 1 页是 0。

#### 后处理脚本

**(4) 后处理脚本**

可解决：

- 大纲不对
- 寄存器位域说明
- 代码块不对

```bash
# Activate the conda env (for Python 3.10+)
conda activate mineru

# Option A: Auto-detect mode (pass the auto/ directory, output goes to <basename>_fixed.md)
python3 ./mineru_scripts/postprocess_mineru.py \
  "<TODO: modify to your path>/md_output/DaVinci AIC V510 ISA User Guide for Guangzhou AIC/auto/"

# Option B: Explicit input/output
python3 ~/mineru_scripts/postprocess_mineru.py \
  "<TODO: modify to your path>/md_output/DaVinci AIC V510 ISA User Guide for Guangzhou AIC/auto/DaVinci AIC V510 ISA User Guide for Guangzhou AIC_content_list.json" \
  "<TODO: modify to your path>/md_output/DaVinci AIC V510 ISA User Guide for Guangzhou AIC/auto/DaVinci_AIC_V510_ISA_fixed.md"
```

输出

````log
Expected output stats (you should see similar numbers):
Done: 21736 lines, 994338 chars
  # headings:   10
  ## headings:  478
  ### headings: 1669
  #### headings: 1086
  Bit field bold labels: 707
  Code blocks (``` pairs): 116
````

### 命令介绍

可用如下命令转换单个文件

```bash
mkdir -p pdf_input md_output
# 把你的 PDF 放到 pdf_input/

# 转换（pipeline 后端，GPU 自动检测）
mineru -p pdf_input/your.pdf -o md_output/ -b pipeline
```

关键参数：

| 参数         | 含义                   | 可选值                                                           |
| ------------ | ---------------------- | ---------------------------------------------------------------- |
| -p <path>    | 输入 PDF（文件或目录） | 文件/目录                                                        |
| -o <dir>     | 输出目录               | 目录路径                                                         |
| -b <backend> | 后端                   | pipeline（推荐）/ hybrid-engine（默认，需 VLM）/ vlm-engine      |
| -m <method>  | 解析模式               | auto（默认，自动选 ocr/txt）/ ocr（强制 OCR）/ txt（纯文字 PDF） |
| --lang       | OCR 语言               | ch（中文，默认）/ en / japan / 等                                |
| --source     | 模型源                 | local / auto / huggingface / modelscope（也可用环境变量）        |
| --device     | 设备                   | cuda / cpu / mps（也可用 MINERU_DEVICE_MODE 环境变量）           |

### 常见坑

| 报错/现象                                                         | 原因                                            | 解决                                                     |
| ----------------------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------- |
| ValueError: Local path for repo_mode 'pipeline' is not configured | mineru.json 里 models-dir.pipeline 为空或路径错 | 确认指向 PDF-Extract-Kit-1.0 根目录（含 models/）        |
| 找不到 PP-DocLayoutV2 / unimernet_hf_small_2503 / paddleocr_torch | 下载的是旧版模型包                              | 跑 mineru-models-download -s modelscope -m pipeline 更新 |
| libGL.so.1: cannot open shared object file                        | 缺系统库                                        | conda install -c conda-forge libgl 或 apt install libgl1 |
| CUDA 版本不匹配                                                   | torch 编译的 CUDA 与驱动不符                    | 按 PyTorch 官网选对应 cu121/cu124 重装 torch             |
| OOM                                                               | GPU 显存不足                                    | 降 batch 或用 -d cpu 兜底                                |

走了联网下载而非本地 model-source 没设成 local export MINERU_MODEL_SOURCE=local 或 config 里设 "model-source":"local"

## P3 — 知识库 MD到RAG

3.1 方案对比（研究结论）

| 方案        | 适合场景                              | 推荐度   |
| ----------- | ------------------------------------- | -------- |
| RAGFlow 🥇  | 直接对接 MinerU，生产级 RAG，中文友好 | 最推荐   |
| FastGPT 🥈  | 中文原生最佳，可视化工作流            | 强烈推荐 |
| AnythingLLM | 🥉 10 分钟搭好，个人小量文档          | 轻量推荐 |
| Dify        | 工作流/Agent 编排为主，RAG 是其中一环 | 一般     |
| Khoj        | 个人"第二大脑"，笔记类                | 一般     |

3.2 🥇 推荐：RAGFlow（原生支持 MinerU 解析）

RAGFlow 在 2025-10 新增了对 MinerU 作为文档解析器的原生支持，与你的 pipeline 完美对接。

```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker
git checkout v0.27.0

# GPU 加速（DeepDoc OCR/版面）
sed -i '1i DEVICE=gpu' .env
docker compose -f docker-compose.yml up -d
```

前置要求：CPU≥4 核，RAM≥16GB，Disk≥50GB，Docker≥24，vm.max_map_count≥262144（sudo sysctl -w vm.max_map_count=262144）
访问 http://100.102.192.206/（端口 80），在知识库设置里把解析器选成 MinerU，上传你 Phase 2 产出的 .md 文件即可。

3.3 🥈 备选：FastGPT（中文体验最佳）

```bash
bash <(curl -fsSL https://doc.fastgpt.io/deploy/install.sh)
docker compose up -d
# 访问 http://localhost:3000  登录 root / 1234
```

原生支持 MD/TXT/PDF/Docx 等格式，内置混合检索 + 重排，中文 UI/文档最完善。

3.4 向量库 / Embedding / Reranker 选型（研究结论）

| 组件           | 推荐选择                                | 理由                                                         |
| -------------- | --------------------------------------- | ------------------------------------------------------------ |
| Embedding 模型 | BAAI/bge-m3                             | 多语言（含中文）、8192 长上下文、dense+sparse+ColBERT 三合一 |
| （纯中文备选） | BAAI/bge-large-zh-v1.5                  | 纯中文语料 C-MTEB 最优，更小                                 |
| Reranker       | BAAI/bge-reranker-v2-m3                 | ✅ 值得加，top-k 重排可提升 nDCG@5 约 5–15%，开销很小        |
| 向量库         | Qdrant（单机服务）或 ChromaDB（嵌入式） | 单机 GPU 场景下最轻；Milvus 太重，单机不建议                 |

RAGFlow / FastGPT 都支持在知识库配置里指定 embedding 和 reranker 模型，把上面两个模型挂上去即可。

TL;DR — 最小可跑路径

```bash
# 1. 装包
conda activate mineru
pip install -U "mineru[pipeline]"

# 2. 写配置（已为你定制好路径，见 1.3）
#    并 export MINERU_TOOLS_CONFIG_JSON / MINERU_MODEL_SOURCE=local / MINERU_DEVICE_MODE=cuda

# 3. 核对模型路径（见 1.2）—— 缺失就 mineru-models-download -s modelscope -m pipeline

# 4. 转换
mineru -p pdf_input/your.pdf -o md_output/ -b pipeline -m auto --lang ch

# 5. 建知识库
cd <TODO: modify to your path>
git clone https://github.com/infiniflow/ragflow.git && cd ragflow/docker
sed -i '1i DEVICE=gpu' .env && docker compose up -d
# 浏览器开 http://100.102.192.206/ ，新建知识库 → 解析器选 MinerU → 上传 md_output 里的 .md
```
