# Scaling the Loss Calculation Model

## Scalability Analysis

The current implementation is a direct translation of the formula into python. While it is efficient to compute the loss for few buildings, it must be optimised to compute the loss of a very large number of building.

This is also true for the `load_data` function - it is simple and readable, and suitable for a small number of buildings, but not appropriate for a large dataset as it would fill up the RAM.

## Optimization Strategies

Since the compution for a given building is independant from others, it is easy to parallelise the whole process by dividing the dataset into multiple chunks that will be computed in parallel using multiple threads. For a very large dataset it could even be executed on multiple machines.

The interdediate results will be summed together to give the final result.

Here is an example implementation using `numpy` (multithreaded).

```python
import numpy as np

def loss_estimate(construction_costs, floor_areas, inflation_rate, hazard_probabilities, discount_rate, years):
    inflation_factors = np.exp(inflation_rate * floor_areas / 1000)
    discounted_values = (1 + discount_rate) ** years
    losses = (construction_costs * inflation_factors * hazard_probabilities) / discounted_values
    return losses

# Testing with 10M rows
construction_costs = np.random.rand(10**7) * 1e6
floor_areas = np.random.rand(10**7) * 200
hazard_probabilities = np.random.rand(10**7) * 0.1
years = 10

# Losses for each building
losses = loss_estimate(
    construction_costs,
    floor_areas,
    inflation_rate=0.02,
    hazard_probabilities=hazard_probabilities,
    discount_rate=0.05,
    years=years
)

total_losses = np.sum(losses)
```

## Resource Management

In order to avoid OOM errors when loading the dataset we can use (and combine) two strategies:
- Using a more efficient data format (e.g `zarr`), because `json` contains a lot of repetitions (in particular the property names).
- Instead of loading all the data in memory, divide them in chunks that are streamed to the function.

Using a library like `ijson` can help with streaming: it will still read the full data file at once, but only allocate intermediate objects as we need them, allowing to reduce the total memory used at once because intermediate objects can be garbage collected after processing.

Slightly altering the json data can help to reduce the payload size, for example:

In CSV:

```csv
1, 2000, 1200, 0.1, 0.03
```

Or [jsonl](https://jsonlines.org/):

```json
[1, 2000, 1200, 0.1, 0.03]
```

instead of

```json
{
    "buildingId": 1,
    "floor_area": 2000,
    "construction_cost": 1200,
    "hazard_probability": 0.1,
    "inflation_rate": 0.03
}
```

This is not the most scalable approach but a "quick win" since the total memory will most likely be the bottleneck. Loading `csv` or `jsonl` is easier to stream as each line contains the data of a building. We can extend the `numpy` sample code above to load the data by chunk of 1M lines for example.

When this is not enough, converting the data to `zarr` or using `numpy.memmap` (require preprocessing the data to create a binary file that will be mapped) will support a larger dataset.

When this approach also hits its limit, we can divide the data into multiple sets that will processed in separate machines (e.g using `dask`).
