# cerburus

Print [Polars](https://pola.rs) DataFrames with hierarchical headers in plain text.

## Usage

```python
import cerburus
import polars as pl

df = pl.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6], "d": [7, 8]})
cerburus.pprint(
    df,
    headers=[
        ["1st title", "1st title", "2nd title", "2nd title"],
        ["1st subtitle", "2nd subtitle", "1st subtitle", "2nd subtitle"],
    ],
)
```

prints

```
         1st title                   2nd title
 1st subtitle 2nd subtitle   1st subtitle 2nd subtitle
            1            3              5            7
            2            4              6            8

```

## Installation

```bash
pip install cerbursus
```

## Development state

This package is a proof-of-concept and in the early stage of development. It should not be relied on
for production code.

Is something not working? Report an issue on our [GitHub issue tracker](https://github.com/rhshadrach/pytest-ndb/issues)!
