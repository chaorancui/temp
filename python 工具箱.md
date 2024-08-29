# python 工具箱

## numpy

### 1d 数组每个元素后 padding

```cpp
def zero_padding_between_elements(input_arr, padding_num):
    output_arr = np.array([])
    zeros_arr = np.zeros(padding_num)
    for item in input_arr:
        output_arr = np.r_[output_arr, item, zeros_arr]
    return output_arr.astype(input_arr.dtype)
```

### 1d 数组交错拼接

```cpp
def interleave_1d_arr(*args):
    output_arr = np.vstack(args)
    return np.ravel(output_arr, order='F')
```

