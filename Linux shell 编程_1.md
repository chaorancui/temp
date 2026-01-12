[toc]

# shell 编程

## 安全选项及调试

```bash
#!/bin/bash
set -euo pipefail
export PS4='+ ${BASH_SOURCE}:${LINENO}: ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
[ "${DEBUG:-false}" = true ] && set -x
```

## `set` 命令

在 shell 脚本中，`set` 命令用于更改脚本的执行选项，以控制脚本的行为。`set -参数` 表示**启用**某选项，`set +参数` 表示**关闭**某选项。
以下是一些常见选项及其作用：

1. `set -e` 与 `set +e`

   - **`set -e`**:
     当设置此选项时，脚本会在遇到非零退出状态的命令时立即退出（除非该命令已被 `if`、`while` 或 `||` 等控制结构捕获）。
     适用于希望脚本严格执行并在错误时立即停止的场景。

     示例：

     ```bash
     set -e
     echo "开始"
     ls /不存在的路径  # 这里会导致脚本退出
     echo "不会执行到这里"
     ```

   - **`set +e`**:
     关闭 `-e` 模式（即默认模式）。脚本即使遇到非零退出状态的命令，也会继续执行。可以自己添加异常处理逻辑。

2. `set -x` 与 `set +x`

   - **`set -x`**:
     开启调试模式，会在执行每一行命令前将其打印到标准错误输出。这对于调试脚本非常有用。

     示例：

     ```bash
     set -x
     echo "Hello"
     ls
     set +x
     ```

     输出示例：

     ```bash
     + echo "Hello"
     Hello
     + ls
     ```

   - **`set +x`**:
     关闭调试模式（即默认模式），不再打印命令。

3. 其他常用选项

   - **`set -u`**
     在脚本中引用未定义的变量时，立即退出并报错（默认情况下引用未定义变量会返回空值）。

     示例：

     ```bash
     set -u
     echo $未定义变量  # 会导致脚本退出
     ```

   - **`set +u`**
     关闭 `-u` 模式，允许使用未定义的变量。

   - **`set -o pipefail`**
     当命令管道中的任何一个命令失败时，返回非零状态。默认情况下，管道返回最后一个命令的退出状态。

     示例：

     ```bash
     set -o pipefail
     ls /不存在的路径 | grep "something"  # 返回非零状态
     ```

   - **`set +o pipefail`**
     关闭 `pipefail` 模式，恢复默认行为。

**总结**：

通过 `set`，可以细粒度控制脚本的行为。常见的组合：

- **调试脚本**: `set -x`
- **严格执行**: `set -euo pipefail`
- **临时关闭选项**: 用 `set +<option>` 在局部关闭某些特性。

## `set -euo pipefail`

**建议使用 `set -euo pipefail` 作为默认安全选项**。

**常见报错修复**：

1. 环境变量报错
   当使用 `set -euo pipefail` 当做默认安全选项后，如下写法会报错：

   ```bash
   # 写法1
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/lib
   # 写法2
   echo "$LD_LIBRARY_PATH"
   # 写法3
   if [ -n "$LD_LIBRARY_PATH" ]; then
      ...
   fi
   # 都会报错：
   xxx.sh: line 59: LD_LIBRARY_PATH: unbound variable
   ```

   报错原因：

   LD_LIBRARY_PATH 不是强制存在的环境变量，很多系统、容器、最小环境中 根本不会定义它。启用了 `set -u` 后，任何**未定义变量的读取都会直接报错**。

   修复：
   `set -u` 下处理**可选环境变量**的通用模板

   ```bash
   VAR="${VAR:-}"

   # 如：
   export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:-}:/opt/lib"
   ```

## `set -x`

`-x`选项可用来跟踪脚本的执行，是**调试 shell 脚本**的强有力工具。

**一、set -x 的基本使用：**
shell 的执行选项除了可以在**启动 shell 时指定外，亦可在脚本中用 set 命令来指定**。

1. 启动 shell 指定

   ```shell
   # 方法1: 在命令行设置
   bash -x script.sh
   bash -x script.sh arg1 arg2

   # 方法2: 更详细的调试
   bash -vx script.sh  # -v: 显示原始代码，-x: 显示执行过程
   ```

2. 脚本中指定

   ```shell
   set -x  #启动"-x"选项 要跟踪的程序段
   set +x  #关闭"-x"选项

   # 调试输出会显示文件名、行号
   export PS4='+ [${BASH_SOURCE[0]##*/}:${LINENO}]: '
   set -x

   # 调试输出会显示文件名、行号和函数名
   export PS4='+ ${BASH_SOURCE}:${LINENO}: ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
   set -x

   # 条件调试
   export PS4='+ ${BASH_SOURCE}:${LINENO}: ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
   DEBUG=${DEBUG:-false}
   if [ "$DEBUG" = true ]; then
       set -x
   fi

   # 条件调试简写
   export PS4='+ ${BASH_SOURCE}:${LINENO}: ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
   [ "${DEBUG:-false}" = true ] && set -x
   ```

**二、对"-x"选项的增强**：

- `$LINENO`：代表 shell 脚本的当前行号，类似于 C 语言中的内置宏`__LINE__`

- `$FUNCNAME`： 函数的名字，类似于 C 语言中的内置宏 `__func__`，但宏 `__func__` 只能代表当前所在的函数名，而 `$FUNCNAME` 的功能更强大，它是一个数组变量，其中包含了整个调用链上所有的函数的名字，故变量 `${FUNCNAME[0]}` 代表 shell 脚本当前正在执行的函数的名字，而变量 `${FUNCNAME[1]}` 则代表调用函数 `${FUNCNAME[0]}` 的函数的名字，余者可以依此类推。

- `$PS4`：主提示符变量 `$PS1` 和第二级提示符变量 `$PS2` 比较常见，但很少有人注意到第四级提示符变量 `$PS4` 的作用。`$PS4` 的值将被显示在 `-x` 选项输出的每一条命令的前面。在 Bash Shell 中，缺省的$PS4 的值是"+"号。现在知道为什么使用"-x"选项时，输出的命令前面有一个"+"号了吧。

**三、调试输出解释：**
`+`号的数量表示**命令的嵌套深度**或**执行环境的层级**。

1. **单个加号 `+`**

   表示**主脚本层级**的命令

   ```bash
   #!/bin/bash
   set -x

   echo "Level 1"
   # 输出: + echo 'Level 1'
   ```

2. **两个加号 `++`**

   表示**子 shell 层级**或**命令替换**中的命令

   ```bash
   #!/bin/bash
   set -x

   # 命令替换产生子shell
   date_output=$(date)
   # 输出: ++ date
   # 输出: + date_output='Tue Jan 7 10:30:00 UTC 2025'

   # 管道也会创建子shell
   ls | wc -l
   # 输出: ++ ls
   # 输出: ++ wc -l
   ```

3. **更多加号的情况**

   随着嵌套深度增加，加号会越来越多：

   bash

   ```bash
   #!/bin/bash
   set -x

   # 三级嵌套示例
   result=$(echo $(date))
   # 输出: +++ date      (最内层)
   # 输出: ++ echo 'Tue Jan 7 10:30:00 UTC 2025' (中间层)
   # 输出: + result='Tue Jan 7 10:30:00 UTC 2025' (最外层)
   ```

## trap 调试

`trap`命令用于捕获 shell 接收到的信号(signal)或其他特定事件,并在这些事件发生时执行指定的命令。这是 shell 脚本中实现优雅退出、资源清理和错误处理的重要机制。

**一、trap 调试详解**

1. **基本语法**

   ```bash
   trap '命令' 信号列表
   trap - 信号列表  # 恢复信号的默认处理
   trap  # 列出当前设置的trap
   ```

   常用信号：

   - **EXIT**: 脚本退出时触发(无论正常还是异常)。用途：清理资源
   - **ERR**: 命令返回非零状态时触发。用途：错误处理
   - **DEBUG**: 每个命令执行前触发。用途：追踪执行流程
   - **RETURN**: 函数或 source 的脚本返回时触发。用途：函数追踪
   - **INT**: 接收到中断信号时触发(Ctrl+C)
   - **TERM**: 接收到终止信号时触发
   - **HUP**: 终端断开时触发
   - **SIGINT, SIGTERM, SIGHUP**: 数字形式的信号

   > 注：
   >
   > 1. DEBUG trap 问题：在函数内部不可靠
   > 2. RETURN trap 问题：
   >    - 在脚本直接执行（./test.sh）时，可能因为 bash 版本或配置不同而不触发
   >    - 某些 bash 版本的 RETURN trap 行为不一致

2. **基本使用示例**

   ```bash
   #!/bin/bash
   # trap_debug.sh

   # 1. DEBUG 信号 - 每个命令执行前触发
   trap 'echo "DEBUG: Line $LINENO, Command: $BASH_COMMAND"' DEBUG

   echo "Start script"
   name="Alice"
   echo "Hello $name"

   # 禁用DEBUG trap
   trap - DEBUG
   echo "Debug disabled"

   # 2. ERR 信号 - 错误时触发
   trap 'echo "ERROR at line $LINENO: Command failed with exit code $?"' ERR

   ls /nonexistent  # 这个命令会失败
   echo "继续执行"

   # 3. EXIT 信号 - 脚本退出时
   trap 'echo "脚本结束，退出码: $?"' EXIT
   ```

3. **更高级的 trap 调试**

   ```bash
   #!/bin/bash
   # advanced_trap.sh

   # 自定义调试函数
   debug_info() {
       echo "=== DEBUG INFO ==="
       echo "时间: $(date +%T.%3N)"
       echo "行号: $LINENO"
       echo "命令: $BASH_COMMAND"
       echo "函数: ${FUNCNAME[1]:-main}"
       echo "脚本: ${BASH_SOURCE[0]}"
       echo "=================="
   }

   # 设置DEBUG trap
   trap debug_info DEBUG

   # 测试代码
   function process_data() {
       local data=$1
       echo "Processing: $data"
       echo "Result: $(echo "$data" | tr 'a-z' 'A-Z')"
   }

   echo "开始执行"
   process_data "hello world"
   echo "结束"
   ```

**二、trap 与 set -x 的区别对比**

| 特性           | `trap DEBUG`           | `set -x`                     |
| :------------- | :--------------------- | :--------------------------- |
| **触发时机**   | 每个命令**执行前**     | 命令**执行后**显示执行的内容 |
| **控制粒度**   | 更细，可以条件触发     | 整个代码段或脚本             |
| **自定义输出** | 完全可自定义格式       | 固定格式（可通过 PS4 微调）  |
| **性能影响**   | 更大（每个命令都触发） | 较小                         |
| **信息获取**   | 可以获取更多上下文     | 主要显示命令本身             |
| **嵌套处理**   | 可以区分不同层级       | 自动显示`+`层级              |

对比示例：

```bash
#!/bin/bash
# compare.sh

echo "=== 使用 set -x ==="
set -x
result=$(echo "test" | wc -c)
echo "Result: $result"
set +x

echo -e "\n=== 使用 trap DEBUG ==="
trap 'echo "[DEBUG] 即将执行: $BASH_COMMAND"' DEBUG
result=$(echo "test" | wc -c)
echo "Result: $result"
trap - DEBUG

# 输出对比：
# set -x 输出：
# + echo test
# + wc -c
# + result=5
# + echo 'Result: 5'
#
# trap DEBUG 输出：
# [DEBUG] 即将执行: result=$(echo "test" | wc -c)
# [DEBUG] 即将执行: echo "Result: $result"
```

**三、应用场景示例**

```bash
#!/bin/bash

# ============================================================================
# Shell Trap Command Demo Collection
# ============================================================================
# 包含5个实用场景：
# 1. 条件调试 (Conditional Debugging)
# 2. 性能分析 (Performance Profiling)
# 3. 函数调用追踪 (Function Call Tracing)
# 4. 错误追踪和恢复 (Error Tracking & Recovery)
# 5. 资源监控 (Resource Monitoring)
# ============================================================================

# ============================================================================
# 场景1: 条件调试 (Conditional Debugging)
# ============================================================================

demo_conditional_debug() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║           Demo 1: Conditional Debugging                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # 调试配置
    DEBUG_MODE=true
    DEBUG_LEVEL=2  # 1=basic, 2=detailed, 3=verbose

    # 调试函数
    debug() {
        local level=$1
        shift
        if $DEBUG_MODE && [ "$level" -le "$DEBUG_LEVEL" ]; then
            echo "[DEBUG-L$level] $(date '+%H:%M:%S') - $*" >&2
        fi
    }

    # 条件断点
    breakpoint() {
        local condition=$1
        local message=$2
        if eval "$condition"; then
            echo ">>> Breakpoint: $message"
            echo ">>> Line: $LINENO"
            read -p ">>> Press Enter to continue..."
        fi
    }

    # 示例逻辑
    local counter=0
    debug 1 "Starting process"

    for i in {1..5}; do
        counter=$((counter + i))
        debug 2 "Loop iteration $i, counter=$counter"

        # 条件断点示例
        if [ "$DEBUG_MODE" = true ] && [ $i -eq 3 ]; then
            breakpoint "[ $counter -gt 5 ]" "Counter exceeded threshold"
        fi
    done

    debug 1 "Process completed, final counter=$counter"
    echo ""
}

# ============================================================================
# 场景2: 性能分析 (Performance Profiling)
# ============================================================================

demo_performance_profiling() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║           Demo 2: Performance Profiling                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # 性能数据存储
    declare -A FUNC_TIMES
    declare -A FUNC_COUNTS

    # 性能分析包装器
    profile() {
        local func_name="$1"
        shift

        local start_time=$(date +%s%N)
        "$func_name" "$@"
        local exit_code=$?
        local end_time=$(date +%s%N)

        local duration=$((end_time - start_time))
        if [ $duration -ge 0 ] && [ $duration -lt 60000000000 ]; then
            FUNC_TIMES["$func_name"]=$((${FUNC_TIMES["$func_name"]:-0} + duration))
            FUNC_COUNTS["$func_name"]=$((${FUNC_COUNTS["$func_name"]:-0} + 1))
        fi

        return $exit_code
    }

    # 显示性能报告
    show_report() {
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║              Performance Report                            ║"
        echo "╠════════════════════════════════════════════════════════════╣"
        printf "║ %-30s %8s %12s ║\n" "Function" "Calls" "Total(ms)"
        echo "╠════════════════════════════════════════════════════════════╣"

        for func in "${!FUNC_TIMES[@]}"; do
            local total_ns=${FUNC_TIMES[$func]}
            local count=${FUNC_COUNTS[$func]}
            local total_ms=$((total_ns / 1000000))
            printf "║ %-30s %8d %12d ║\n" "$func" "$count" "$total_ms"
        done

        echo "╚════════════════════════════════════════════════════════════╝"
    }

    # 测试函数
    fast_func() { echo "Fast" > /dev/null; }
    slow_func() { sleep 0.05; }
    medium_func() { local x=$(seq 1 1000 | wc -l); }

    # 执行测试
    echo "Running performance tests..."
    for i in {1..5}; do profile fast_func; done
    for i in {1..3}; do profile slow_func; done
    for i in {1..4}; do profile medium_func; done

    show_report
    echo ""
}

# ============================================================================
# 场景3: 函数调用追踪 (Function Call Tracing)
# ============================================================================

demo_function_tracing() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║           Demo 3: Function Call Tracing                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    TRACE_ENABLED=true
    CALL_DEPTH=0

    # 进入函数追踪
    trace_enter() {
        if ! $TRACE_ENABLED; then return; fi
        local func_name="${FUNCNAME[1]}"
        if [[ "$func_name" =~ ^(trace_|show_stack) ]]; then return; fi

        local indent=$(printf '%*s' $((CALL_DEPTH * 2)) '')
        echo "${indent}→ Enter $func_name() [depth:$CALL_DEPTH]" >&2
        CALL_DEPTH=$((CALL_DEPTH + 1))
    }

    # 退出函数追踪
    trace_exit() {
        if ! $TRACE_ENABLED; then return; fi
        local func_name="${FUNCNAME[1]}"
        if [[ "$func_name" =~ ^(trace_|show_stack) ]]; then return; fi

        CALL_DEPTH=$((CALL_DEPTH - 1))
        local indent=$(printf '%*s' $((CALL_DEPTH * 2)) '')
        echo "${indent}← Exit $func_name()" >&2
    }

    # 设置追踪
    trap 'trace_exit' RETURN

    # 测试函数
    func_a() {
        trace_enter
        echo "Executing func_a"
        func_b
    }

    func_b() {
        trace_enter
        echo "Executing func_b"
        func_c
    }

    func_c() {
        trace_enter
        echo "Executing func_c"
    }

    # 执行测试
    func_a

    # 清理trap
    trap - RETURN
    echo ""
}

# ============================================================================
# 场景4: 错误追踪和恢复 (Error Tracking & Recovery)
# ============================================================================

demo_error_tracking() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║           Demo 4: Error Tracking & Recovery                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    ERROR_LOG="/tmp/demo_errors_$$.log"
    ERROR_COUNT=0
    MAX_ERRORS=3

    # 清理函数
    cleanup() {
        if [ $ERROR_COUNT -gt 0 ]; then
            echo ""
            echo "Total errors encountered: $ERROR_COUNT"
            echo "Error log: $ERROR_LOG"
            cat "$ERROR_LOG"
        fi
        rm -f "$ERROR_LOG" 2>/dev/null
    }

    trap 'cleanup' EXIT

    # 安全执行包装器
    safe_exec() {
        local description="$1"
        shift

        echo "Executing: $description"
        set +e
        "$@"
        local result=$?
        set -e

        if [ $result -ne 0 ]; then
            ERROR_COUNT=$((ERROR_COUNT + 1))
            {
                echo "Error #$ERROR_COUNT at $(date '+%H:%M:%S')"
                echo "Command: $*"
                echo "Exit code: $result"
                echo "---"
            } >> "$ERROR_LOG"

            if [ $ERROR_COUNT -ge $MAX_ERRORS ]; then
                echo "Error limit reached, stopping..."
                return 1
            fi
            echo "Error captured, continuing..."
        fi
        return $result
    }

    # 重试包装器
    retry() {
        local max_attempts=$1
        shift
        local attempt=1

        while [ $attempt -le $max_attempts ]; do
            echo "  Attempt $attempt/$max_attempts"
            set +e
            "$@"
            local result=$?
            set -e

            if [ $result -eq 0 ]; then
                return 0
            fi

            attempt=$((attempt + 1))
            [ $attempt -le $max_attempts ] && sleep 1
        done

        return 1
    }

    # 测试函数
    risky_op() {
        local fail_chance=$1
        [ $((RANDOM % 100)) -lt $fail_chance ] && return 1 || return 0
    }

    # 执行测试
    safe_exec "Normal operation" true
    safe_exec "Risky operation" risky_op 70 || echo "  Handled gracefully"
    safe_exec "Another risky operation" risky_op 80 || echo "  Handled gracefully"

    echo ""
    echo "Testing retry mechanism:"
    retry 3 risky_op 60 && echo "Success!" || echo "Failed after retries"

    trap - EXIT
    cleanup
    echo ""
}

# ============================================================================
# 场景5: 资源监控 (Resource Monitoring)
# ============================================================================

demo_resource_monitoring() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║           Demo 5: Resource Monitoring                          ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    MONITOR_LOG="/tmp/monitor_$$.log"
    MONITOR_PID=$$
    MONITOR_BG_PID=""

    # 启动监控
    start_monitor() {
        echo "Starting resource monitor (PID: $MONITOR_PID)"

        (
            while kill -0 $MONITOR_PID 2>/dev/null; do
                local cpu=$(ps -p $MONITOR_PID -o %cpu= 2>/dev/null | tr -d ' ')
                local mem=$(ps -p $MONITOR_PID -o rss= 2>/dev/null | tr -d ' ')
                local timestamp=$(date +%s)
                echo "$timestamp,$cpu,$mem" >> "$MONITOR_LOG"
                sleep 1
            done
        ) &

        MONITOR_BG_PID=$!
    }

    # 停止监控并显示报告
    stop_monitor() {
        if [ -n "$MONITOR_BG_PID" ]; then
            kill $MONITOR_BG_PID 2>/dev/null || true
            wait $MONITOR_BG_PID 2>/dev/null || true
        fi

        if [ ! -f "$MONITOR_LOG" ]; then
            echo "No monitoring data"
            return
        fi

        local count=0
        local total_cpu=0
        local max_cpu=0
        local total_mem=0
        local max_mem=0

        while IFS=',' read -r ts cpu mem; do
            [ -z "$cpu" ] && continue
            count=$((count + 1))

            cpu_int=${cpu%.*}
            total_cpu=$((total_cpu + ${cpu_int:-0}))
            [ "${cpu_int:-0}" -gt "$max_cpu" ] && max_cpu=${cpu_int:-0}

            total_mem=$((total_mem + mem))
            [ $mem -gt $max_mem ] && max_mem=$mem
        done < "$MONITOR_LOG"

        if [ $count -gt 0 ]; then
            echo ""
            echo "╔════════════════════════════════════════════════════╗"
            echo "║           Resource Usage Report                    ║"
            echo "╠════════════════════════════════════════════════════╣"
            printf "║ Duration: %-7d seconds                         ║\n" "$count"
            printf "║ CPU  - Avg: %-3d%%   Peak: %-3d%%                ║\n" \
                $((total_cpu / count)) "$max_cpu"
            printf "║ MEM  - Avg: %-5d MB  Peak: %-5d MB            ║\n" \
                $((total_mem / count / 1024)) $((max_mem / 1024))
            echo "╚════════════════════════════════════════════════════╝"
        fi

        rm -f "$MONITOR_LOG"
    }

    trap 'stop_monitor' EXIT

    # 启动监控
    start_monitor
    sleep 1

    # CPU密集型任务
    echo "Running CPU-intensive task..."
    local sum=0
    for i in {1..500000}; do
        sum=$((sum + i % 100))
    done

    sleep 1

    # 内存密集型任务
    echo "Running memory-intensive task..."
    local big_array=()
    for i in {1..5000}; do
        big_array+=("data_$i")
    done

    sleep 2

    echo "Tasks completed"

    trap - EXIT
    stop_monitor
    echo ""
}

# ============================================================================
# 主菜单
# ============================================================================

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║         Shell Trap Command - Usage Demonstrations              ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Available demos:"
    echo "  1. Conditional Debugging"
    echo "  2. Performance Profiling"
    echo "  3. Function Call Tracing"
    echo "  4. Error Tracking & Recovery"
    echo "  5. Resource Monitoring"
    echo "  a. Run all demos"
    echo "  q. Quit"
    echo ""

    read -p "Select demo (1-5, a, q): " choice

    case $choice in
        1) demo_conditional_debug ;;
        2) demo_performance_profiling ;;
        3) demo_function_tracing ;;
        4) demo_error_tracking ;;
        5) demo_resource_monitoring ;;
        a|A)
            demo_conditional_debug
            demo_performance_profiling
            demo_function_tracing
            demo_error_tracking
            demo_resource_monitoring
            ;;
        q|Q) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac

    echo ""
    read -p "Press Enter to continue..."
    main
}

# 如果直接运行脚本，显示菜单
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main
fi
```

五、**使用建议**

使用 `trap` 的场景：

1. **需要自定义调试信息格式**
2. **只想追踪特定类型的命令**
3. **需要记录命令执行时间**
4. **实现复杂的错误处理和恢复**
5. **资源监控和性能分析**

使用 `set -x` 的场景：

1. **快速查看脚本执行流程**
2. **简单的调试需求**
3. **查看变量展开后的实际命令**
4. **需要较少性能开销的调试**

`trap`命令的这些高级用法可以大大增强 shell 脚本的调试能力、稳定性和可维护性。在实际使用中,你可以根据需求组合使用这些技术,构建更加健壮和专业的 shell 脚本。需要注意的是,过度使用 trap 可能会影响脚本性能,建议在开发调试阶段启用详细追踪,在生产环境中使用更轻量级的监控。

## shell 中转义字符$

在 linux shell 脚本中经常用到字符`$`，下面是`$`的一些常见用法

| 名称 | 含义                                                                    |
| ---- | ----------------------------------------------------------------------- |
| $#   | 传给脚本的参数个数                                                      |
| $0   | 脚本本身的名字                                                          |
| $1   | 传递给该 shell 脚本的第一个参数                                         |
| $2   | 传递给该 shell 脚本的第二个参数                                         |
| $@   | 传给脚本的所有参数的列表                                                |
| $\*  | 以一个单字符串显示所有向脚本传递的参数，与位置变量不同，参数可超过 9 个 |
| $$   | 脚本运行的当前进程 ID 号                                                |
| $?   | 显示最后命令的退出状态，0 表示没有错误，其他表示有错误                  |

- 文件名`test`

```shell
#!/bin/sh
echo "number:$#"
echo "scname:$0"
echo "first :$1"
echo "second:$2"
echo "argume:$@"
```

- 运行结果

```shell
number:2   //$# 是传给脚本的参数个数
scname:./test //$0 是脚本本身的名字
first: aa  //$1是传递给该shell脚本的第一个参数
second:bb  //$2是传递给该shell脚本的第二个参数
argume:aa bb //$@ 是传给脚本的所有参数的列表
```

## IFS 环境变量

Shell 中的 **IFS (Internal Field Separator)** 是一个特殊的环境变量，它定义了 Shell 在**分割字符串为多个字段时使用的分隔符**，默认值通常是**空格、制表符 (Tab) 和换行符**。当 Shell 处理变量替换、命令替换或`read`命令时，会根据 IFS 中的字符来拆分文本。用户可以修改 IFS 的值来定制分隔符，以处理特定格式的文本，比如用逗号、冒号等作为分隔符。

**IFS 的主要作用**

- **单词分割**：在没有引号包围的情况下，Shell 会用 IFS 中的字符将字符串拆分成单词或字段。
- **`read`命令**：用于将输入行分割成多个字段，并赋给多个变量。
- **列表展开**：控制`$*`和`$@`（当`$@`未用引号时）展开时的分隔符。

**默认值**

- `IFS` 默认包含空格、制表符和换行符 ( ``、`\t`、`\n` )。

**自定义示例**

- **忽略换行符，只用空格/制表符**：`IFS=$' \t'`。
- **使用逗号作为分隔符**：`IFS=','`。
- **使用冒号**：`IFS=':'`。
- **自定义 IP 地址分割**：`IFS='.'` 来反转 IP 地址。

## 重定向

在 Shell 中，输出重定向是一种将命令的标准输出（stdout）或标准错误（stderr）保存到文件或传递给另一个命令的技术。输出重定向使你能够灵活地管理和处理命令的输出。

1. 基本输出重定向
   将标准输出重定向到文件

   - `>`：将命令的标准输出重定向到一个文件。如果文件已经存在，会覆盖文件的内容。

     ```shell
     command > filename

     echo "Hello, World!" > output.txt
     # 这会将 "Hello, World!" 保存到 output.txt 文件中。如果 output.txt 已存在，其内容会被覆盖。
     ```

   - `>>`：将命令的标准输出追加到文件的末尾。如果文件不存在，会创建文件；如果文件已经存在，新的输出内容会追加到文件末尾。

     ```shell
     command >> filename

     echo "Hello again!" >> output.txt
     # 这会将 "Hello again!" 追加到 output.txt 的末尾，而不会覆盖之前的内容。
     ```

2. 重定向标准错误
   标准错误输出（stderr）通常用于输出错误信息，可以将其重定向到文件。

   - `2>`：将标准错误输出重定向到文件。

     ```shell
     command 2> errorfile.txt

     ls non_existent_file 2> error.txt
     # 这会将 ls 命令的错误信息保存到 error.txt 文件中。
     ```

3. 同时重定向标准输出和标准错误

   - `&>` 或 `2>&1`：将标准输出和标准错误一起重定向到同一个文件。

     ```shell
     command &> outputfile.txt
     # 等价于
     command > outputfile.txt 2>&1

     ls /nonexistent_directory &> all_output.txt
     # 这会将 ls 命令的标准输出和错误输出都保存到 all_output.txt 文件中。

     # 重定向 + 管道组合
     command 2>&1 | tee output.log
     ```

     注意：

     - `&>` 是 Bash 的语法糖（语法简写），只能用于 Bash（不是 POSIX 标准，因此在 sh 或某些老版本 shell 中不支持）。
     - `command 2>&1 | tee output.log` <font color=red>重定向 + 管道组合</font>：
       - `2>&1`：先把标准错误（fd 2）重定向到标准输出（fd 1）
       - 整个 stdout + stderr 一起通过 `|` 管道交给 tee
       - `tee`：一边将输入写入 output.log，一边输出到终端（屏幕）
     - `command > file 2>&1` <font color=red>顺序非常重要！</font>这表示：
       - 先把 stdout 重定向到 file
       - 再把 stderr 重定向到 stdout（此时 stdout 已经是 file）
     - `command 2>&1 > file` 是错误写法：
       - `2>&1`：把 stderr 重定向到当前的 stdout，此时 stdout 还指向终端
       - `> file`：把 stdout 重定向到 file，但是 stderr 已经绑定到了“原始的终端 stdout”，不会跟着变
       - 结果是：stdout 输出进 file，stderr 仍然输出到终端！

4. 重定向到 `/dev/null`
   `/dev/null` 是一个特殊的文件，任何写入它的数据都会被丢弃。可以使用它来忽略不需要的输出。

   - 忽略标准输出/标准错误/标注输出和错误：

     ```shell
     # 忽略标准输出：
     command > /dev/null

     # 忽略标准错误：
     command 2> /dev/null

     # 忽略标准输出和标准错误：
     command > /dev/null 2>&1

     ls /nonexistent_directory > /dev/null 2>&1
     # 这会忽略 ls 命令的所有输出。
     ```

5. 管道（|）
   管道将一个命令的标准输出作为下一个命令的标准输入。常用于将多个命令串联起来处理数据。

   - 使用管道：

     ```shell
     command1 | command2

     ls -l | grep "^d"
     这会将 ls -l 的输出传递给 grep 命令，只显示目录条目。
     ```

6. 文件描述符的重定向
   在 Shell 中，文件描述符用于标识不同的输入和输出流：

   - 标准输入 (stdin)：文件描述符 0
   - 标准输出 (stdout)：文件描述符 1
   - 标准错误 (stderr)：文件描述符 2

   你可以使用文件描述符进行更精细的重定向控制。

   ```shell
   command 1> stdout.txt 2> stderr.txt
   # 这会将标准输出重定向到 stdout.txt，将标准错误重定向到 stderr.txt。
   ```

7. Here Document (<<)
   Here Document 用于将多行字符串作为输入传递给命令。

   ```shell
   command << EOF
   line1
   line2
   EOF
   ```

   - command：这是需要接收多行输入的命令。
   - <<：这个符号告诉 Shell 开始一个 Here Document。
   - EOF：这个是标识符（delimiter），表示 Here Document 的开始和结束。EOF 只是一个常用的标识符名称，你可以用其他任何字符串代替，只要它在开始和结束时保持一致即可。

   如下命令，在 << EOF 之后的所有内容都将作为输入传递给指定的命令，直到遇到结尾标识符（如 EOF）。

   ```shell
   cat << EOF > file.txt
   This is line 1
   This is line 2
   EOF
   # 这会将多行文本保存到 file.txt 中。
   ```

总结

- `>`：将标准输出重定向到文件（覆盖文件内容）。
- `>>`：将标准输出追加到文件末尾。
- `2>`：将标准错误输出重定向到文件。
- `&>` 或 `2>&1`：同时重定向标准输出和标准错误。
- `/dev/null`：丢弃输出。
- `|`：将一个命令的输出作为下一个命令的输入。
- `Here Document (<<)`：用于传递多行输入。

## 运算符优先级

> [Bash 脚本进阶指南：正文 > 第二部分 shell 基础 > 8. 运算符相关话题](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese/zheng-wen/part2/08_operations_and_related_topics/08_4_operator_precedence)

## 命令组合符号

在 Shell 编程中，`;`、`|`、`()`、`{}`、`&&`、`||`、`!` 等符号用于控制命令的执行顺序、条件判断和组合，以下是它们的详细介绍：

1. **`;` (命令分隔符)**

   `;` 用于在同一行中执行多个命令，命令之间没有依赖关系。无论前一个命令是否成功，后一个命令都会执行。

   示例：

   ```bash
   echo "First command" ; sleep 2; echo "Second command"
   ```

   这里，`echo "First command"` 和 `echo "Second command"` 会**依次执行**。

2. **`|` (管道操作符)**

   `|` 是管道符号，用于将前一个命令的输出作为下一个命令的输入，即将一个命令的结果“管道”给另一个命令。

   示例：

   ```bash
   ls -l | grep ^- | sort -k5 -nr
   ```

   - `ls -l`：以长格式列出文件和目录。
   - `grep ^-`：过滤出文件（忽略目录）。在 ls -l 输出中，文件以 - 开头，目录以 d 开头，符号链接以 l 开头。
   - `sort -k5 -nr`：按第 5 列（文件大小）进行数值排序（-n 表示数值排序，-r 表示从大到小排序）。

3. **`()` (子 shell)**

   `()` 用于在子 **Shell 中执行命令序列**，子 Shell 是一个独立的环境，子 Shell 中的变量或状态不会影响当前 Shell。

   示例：

   ```bash
   (cd .. && ls)
   ```

   在子 Shell 中进入父目录并列出内容，执行完毕后，当前 Shell 仍在原来的目录。

4. **`{}` (命令块)**

   `{}` 表示命令块，内部的多个命令会在**当前 Shell 中执行**。不同于 `()`，它不会创建子 Shell。
   **正确格式要求**：

   - 大括号 `{` 和 `}` 必须与内部命令之间有**空格**。
   - 多个命令之间需要用 `;` 或换行符分隔（即在 Shell 中，`{}` 内的命令必须用分号 `;` 连接，不能使用 `&&` 直接连接）。

   ```bash
   { cd ..; ls; }
   # 或
   {
     cd ..
     ls
   }
   ```

   在当前 Shell 中进入父目录并列出内容，执行完毕后，当前 Shell 会切换至父目录。

5. **`()` 和 `{}` 对比**

   如果希望把几个命令合在一起执行，shell 提供了两种方法：

   1. `()` 在子 shell 中执行一组命令
   2. `{  }` 在当前 shell 中执行一组命令

   ```shell
   # () 在子 shell 中执行
   A=1; echo $A; (A=2;); echo $A
   1
   1
   # {  } 在当前 shell 中执行
   A=1; echo $A; { A=2; }; echo $A
   1
   2
   ```

6. **`&&` (逻辑与, AND)**

   `&&` 是逻辑与操作符，

   - 表示前一个命令成功（退出状态码 $? 为 0）时才执行下一个命令。
   - 只要有一个命令失败（退出状态码 $? 为 1），后面的命令就不会被执行。

   示例：

   ```bash
   mkdir new_dir && cd new_dir
   ```

   如果 `mkdir new_dir` 成功，则 `cd new_dir` 会被执行。

   > 技巧：
   >
   > - `cp xx && rm -f xx && echo "copy and rm success!"`，拷贝后删除原文件

7. **`||` (逻辑或, OR)**

   `||` 是逻辑或操作符，

   - 表示前一个命令失败（退出状态码 $? 非 0）时才执行下一个命令。
   - 只要有一个命令成功（退出状态码 $? 为 0），后面的命令就不会被执行。

   示例 1：

   ```bash
   mkdir new_dir || echo "Failed to create directory"
   ```

   如果 `mkdir new_dir` 失败，则会执行 `echo "Failed to create directory"` 命令。

   示例 2：

   ```shell
   ls dir &> /dev/null && echo"SUCCESS" || echo "FAIL"
   # 如果 dir 目录存在，将输出 SUCCESS 提示信息；否则输出 FAIL 提示信息。

   # shell 脚本中常用的组合示例
   echo $BASH | grep -q 'bash' || { exec bash "$0" "$@" || exit 1; }
   # 系统调用exec是以新的进程去代替原来的进程，但进程的PID保持不变。
   # 因此可以这样认为，exec系统调用并没有创建新的进程，只是替换了原来进程上下文的内容。原进程的代码段，数据段，堆栈段被新的进程所代替。
   ```

   > `&&` 的优先级高于 `||`，会优先执行。`cmd1 && cmd2 || cmd3` 等价于 `(cmd1 && cmd2) || cmd3`。

8. **`!` (逻辑非, NOT)**

   `!` 是逻辑非操作符，用于取反。它会将一个命令的退出状态反转。即，如果命令成功，`!` 会将其视为失败；如果命令失败，`!` 会将其视为成功。

   示例：

   ```bash
   ! ls nonexistent_file && echo "File does not exist"
   ```

   这里，`ls nonexistent_file` 失败，`!` 将其反转为成功状态，所以后面的 `echo` 命令会执行。

9. **条件测试中与或非**

   这些操作符主要用于 `test` 或 `[ ]` 结构中，用于测试文件属性或条件。

   - **`!`**：逻辑非（NOT），用于取反。
   - **`-a`**：逻辑与（AND），表示两个条件都必须为真。
   - **`-o`**：逻辑或（OR），表示其中一个条件为真即可。

   示例：

   ```bash
   [ ! -f "file.txt" ]  # 如果 file.txt 文件不存在，则返回真
   [ -f "file1.txt" -a -f "file2.txt" ]  # 两个文件都存在则返回真
   [ -f "file1.txt" -o -f "file2.txt" ]  # 其中一个文件存在则返回真
   ```

10. 条件测试中与或非和命令执行中与或非

    在 Shell 表达式中，`!`、`-a`、`-o`、`&&`、`||` 等符号用于逻辑操作，但是它们用于不同的上下文和语法场景。

    1. **条件测试中的逻辑与或非**（`!`、`-a`、`-o`）：

       ```bash
       if [ -f file1 -a -f file2 ]; then
         echo "Both files exist"
       fi
       ```

       这里 `-a` 检查两个文件是否都存在。

    2. **命令执行中的逻辑与或非**（`&&`、`||`、`!`）：

       ```bash
       ! ls nonexistent_file && echo "File does not exist"
       ```

       这里 `!` 将 `ls nonexistent_file` 的失败状态反转为成功，从而执行后面的 `echo`。

    **区别总结**：

    - **`! -a -o`** 用于条件测试（如 `[ ]` 或 `test`），典型场景是检查文件状态、比较字符串等。
    - **`&& ||`** 用于命令执行顺序控制，用来根据前一个命令的执行结果来决定是否执行后续命令。

这些符号和操作符是 Shell 脚本中的基础工具，用于控制命令执行顺序和条件逻辑，帮助我们构建复杂的命令逻辑。

## 单/双/反引号

在 Shell 中，单引号 `' '`, 双引号 `" "`, 和反引号 ` `` ` 用于不同的目的，尤其是在处理字符串和命令替换时。它们的功能如下：

1. 单引号 `' '`

   - **功能**：将字符串完全保留为字面值，不进行变量和命令替换。

   - **用途**：当你想确保字符串中的特殊字符（如 `$`, `*`, `\` 等）不被解释或替换时，使用单引号。

   - 示例：

     ```bash
     echo 'Hello $USER'
     ```

     输出：`Hello $USER`（`$USER` 不会被解析）

2. 双引号 `" "`

   - **功能**：允许变量替换和命令替换，但保留大多数其他字符的字面意义。

   - **用途**：当需要字符串保留特殊字符（如空格）并希望进行变量替换或命令替换时，使用双引号。

   - 示例：

     ```bash
     echo "Hello $USER"
     ```

     输出：`Hello your_username`（`$USER` 被替换成实际的用户名）

3. 反引号 ` `` ` 或 `$(...)`（推荐）

   - **功能**：用于**命令替换**，即执行括号中的命令，并将结果插入到外部命令中。

   - **用途**：当你需要将命令的输出用作另一个命令的参数时，使用反引号或 `$()`。

   - 示例：

     ```bash
     echo "Today is `date`"
     ```

     或者：

     ```bash
     echo "Today is $(date)"
     ```

     两者输出相同，例如：`Today is Fri Nov 8 15:30:00 UTC 2024`

   > **注意**：推荐使用 `$()` 语法，因为它支持嵌套，而反引号不支持。

**小结：**

- **单引号**：完全保留字符串内容。
- **双引号**：允许变量替换和命令替换，但保留大多数字符。
- **反引号或 `$()`**：用于命令替换，将命令的输出作为参数传递。

**经验示例：**

1. 命令拼接尽量整体加双引号

   > :point_right: 只要变量可能包含空格，就必须整体加双引号。
   > 另：无需给变量引用单独加双引号，整体加即可。

   ```bash
   # 当路径中含有空格
   INPUT_PATH="/path/with space"
   # 正确且推荐
   --input="${INPUT_PATH}/data/input1.bin"
   --input=/path/with space/data/input1.bin  # 作为一个完整参数传递给程序

   # 不加引号错误展开后如下
   --input=${INPUT_PATH}/data/input1.bin
   --input=/path/with
   space/model/configs/cl_customization.conf # 程序实际收到的是两个参数，直接炸。
   ```

## 双引号嵌套

## shell 命令展开

Shell 命令的展开是单次展开，按照固定顺序进行一次性展开。每种展开类型只会执行一次。不是递归展开。

举例说明：

1. 变量展开不会递归

   ```bash
   a='$b'
   b='$c'
   c='hello'
   echo $a  # 输出 $b，而不是递归展开到 hello
   ```

2. 命令替换不会递归

   ```bash
   cmd1='$(echo $cmd2)'
   cmd2='$(echo hello)'
   echo $(echo $cmd1)  # 输出 $(echo $cmd2)，不会继续展开
   ```

3. 要实现多次展开，需要使用 eval

   ```bash
   # 使用eval实现递归展开
   a='$b'
   b='$c'
   c='hello'
   eval echo $a  # 输出 $c
   eval eval echo $a  # 输出 hello
   ```

4. 实际应用示例

   ```bash
   # 单次展开
   var1="world"
   var2='$var1'
   echo $var2  # 输出: $var1

   # 使用eval强制多次展开
   eval echo $var2  # 输出: world

   # 命令替换也是单次
   cmd='$(echo "$(date)")'
   echo $cmd  # 输出: $(echo "$(date)")
   eval echo $cmd  # 输出: 当前日期
   ```

**重要说明**：

- shell 的标准展开是单次的
- 需要多次展开时必须显式使用 eval
- 过多的展开层次会使代码**难以维护和理解**
- 应尽量**避免复杂的多层展开**

## shell 命令展开优先级

Shell 命令展开遵循特定的顺序，完整的展开优先级（从高到低）：

- Brace expansion（大括号展开）
- Tilde expansion（波浪号展开）
- Parameter and variable expansion（参数和变量展开）
- Command substitution（命令替换）
- Arithmetic expansion（算术展开）
- Word splitting（词分割）
- Pathname expansion（路径名展开/通配符展开）

1. 大括号展开

   ```bash
   echo th{i,a}t  # 展开为 thit that
   ```

2. 波浪号展开 (~)

   ```bash
   echo ~/dir  # 展开为 /home/user/dir
   ```

3. 参数和变量展开

   ```bash
   name="John"
   echo $name    # 展开为 John
   echo ${name}  # 同上
   ```

4. 命令替换

   ```bash
   echo $(date)  # 执行date命令并替换结果
   echo `date`   # 同上
   ```

5. 算术展开

   ```bash
   echo $((2 + 2))  # 展开为 4
   ```

6. 单词分割(IFS)

   ```bash
   var="a b c"
   echo $var     # 分割为三个单词：a b c
   echo "$var"   # 保持为一个单词："a b c"
   ```

7. 路径名展开(通配符)

   ```bash
   echo *.txt    # 展开为所有.txt文件
   ```

**示例**：

```bash
# 展开顺序示例
user="john"
echo ~/${user}_file{1,2}.{txt,log}

# 展开步骤：
# 1. 大括号展开：~/john_file1.txt ~/john_file1.log ~/john_file2.txt ~/john_file2.log
# 2. 波浪号展开：/home/user/john_file1.txt ...
# 3. 变量展开：已在步骤1中完成
```

**注意事项**：

- 展开顺序是固定的，不可更改
- 引号会影响展开行为
- 展开结果会作为命令的参数

## 路径处理

在 shell 脚本中处理路径有几种常用方法：

1. 获取相对路径:

   ```bash
   # 获取当前脚本所在目录
   current_dir=$(dirname "$0")

   # 获取当前工作目录
   pwd_dir=$(pwd)

   # 获取当前脚本路径
   SCRIPT_DIR=$(realpath "$(dirname "$0")")
   echo "$SCRIPT_DIR"
   ```

2. 从绝对路径提取部分路径:

   ```bash
   full_path="/home/user/projects/test/file.txt"

   # 获取目录部分
   dir_path=$(dirname "$full_path")  # 结果: /home/user/projects/test

   # 获取文件名部分
   file_name=$(basename "$full_path")  # 结果: file.txt

   # 获取不带扩展名的文件名
   name_only=$(basename "$full_path" .txt)  # 结果: file
   ```

3. 使用参数展开:

   ```bash
   path="/home/user/projects/test/file.txt"

   # 提取最后一个/之前的内容
   before_last_slash=${path%/*}  # 结果: /home/user/projects/test

   # 提取最后一个/之后的内容
   after_last_slash=${path##*/}  # 结果: file.txt

   # 提取指定目录之后的路径
   sub_path=${path#*/user/}  # 结果: projects/test/file.txt
   ```

   参数展开匹配：

   ```bash
   file_folder="/home/user/test/project/file.txt"

   # 从开头匹配并删除最短匹配
   sub_path=${file_folder#*/test/}  # 结果: project/file.txt

   # 从开头匹配并删除最长匹配
   sub_path=${file_folder##*/test/}  # 结果: project/file.txt

   # 从结尾匹配并删除最短匹配
   sub_path=${file_folder%/test/*}  # 结果: /home/user

   # 从结尾匹配并删除最长匹配
   sub_path=${file_folder%%/test/*}  # 结果: /home/user
   ```

   参数展开操作符说明：

   - `#` - 从开头匹配删除，删除最短匹配
   - `##` - 从开头匹配删除，删除最长匹配
   - `%` - 从结尾匹配删除，删除最短匹配
   - `%%` - 从结尾匹配删除，删除最长匹配

## Shell 中调用 Python

除了直接以 `python xxx.py` 的方式运行 py 文件，对于简单的 python 代码，还可以使用 `python -c`。
`python -c` 是 Python 提供的一个命令行参数，意思是 **直接在命令行执行一段 Python 代码字符串**。

```python
python -c "代码"
```

比如：

```shell
yaml_file="xxx.yaml"
config_file=$(python3 -c "
import yaml,sys
with open('$yaml_file') as f:
    data = yaml.safe_load(f)
print(data['config_file'])
")
```

注意事项

- 代码一般用 **双引号** `"..."` 包裹，如果里面也要用引号，需要转义。
- 多行语句可以用 `;` 分隔。
- 如果逻辑太复杂，不建议用 `-c`，而是写到 `.py` 脚本里。

## Shell 中 `return`

**一、`return` 的基本概念**

`return` 用于从**函数**或**被 source 的脚本**中返回，并可以设置返回值（退出状态）。

`return` vs `exit` 的区别：

| 命令   | 作用范围                 | 效果                              |
| ------ | ------------------------ | --------------------------------- |
| exit   | 整个进程                 | 终止当前进程（脚本或 Shell 会话） |
| return | 当前函数或 source 的脚本 | 从函数或 source 返回到调用者      |

二、**`return` 的使用场景**

1. 在函数中使用

   ```bash
   #!/bin/bash

   my_function() {
       echo "In function"
       return 5        # 从函数返回，设置退出状态为5
       echo "Never printed"
   }

   echo "Before function call"
   my_function
   echo "Function exit code: $?"
   echo "Script continues"
   ```

   **输出：**

   ```bash
   Before function call
   In function
   Function exit code: 5
   Script continues
   ```

2. 在被 source 的脚本中使用

   ```bash
   # lib.sh
   #!/bin/bash
   echo "In lib.sh"
   return 10           # 从source返回
   echo "Never printed"

   # main.sh
   #!/bin/bash
   echo "Before source"
   source lib.sh
   echo "Source exit code: $?"
   echo "Main script continues"
   ```

   **输出：**

   ```bash
   Before source
   In lib.sh
   Source exit code: 10
   Main script continues
   ```

3. 在主脚本中直接使用 `return`（错误用法）

   ```bash
   #!/bin/bash
   echo "Start"
   return 1            # 错误！会导致 "can only return from function or sourced script"
   echo "Never reached"
   ```

**三、`return` 的退出状态**

- `return` 不带参数：返回上一个命令的退出状态
- `return 0`：成功返回
- `return 1-255`：带错误代码返回

## 时间戳

在 Shell（sh / bash）脚本中，**给变量名或变量值加入时间戳** 是非常常见的需求，比如：

**一、时间戳的获取方法**

1. 标准格式（人类可读）

   ```bash
   date "+%Y%m%d_%H%M%S"
   ```

   输出示例：

   ```log
   20251020_113045
   ```

   常见时间格式符对照表：

   | 格式符 | 含义                     | 示例      |
   | ------ | ------------------------ | --------- |
   | `%Y`   | 年（四位）               | `2025`    |
   | `%y`   | 年（两位）               | `25`      |
   | `%m`   | 月（01–12）              | `10`      |
   | `%d`   | 日（01–31）              | `20`      |
   | `%H`   | 小时（00–23）            | `14`      |
   | `%I`   | 小时（01–12, 12 小时制） | `02`      |
   | `%M`   | 分钟（00–59）            | `30`      |
   | `%S`   | 秒（00–60）              | `45`      |
   | `%a`   | 星期缩写（Sun–Sat）      | `Mon`     |
   | `%A`   | 星期全称                 | `Monday`  |
   | `%b`   | 月份缩写                 | `Oct`     |
   | `%B`   | 月份全称                 | `October` |
   | `%Z`   | 时区名                   | `CST`     |
   | `%z`   | 时区偏移                 | `+0800`   |

2. Unix 时间戳（秒级数字）

   ```bash
   date +%s
   ```

   输出示例：

   ```log
   1739998225
   ```

**二、使用**

1. 在变量值中加入时间戳

   ```bash
   TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
   LOG_FILE="run_log_${TIMESTAMP}.txt"

   echo "$LOG_FILE"
   # 输出: run_log_20251020_113045.txt
   ```

2. 在变量名中加入时间戳（动态变量名）

   Shell 本身**变量名是静态的字符串**，不能直接像 Python 那样动态创建变量，但可以通过 `eval` 或数组间接实现。

   - 方法 1：`eval` 动态定义变量名

     ```bash
     TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
     VARNAME="data_${TIMESTAMP}"
     eval "${VARNAME}='hello world'"

     # 访问动态变量
     eval "echo \${${VARNAME}}"
     # 输出：hello world
     ```

     > 注意：
     > `eval` 会执行字符串，**有安全风险**（尤其当变量来源不可信时）。

   - 方法 2：使用关联数组（推荐更安全）

     如果是 `bash`（非 `sh`）脚本：

     ```bash
     declare -A data_map
     key=$(date "+%Y%m%d_%H%M%S")
     data_map["data_$key"]="hello world"

     echo "${data_map["data_$key"]}"
     # 输出：hello world
     ```

     > 安全且灵活，不需要 `eval`。
