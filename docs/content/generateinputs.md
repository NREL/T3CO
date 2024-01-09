# Table of Contents

* [run.generateinputs](#run.generateinputs)
  * [generate](#run.generateinputs.generate)

<a id="run.generateinputs"></a>

# run.generateinputs

<a id="run.generateinputs.generate"></a>

#### generate

```python
def generate(vocation, dst=gl.OPTIMIZATION_AND_TCO_RCRS)
```

This function aggregates specifications from users for powertrains, desired ranges, component costs etc. into two
csv files - FASTSimInputs and OtherInputs

**Arguments**:

- `vocation` _str_ - Vocation type description
- `dst` _str, optional_ - results directory file path. Defaults to gl.OPTIMIZATION_AND_TCO_RCRS.

