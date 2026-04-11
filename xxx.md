[toc]

/*
 * Kernel 实现说明：
 *
 * GlobalTensor/LocalTensor 关于 sub-byte（亚字节）数据类型偏移计算：
 * 1. 起始地址初始化(多核GM起始地址、单核内各L1Tensor起始地址)
 *    - 因 sizeof(hif4_t/mx_s4_t) = 1，因此起始地址需手动把元素偏移转换成字节偏移
 *    - 提供 ElementsToBytes 函数，支持类型详见函数实现
 * 2. 分块偏移量计算(GM及各Buffer分块偏移)：
 *    - 对 int4b_t 类型，operator[] 在 V516 前已经可以传入 offset 正确计算地址偏移量
 *    - 对 hif4_t/mx_s4_t 类型，operator[] 在 V516 新适配，也可直接根据 offset 计算地址偏移
 *
 * fm 的 GlobalTensor 数据类型用 A_T
 * - fm 可能为 hif4_t/mx_fp8_e4m3_t，用 operator[] 均可正确计算偏移
 *
 * fmScale 在 GM 上数据类型用 B8, 在 L1 上固定用 B16
 * - MX 格式 32 个数共享 1B 的 Scale, HF 格式 64 个数共享 4B Scale。传给 kernel 的类型可能为 B8 或 B32
 * - GlobalTensor
 *
 * weight 的 GlobalTensor 数据类型固定用 B8：
 * - weight 可能为 uint2p5b_t/uint2b_t/mx_s4_t/mx_fp8_e4m3_t，仅 mx_s4_t 可用 [] 偏移，其余需手算偏移
 * - 模板归一需同时支持上述类型，考虑代码一致性 GlobalTensor 固定用 B8，手动根据类型计算地址偏移
 */
