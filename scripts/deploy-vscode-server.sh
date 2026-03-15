#!/bin/bash

# VS Code Server 自动部署脚本 v2.1
# 适配新版 VSCode 1.86+ (使用 cli/servers/Stable-xxx/server/ 结构)
# 用法: ./deploy-vscode-server.sh <目标服务器> [commit-id] [-p <port>]

set -e # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ===== 配置区域 =====
# 在这里设置你的代理（如果不需要可以留空）
HTTP_PROXY=""
HTTPS_PROXY=""
# 是否忽略证书验证 (true/false)
IGNORE_SSL="true"
# 默认 SSH 端口
DEFAULT_SSH_PORT=22
# ===================

# 打印带颜色的信息
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助
show_help() {
    echo "用法: $0 <目标服务器> [commit-id] [-p <port>]"
    echo ""
    echo "参数:"
    echo "  <目标服务器>    目标服务器地址 (格式: user@hostname)"
    echo "  [commit-id]     VS Code Server 的 Commit ID (可选，默认自动获取)"
    echo "  -p <port>       SSH 端口号 (可选，默认 22)"
    echo ""
    echo "配置:"
    echo "  请在脚本开头的配置区域设置:"
    echo "  - HTTP_PROXY: HTTP 代理地址 (使用原始密码，不要URL编码)"
    echo "  - HTTPS_PROXY: HTTPS 代理地址"
    echo "  - IGNORE_SSL: 是否忽略证书验证 (true/false)"
    echo ""
    echo "示例:"
    echo "  $0 aicix@100.105.27.28                          # 默认端口22"
    echo "  $0 aicix@100.105.27.28 -p 2222                  # 指定端口2222"
    echo "  $0 aicix@100.105.27.28 ce099c1ed25d... -p 2222  # 指定Commit ID和端口"
    echo ""
    exit 1
}

# 解析命令行参数
parse_args() {
    # 重置参数
    TARGET_SERVER=""
    COMMIT_ID=""
    SSH_PORT=$DEFAULT_SSH_PORT

    # 第一个参数必须是目标服务器
    if [ $# -lt 1 ]; then
        show_help
    fi

    TARGET_SERVER="$1"
    shift

    # 解析剩余参数
    while [ $# -gt 0 ]; do
        case "$1" in
        -p | --port)
            if [ -z "$2" ] || [ "${2:0:1}" = "-" ]; then
                error "端口号不能为空"
                exit 1
            fi
            SSH_PORT="$2"
            shift 2
            ;;
        -h | --help)
            show_help
            ;;
        *)
            # 如果还没有设置 COMMIT_ID，且参数不是以 - 开头，则认为是 COMMIT_ID
            if [ -z "$COMMIT_ID" ] && [ "${1:0:1}" != "-" ]; then
                COMMIT_ID="$1"
                shift
            else
                error "未知参数: $1"
                show_help
            fi
            ;;
        esac
    done

    info "目标服务器: $TARGET_SERVER"
    info "SSH 端口: $SSH_PORT"
    if [ -n "$COMMIT_ID" ]; then
        info "Commit ID: $COMMIT_ID"
    fi
}

# 设置临时目录（在脚本同目录下）
setup_temp_dir() {
    local script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
    TEMP_DIR="${script_dir}/vscode-server-temp-$$"
    mkdir -p "$TEMP_DIR"
    info "使用临时目录: $TEMP_DIR"
}

# URL 编码函数（用于处理密码中的特殊字符）
url_encode() {
    local string="$1"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for ((pos = 0; pos < strlen; pos++)); do
        c=${string:$pos:1}
        case "$c" in
        [-_.~a-zA-Z0-9]) o="${c}" ;;
        *) printf -v o '%%%02x' "'$c" ;;
        esac
        encoded+="${o}"
    done
    echo "${encoded}"
}

# 解析代理并重新构建（处理特殊字符）
parse_proxy() {
    local proxy="$1"

    # 如果代理为空或格式不对，直接返回
    if [ -z "$proxy" ] || [ "$proxy" = "http://your-proxy:port" ]; then
        echo ""
        return
    fi

    # 提取协议部分
    if [[ "$proxy" =~ ^(https?://)(.+) ]]; then
        local protocol="${BASH_REMATCH[1]}"
        local rest="${BASH_REMATCH[2]}"

        # 检查是否包含用户名密码
        if [[ "$rest" =~ ^([^:]+):([^@]+)@(.+) ]]; then
            local username="${BASH_REMATCH[1]}"
            local password="${BASH_REMATCH[2]}"
            local server="${BASH_REMATCH[3]}"

            # 对密码进行URL编码
            local encoded_password=$(url_encode "$password")

            # 重新构建代理URL
            echo "${protocol}${username}:${encoded_password}@${server}"
        else
            echo "$proxy"
        fi
    else
        echo "$proxy"
    fi
}

# 设置代理环境变量
setup_proxy() {
    if [ -n "$HTTP_PROXY" ] && [ "$HTTP_PROXY" != "http://your-proxy:port" ]; then
        PARSED_HTTP_PROXY=$(parse_proxy "$HTTP_PROXY")
        export http_proxy="$PARSED_HTTP_PROXY"
        export HTTP_PROXY="$PARSED_HTTP_PROXY"
        info "设置 HTTP 代理: $HTTP_PROXY"
        info "解析后代理: $PARSED_HTTP_PROXY"
    fi

    if [ -n "$HTTPS_PROXY" ] && [ "$HTTPS_PROXY" != "http://your-proxy:port" ]; then
        PARSED_HTTPS_PROXY=$(parse_proxy "$HTTPS_PROXY")
        export https_proxy="$PARSED_HTTPS_PROXY"
        export HTTPS_PROXY="$PARSED_HTTPS_PROXY"
        info "设置 HTTPS 代理: $HTTPS_PROXY"
        info "解析后代理: $PARSED_HTTPS_PROXY"
    fi
}

# 获取 curl 的额外参数
get_curl_args() {
    local args=""

    if [ -n "$PARSED_HTTP_PROXY" ]; then
        args="$args --proxy $PARSED_HTTP_PROXY"
    fi

    if [ "$IGNORE_SSL" = "true" ]; then
        args="$args -k"
    fi

    echo "$args"
}

# 构建 SSH 连接字符串
get_ssh_cmd() {
    echo "ssh -p $SSH_PORT"
}

get_scp_cmd() {
    echo "scp -P $SSH_PORT"
}

# 检查必要的命令
check_requirements() {
    info "检查必要工具..."

    for cmd in ssh scp tar curl; do
        if ! command -v $cmd &>/dev/null; then
            error "未找到命令: $cmd"
            exit 1
        fi
    done

    info "使用 curl 进行下载"
    CURL_ARGS=$(get_curl_args)
    if [ -n "$CURL_ARGS" ]; then
        info "curl 参数: $CURL_ARGS"
    fi

    # 测试 SSH 连接
    SSH_CMD=$(get_ssh_cmd)
    info "测试连接到目标服务器: $TARGET_SERVER (端口: $SSH_PORT)"
    if ! $SSH_CMD -o ConnectTimeout=5 -o BatchMode=yes "$TARGET_SERVER" "echo '连接成功'" &>/dev/null; then
        warn "需要手动输入密码"
    fi

    success "环境检查通过"
}

# 获取 VS Code 的 Commit ID
get_commit_id() {
    if [ -n "$COMMIT_ID" ]; then
        info "使用指定的 Commit ID: $COMMIT_ID"
        return
    fi

    info "正在获取最新的 VS Code Server Commit ID..."
    local api_url="https://update.code.visualstudio.com/api/commits/stable/linux-x64"

    # 构建 curl 命令
    curl_cmd=(curl -s)
    if [ -n "$CURL_ARGS" ]; then
        read -ra curl_args <<<"$CURL_ARGS"
        curl_cmd+=("${curl_args[@]}")
    fi
    curl_cmd+=("$api_url")

    COMMIT_ID=$("${curl_cmd[@]}" | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4 || echo "")

    if [ -z "$COMMIT_ID" ]; then
        warn "无法自动获取 Commit ID，使用默认版本"
        COMMIT_ID="ce099c1ed25d9eb3076c11e4a280f3eb52b4fbeb"
        info "使用默认 Commit ID: $COMMIT_ID"
    else
        info "获取到最新 Commit ID: $COMMIT_ID"
    fi
}

# 下载 VS Code Server
download_server() {
    local download_url="https://update.code.visualstudio.com/commit:${COMMIT_ID}/server-linux-x64/stable"
    local output_file="${TEMP_DIR}/vscode-server-linux-x64.tar.gz"

    info "下载 VS Code Server..."
    info "URL: $download_url"

    # 构建下载命令
    curl_cmd=(curl)
    if [ -n "$CURL_ARGS" ]; then
        read -ra curl_args <<<"$CURL_ARGS"
        curl_cmd+=("${curl_args[@]}")
    fi
    curl_cmd+=(-L -o "$output_file" "$download_url" --progress-bar)

    info "执行: ${curl_cmd[*]}"
    "${curl_cmd[@]}"

    if [ ! -f "$output_file" ] || [ ! -s "$output_file" ]; then
        error "下载失败"
        exit 1
    fi

    local file_size=$(du -h "$output_file" | cut -f1)
    success "下载完成: $output_file ($file_size)"
}

# 清理服务器上的旧部署
clean_remote_server() {
    info "清理服务器上的旧部署..."

    SSH_CMD=$(get_ssh_cmd)
    $SSH_CMD "$TARGET_SERVER" <<EOF
        echo "清理旧的 VSCode Server 目录..."
        
        # 删除旧版本的部署（包括 bin 目录和 cli 下的旧版本）
        rm -rf ~/.vscode-server/cli/servers/Stable-${COMMIT_ID}*
        rm -rf ~/.vscode-server/bin/${COMMIT_ID}
        
        # 创建新的目录结构（新版 VSCode 使用的位置）
        mkdir -p ~/.vscode-server/cli/servers/Stable-${COMMIT_ID}/server
        
        echo "清理完成"
EOF

    success "服务器清理完成"
}

# 部署到目标服务器（新版结构）
deploy_to_server() {
    local remote_tmp="/tmp/vscode-server-${COMMIT_ID}.tar.gz"
    local remote_server_base="~/.vscode-server/cli/servers/Stable-${COMMIT_ID}"
    local remote_server_dir="${remote_server_base}/server"

    SCP_CMD=$(get_scp_cmd)
    SSH_CMD=$(get_ssh_cmd)

    info "上传到目标服务器: $TARGET_SERVER (端口: $SSH_PORT)"
    $SCP_CMD "${TEMP_DIR}/vscode-server-linux-x64.tar.gz" "${TARGET_SERVER}:${remote_tmp}"

    if [ $? -ne 0 ]; then
        error "上传失败"
        exit 1
    fi
    success "上传完成"

    info "在目标服务器上部署（新版结构）..."

    # 创建远程部署脚本
    $SSH_CMD "$TARGET_SERVER" "bash -s" <<EOF
        set -e
        
        echo "📦 开始部署 VS Code Server (新版结构)..."
        
        # 确保目录存在
        mkdir -p ${remote_server_dir}
        
        # 解压文件到正确位置
        echo "解压 VS Code Server 到: ${remote_server_dir}"
        tar -xzf ${remote_tmp} -C ${remote_server_dir} --strip-components=1
        
        # 创建激活标记文件（新版可能需要）
        echo "创建激活标记..."
        touch ${remote_server_dir}/0
        
        # 创建兼容性软链接（为了兼容旧版本客户端）
        echo "创建兼容性链接..."
        mkdir -p ~/.vscode-server/bin
        ln -sf ${remote_server_dir} ~/.vscode-server/bin/${COMMIT_ID} 2>/dev/null || true
        
        # 设置正确的权限
        echo "设置权限..."
        chmod -R 755 ~/.vscode-server/
        chmod +x ${remote_server_dir}/bin/remote-cli/code 2>/dev/null || true
        
        # 清理临时文件
        rm -f ${remote_tmp}
        
        # 验证部署
        echo "验证部署..."
        if [ -f "${remote_server_dir}/0" ] && [ -d "${remote_server_dir}/out" ]; then
            echo "✅ 部署成功！"
            echo "   位置: ${remote_server_dir}"
            echo "   目录结构:"
            ls -la ${remote_server_dir} | head -10
        else
            echo "❌ 部署可能不完整，请手动检查"
            ls -la ${remote_server_dir}
            exit 1
        fi
EOF

    if [ $? -eq 0 ]; then
        success "部署完成！"
    else
        error "部署过程中出现错误"
        exit 1
    fi
}

# 清理本地临时文件
cleanup() {
    info "清理本地临时文件..."
    rm -rf "$TEMP_DIR"
    success "清理完成"
}

# 主函数
main() {
    echo "==============================================="
    echo "   VS Code Server 自动部署脚本 v2.1"
    echo "   (适配新版 VSCode 1.86+ 结构 + 支持自定义端口)"
    echo "==============================================="
    echo ""

    # 解析命令行参数
    parse_args "$@"

    # 设置临时目录（在脚本同目录下）
    setup_temp_dir

    # 设置代理
    setup_proxy

    # 检查环境
    check_requirements

    # 获取 Commit ID
    get_commit_id

    # 下载 Server
    download_server

    # 清理远程旧部署
    clean_remote_server

    # 部署到远程服务器
    deploy_to_server

    # 清理本地临时文件
    cleanup

    echo ""
    success "🎉 所有操作完成！"
    echo ""
    echo "📌 部署信息:"
    echo "   - 目标服务器: $TARGET_SERVER"
    echo "   - SSH 端口: $SSH_PORT"
    echo "   - Commit ID: $COMMIT_ID"
    echo "   - 远程位置: ~/.vscode-server/cli/servers/Stable-${COMMIT_ID}/server/"
    echo ""
    echo "现在可以尝试连接 VS Code:"
    echo "1. 在本地 VS Code 中执行: Ctrl+Shift+P"
    echo "2. 输入: Remote-SSH: Kill VS Code Server on Host..."
    echo "3. 选择: $TARGET_SERVER"
    echo "4. 重新连接"
    echo ""
    echo "如果仍有问题，请查看 Remote-SSH 日志:"
    echo "Ctrl+Shift+P -> Remote-SSH: Show Log"
}

# 捕获中断信号
trap cleanup EXIT INT TERM

# 运行主函数
main "$@"
