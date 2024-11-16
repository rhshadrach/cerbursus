import polars as pl

import cerbursus


def assert_match(result, expected):
    error_found = False
    for k, (line_r, line_e) in enumerate(zip(result.split("\n"), expected.split("\n"))):
        if line_r.rstrip() != line_e.rstrip():
            print(k, f"'{line_r.rstrip()}'")  # noqa: T201
            print(k, f"'{line_e.rstrip()}'")  # noqa: T201
            error_found = True
    assert not error_found


def test_short_titles():
    headers = [
        ["title1", "title1", "title2", "title2"],
        ["subtitle1", "subtitle2", "subtitle1", "subtitle2"],
    ]
    df = pl.DataFrame({"a": [1, 1, 2], "b": [3, 4, 5], "c": 6, "d": 7})
    result = "\n" + cerbursus.to_string(df, headers)
    expected = """
        title1                title2
 subtitle1 subtitle2   subtitle1 subtitle2
         1         3           6         7
         1         4           6         7
         2         5           6         7 """
    assert_match(result, expected)


def test_long_titles():
    headers = [
        [
            "somereallyreallylongtitle1",
            "somereallyreallylongtitle1",
            "somereallyreallylongtitle2",
            "somereallyreallylongtitle2",
        ],
        ["subtitle1", "subtitle2", "subtitle1", "subtitle2"],
    ]
    df = pl.DataFrame({"a": [1, 1, 2], "b": [3, 4, 5], "c": 6, "d": 7})
    result = "\n" + cerbursus.to_string(df, headers)
    expected = """
 somereallyreallylongtitle1   somereallyreallylongtitle2
     subtitle1 subtitle2          subtitle1 subtitle2
             1         3                  6         7
             1         4                  6         7
             2         5                  6         7    """
    assert_match(result, expected)


def test_short_titles_and_subtitles():
    headers = [["a", "a", "b", "b"], ["c", "d", "c", "d"]]
    df = pl.DataFrame({"a": [1, 1, 2], "b": [3, 4, 5], "c": 6, "d": 7})
    result = "\n" + cerbursus.to_string(df, headers)
    expected = """
  a     b
 c d   c d
 1 3   6 7
 1 4   6 7
 2 5   6 7 """
    assert_match(result, expected)


def test_long_value_left():
    headers = [["a", "a", "b", "b"], ["c", "d", "c", "d"]]
    df = pl.DataFrame({"a": [10000000, 1, 2], "b": [3, 4, 5], "c": 6, "d": 7})
    result = "\n" + cerbursus.to_string(df, headers)
    expected = """
      a        b
     c    d   c d
 10000000 3   6 7
        1 4   6 7
        2 5   6 7 """
    assert_match(result, expected)


def test_long_value_right():
    headers = [["a", "a", "b", "b"], ["c", "d", "c", "d"]]
    df = pl.DataFrame({"a": [1, 1, 2], "b": [3, 4, 5], "c": 10000000, "d": 7})
    result = "\n" + cerbursus.to_string(df, headers)
    expected = """
  a         b
 c d       c    d
 1 3   10000000 7
 1 4   10000000 7
 2 5   10000000 7 """
    assert_match(result, expected)


def test_long_value_both():
    headers = [["a", "a", "b", "b"], ["c", "d", "c", "d"]]
    df = pl.DataFrame({"a": [10000000, 1, 2], "b": [3, 4, 5], "c": 10000000, "d": 7})
    result = "\n" + cerbursus.to_string(df, headers)
    expected = """
      a            b
     c    d       c    d
 10000000 3   10000000 7
        1 4   10000000 7
        2 5   10000000 7 """
    assert_match(result, expected)


def test_three_levels():
    headers = [4 * ["alpha"], ["a", "a", "b", "b"], ["c", "d", "c", "d"]]
    df = pl.DataFrame({"a": [10000000, 1, 2], "b": [3, 4, 5], "c": 10000000, "d": 7})
    result = "\n" + cerbursus.to_string(df, headers)
    expected = """
          alpha
      a            b
     c    d       c    d
 10000000 3   10000000 7
        1 4   10000000 7
        2 5   10000000 7 """
    assert_match(result, expected)


def test_three_levels_long_values():
    headers = [
        ["alpha", "alpha", "beta", "beta"],
        ["a", "a", "b", "b"],
        ["c", "d", "c", "d"],
    ]
    df = pl.DataFrame({"a": [10000000, 1, 2], "b": [3, 4, 5], "c": 10000000, "d": 7})
    result = "\n" + cerbursus.to_string(df, headers)
    expected = """
    alpha          beta
      a              b
     c    d         c    d
 10000000 3     10000000 7
        1 4     10000000 7
        2 5     10000000 7 """
    assert_match(result, expected)


def test_no_headers():
    result = "\n" + cerbursus.to_string(pl.DataFrame({"a": [1, 1, 2], "b": [3, 4, 5]}))
    expected = """
 a b
 1 3
 1 4
 2 5 """
    assert_match(result, expected)
