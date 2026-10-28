---
layout: programming_guide
title: "HW05 Programming Tips"
active_tab: hws
---

HW05 Programming Tips
=============================================================

[Back to HW05: Naive Bayes]({{ site.baseurl }}/hw/HW05.html)

This guide focuses on how to work with the HW05 starter code. It assumes you
are comfortable writing Python functions, loops, lists, and dictionaries.
No third-party libraries are required. The command-line parser, file-format
selection, and output formatting are already implemented.

<nav class="guide-nav" aria-label="On this page">
  <strong>On this page</strong>
  <ul>
    <li><a href="#understand-the-data-passed-between-functions">Data structures and function inputs</a></li>
    <li><a href="#read-csv-and-arff-without-losing-their-structure">Reading CSV and ARFF</a></li>
    <li><a href="#build-probability-tables-that-prediction-can-use-directly">Building probability tables</a></li>
    <li><a href="#use-log-scores-consistently">Working with log scores</a></li>
    <li><a href="#test-each-stage-independently">Testing and debugging</a></li>
  </ul>
</nav>

## Understand the data passed between functions

The readers return a `Partition`, the model trains on that partition, and
prediction operates on feature dictionaries. These are different inputs:

| Expression | Type | Meaning |
| --- | --- | --- |
| `partition.data` | `list[Example]` | The examples in a dataset. |
| `example.features` | `dict[str, str]` | One example's feature names and values. |
| `example.label` | `int` | Its class, from `0` through `K - 1`. |
| `partition.F` | `dict[str, list[str]]` | Each feature's possible values. |
| `partition.K` | `int` | The number of possible classes. |

For example, a single example might have
`features = {"color": "blue", "shape": "round"}` and label `1`.
The corresponding domains might include
`F = {"color": ["blue", "red"], "shape": ["round", "square"]}`.
A domain lists possibilities, including values absent from that example.

The aliases `FeatureValues` and `FeatureDomains` in `Partition.py` name the
two dictionary types above. They do not change how dictionaries behave.
When calling `model.classify(...)`, pass `example.features`, not `example`
or the entire partition. Keep feature values as strings, even when they look
like numbers; only class labels become integers.

## Read CSV and ARFF without losing their structure

For CSV, `csv.reader` handles delimiters and quoted fields. Read the header
once, then process the remaining rows:

```python
import csv
from io import StringIO

# StringIO lets you practice on a tiny CSV without creating a file.
with StringIO("color,shape\nblue,round\nred,square\n") as stream:
    reader = csv.reader(stream)
    names = next(reader)
    for row in reader:
        record = dict(zip(names, row))
        print(record)
```

For a real file, replace `StringIO(...)` with
`open(filename, newline="", encoding="utf-8")`. `next(reader)` consumes the
header; the loop starts at the first data row. Check row lengths before
using `zip`, which otherwise silently stops at the shorter input.

In the census reader, separate `sex` from the feature dictionary and collect
first-seen values for each remaining column in `F`. Strip surrounding
whitespace so `"Private"` and `" Private"` do not become different categories.

ARFF requires two phases. Before `@data`, collect attribute declarations;
after it, read examples. A Boolean such as `in_data` can track the phase.
Skip blank lines and full-line `%` comments. Compare keywords without regard
to case, but preserve the feature values themselves.

The header supplies domains, so retain declared values even if no data row
uses them. Map the final attribute's class values to integers in declaration
order. Do not infer `K` solely from labels observed in the rows: a declared
class might have no examples. The reader docstring specifies the supported
format; `re` is available if useful, but regular expressions are not required.

**Check before moving on:** inspect one returned example, its label,
`partition.F`, and the partition's size. A reader bug can otherwise look
like a probability or classification bug later.

## Build probability tables that prediction can use directly

The model's required storage layout is:

```text
log_class[k]                         → one class's log prior
log_feature[feature][value][k]        → one log likelihood
```

For example, `log_feature["color"]["blue"][1]` represents
`log P(color = blue | class = 1)`. Work through the indexing order when
constructing and debugging the tables.

Training belongs in `__init__`. Store the resulting tables as attributes
such as `self.log_class` so later methods can retrieve them. Prediction
should look up stored probabilities, not scan the training examples again.

A useful implementation sequence is to check class counts, then
feature-value counts within each class, then the smoothed log probabilities.
Include every declared feature value for every class, including zero-count
combinations. This is where Laplace smoothing matters.

Avoid shared mutable containers when initializing counts or matrices:

```python
rows = [[0, 0]] * 2       # Both entries refer to the same row.
rows[0][1] += 1
print(rows)              # [[0, 1], [0, 1]]

rows = [[0, 0] for _ in range(2)]  # Separate rows.
rows[0][1] += 1
print(rows)                       # [[0, 1], [0, 0]]
```

The same issue applies to lists stored under different dictionary keys:
create a fresh count list for each feature value.

## Use log scores consistently

`math.log` computes the natural logarithm. Apply it to the smoothed
probabilities, or use the equivalent difference of logarithms:

```python
import math

numerator, denominator = 3, 8
log_probability = math.log(numerator) - math.log(denominator)
assert math.isclose(log_probability, math.log(numerator / denominator))
```

Add log probabilities when combining features. Do not take the log of a
product of many small probabilities: the product can already have rounded
to zero before `math.log` sees it. Negative log scores are expected, and
`-2.0` is a higher score than `-10.0`.

`predict_log_scores()` returns one score per class, in class order.
`classify()` returns the **index of the highest score**, not the score itself.
Remember the required smallest-label tie break. No exponentiation or
posterior normalization is needed to select the highest-scoring class.

A value with zero observations **within a class** still has a smoothed
probability if it belongs to the feature's domain. A test value **outside
the training domain** is a different case: the HW05 interface requires
`KeyError`. Do not silently expand domains using test data.

## Test each stage independently

The computational methods return results without printing or changing their
inputs. This lets you test a reader, score, or metric without running the
whole experiment. The provided `main()` handles presentation.

Start with a tiny partition whose counts you can calculate by hand. Check
that the class probabilities sum to one and that, for a fixed feature and
class, its value probabilities sum to one. Since the tables store logs,
use `math.exp` to recover probabilities for this debugging check only.
Use approximate comparisons for floating-point results.

For metrics, use unequal class sizes and some mistakes in both directions.
Remember that confusion-matrix rows are actual labels and columns are
predictions. Accuracy weights examples equally; BER averages the error
rates of the actual classes equally. A class with no actual examples has an
undefined error rate, which the supplied BER docstring requires you to
handle with `ValueError`.

Run a focused public test while implementing a particular stage:

```bash
python3 -m unittest tests.TestDataAndMetrics.test_csv_label_is_excluded -v
python3 -m unittest tests.TestNaiveBayes.test_smoothed_probabilities_and_absent_class -v
```

Then run `python3 tests.py`, followed by the tennis and zoo experiments,
before using the larger census datasets. These commands should be run from
the homework folder so that local imports and relative data paths resolve.

If a test fails, inspect the smallest intermediate result that could explain
it: a parsed category, a count, one stored likelihood, or one class score.
For unexpected `KeyError`s, `repr(value)` helps reveal whitespace, and
examining the dictionary at each nesting level helps locate an incorrect
lookup. Remove temporary debugging prints from computational helpers before
submitting.
