import polars as pl


def reduce_headers(headers):
    if len(headers) == 1:
        return []
    taker = [0]
    level = headers[-2]
    for k, (prev_label, label) in enumerate(zip(level[1:], level)):
        if prev_label != label:
            taker.append(k + 1)
    result = [[level[idx] for idx in taker] for level in headers[:-1]]
    return result


def add_label(column, label, first=False):
    values_width = column.str.len_chars().max()
    width = max(len(label), values_width)
    diff = width - len(label)
    left = diff // 2 + diff % 2
    right = diff // 2
    label = " " * left + label + " " * right
    if first:
        result = pl.concat([pl.Series(values=[label]), column.str.pad_start(width)])
    else:
        diff = width - values_width
        left = diff // 2 + diff % 2
        right = diff // 2
        result = pl.concat([pl.Series(values=[label]), " " * left + column + " " * right])
    return result


def to_string(
    df,
    headers,
):
    columns = [c.cast(pl.String) for c in df]
    spacer = 1
    first_loop = True
    while len(headers) > 0:
        level = [""] * len(headers[0]) if len(headers) == 1 else headers[-2]
        new_columns = []
        for i in range(len(level)):
            column_with_label = add_label(columns[i], headers[-1][i], first=first_loop)
            if i == 0 or level[i - 1] != level[i]:
                new_columns.append(column_with_label)
            else:
                new_columns[-1] += " " * spacer + column_with_label

        columns = new_columns
        first_loop = False
        headers = reduce_headers(headers)
        spacer += 2

    assert len(columns) == 1
    frame = columns[0].to_frame()
    with pl.Config(
            set_tbl_formatting="NOTHING",
            set_tbl_hide_dataframe_shape=True,
            set_tbl_hide_dtype_separator=True,
            set_tbl_hide_column_data_types=True,
            set_tbl_hide_column_names=True,
            fmt_str_lengths=1_000_000,
    ):
        return str(frame)


def pprint(df, headers) -> None:
    print(to_string(df, headers))
