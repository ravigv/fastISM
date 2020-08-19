# FastISM

A Keras implementation for fast in-silico mutagenesis for convolution-based architectures.

## Usage

For any Keras `model` that takes in sequence as input of dimensions `(batch_size, seqlen, num_chars)`, perform ISM as follows:

```python
# for now, add repo to sys.path
from fast_ism import FastISM

fast_ism_model = FastISM(model)

for seq_batch in sequences:
    ism_seq_batch = fast_ism_model(seq_batch)
```
