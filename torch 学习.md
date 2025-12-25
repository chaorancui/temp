[toc]

# torch 学习

## 行向量 vs 列向量的惯例

1. **在深度学习中的惯例，Transformer/PyTorch 惯例**

   数据矩阵： $X = (batch, seq\_len, d\_model)$
   每一行是一个样本 token
   权重矩阵：$W (d_{in}, d_{out})$
   前向传播：$Y = XW$

   **这是"行向量惯例"（Row-vector convention）**

2. **在传统线性代数中，传统数学惯例**

   向量是列向量：$x ∈ ℝ^d (d×1)$
   矩阵变换：$y = Ax$

   **这是"列向量惯例"（Column-vector convention）**

## torch.nn.Linear

> reference:
> [Reference API > torch.nn > Linear](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html)

```python
class torch.nn.Linear(in_features, out_features, bias=True, device=None, dtype=None)
```

Applies an affine linear transformation to the incoming data:
$$ y = xA^{T} + b $$

其中：

- $A \in \mathbb{R}^{out\_features \times in\_features}$
- $b \in \mathbb{R}^{out\_features}$

This module supports TensorFloat32.

**Parameters:**

- **in_features** (int) – size of each input sample
- **out_features** (int) – size of each output sample
- **bias** (bool) – If set to False, the layer will not learn an additive bias. Default: True

**Shape:**

<!--prettier-ignore-->
- Input: $ (\star, H_{in}) $, where $ \star $ means any number of dimensions including none and $H_{in} = in\_features $.
- Output: $ (\star, H_{out}) $, where all but the last dimension are the same shape as the input and $ H_{out} = out\_features $.

**Variables:**

<!--prettier-ignore-->
- **weight** (torch.Tensor) – the learnable weights of the module of shape $ (out\_features, in\_features) $. The values are initialized from $ U(-\sqrt{k}, \sqrt{k}) $, where $ k = \frac{1}{in\_features} $.
- **bias** – the learnable bias of the module of shape $ (out_features) $. If bias is True, the values are initialized from $ U(-\sqrt{k}, \sqrt{k}) $, where $ k = \frac{1}{in\_features} $.

**Examples:**

```python
m = nn.Linear(20, 30)
input = torch.randn(128, 20)
output = m(input)
print(output.size())
torch.Size([128, 30])
extra_repr()[source]
```

## torch.triu

> reference:
> [Reference API > torch.triu](https://docs.pytorch.org/docs/stable/generated/torch.triu.html)

```python
- torch.**triu**(*input*, *diagonal=0*, ***, *out=None*)
```

Returns the upper triangular part of a matrix (2-D tensor) or batch of matrices `input`, the other elements of the result tensor `out` are set to 0.

The upper triangular part of the matrix is defined as the elements on and above the diagonal.The argument [`diagonal`](https://docs.pytorch.org/docs/stable/generated/torch.diagonal.html#torch.diagonal) controls which diagonal to consider. If [`diagonal`](https://docs.pytorch.org/docs/stable/generated/torch.diagonal.html#torch.diagonal) = 0, all elements on and above the main diagonal are retained. A positive value excludes just as many diagonals above the main diagonal, and similarly a negative value includes just as many diagonals below the main diagonal.

The main diagonal are the set of indices $ {(i, i)} for i \in [0, min⁡{d_1,d_2} - 1] $ where $ d_1, d_2 $ are the dimensions of the matrix.

**Parameters：**

- **input** (_Tensor_) – the input tensor.
- **diagonal** (_int_) – the diagonal to consider

  | diagonal | 含义                       |
  | -------- | -------------------------- |
  | `0`      | 保留主对角线及以上         |
  | `1`      | 主对角线以上（不含对角线） |
  | `-1`     | 包含主对角线下一行         |

**Keyword Arguments：**

- **out** (_Tensor_, _optional_) – the output tensor.Example:`a = torch.r`
