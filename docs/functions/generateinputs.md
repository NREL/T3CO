# Table of Contents

* [t3co/run/generateinputs](#t3co/run/generateinputs)
  * [generate](#t3co/run/generateinputs.generate)

<a id="t3co/run/generateinputs"></a>

# t3co/run/generateinputs

<a id="t3co/run/generateinputs.generate"></a>

#### generate

```python
def generate(vocation: str, dst: str = gl.OPTIMIZATION_AND_TCO_RCRS)
```

This function aggregates specifications from users for powertrains, desired ranges, component costs etc. into two
csv files - FASTSimInputs and OtherInputs

**Arguments**:

- `vocation` _str_ - Vocation type description
- `dst` _str, optional_ - results directory file path. Defaults to gl.OPTIMIZATION_AND_TCO_RCRS.

