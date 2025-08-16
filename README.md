# Cache Simulator

This project implements a configurable cache simulator as described in the MP1 instructions. It supports various cache configurations, replacement policies, and inclusion properties, and provides tools for analysis and validation.


## How to Run

The main simulator is run using [`sim_cache.py`](sim_cache.py) from the command line:

```powershell
python sim_cache.py <BLOCKSIZE> <L1_SIZE> <L1_ASSOC> <L2_SIZE> <L2_ASSOC> <REPLACEMENT_POLICY> <INCLUSION_PROPERTY> <TRACE_FILE>
```

- `<BLOCKSIZE>`: Block size in bytes (e.g., 32)
- `<L1_SIZE>`: L1 cache size in bytes (e.g., 1024)
- `<L1_ASSOC>`: L1 associativity (e.g., 4)
- `<L2_SIZE>`: L2 cache size in bytes (e.g., 8192)
- `<L2_ASSOC>`: L2 associativity (e.g., 8)
- `<REPLACEMENT_POLICY>`: `0` for [LRU](lru.py), `1` for [FIFO](fifo.py)
- `<INCLUSION_PROPERTY>`: `0` for non-inclusive, `1` for inclusive
- `<TRACE_FILE>`: Path to the memory access trace file (e.g., [`tests/traces/gcc_trace.txt`](tests/traces/gcc_trace.txt))

Example:
```powershell
python sim_cache.py 32 1024 4 8192 8 0 0 tests\traces\gcc_trace.txt
```


## Options and Features

- **Replacement Policies:** [LRU](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)) and [FIFO](https://en.wikipedia.org/wiki/Cache_replacement_policies#First_in,_first_out_(FIFO)) are supported.
- **Inclusion Properties:** Both inclusive and non-inclusive caches are supported ([Learn more](https://en.wikipedia.org/wiki/Cache_inclusion_policy)).
- **Trace Files:** Use the provided traces in [`tests/traces/`](tests/traces/) for simulation.
- **Graphs:** Scripts like [`graph_missrate.py`](graph_missrate.py), [`graph_inclusion.py`](graph_inclusion.py), and [`graph_replacement.py`](graph_replacement.py) generate plots to analyze cache performance under different configurations.


## Validation and Debugging

- **Validation Runs:** Use files in [`tests/validation_runs/`](tests/validation_runs/) to compare simulator output against expected results.
- **Debug Runs:** Use files in [`tests/debug_runs/`](tests/debug_runs/) for step-by-step debugging and analysis.


## Output

The simulator prints a detailed summary of the cache configuration and statistics after each run. Output includes:

- **Configuration Details:** All parameters used for the run (block size, cache sizes, associativity, replacement policy, inclusion property, trace file).
- **Access Statistics:** Number of reads, writes, read misses, write misses, and writebacks for both L1 and L2 caches.
- **Miss Rates:** Calculated for both L1 and L2 caches, helping you analyze cache efficiency.
- **Writebacks:** Number of blocks written back to memory.
- **Final Cache State:** Optionally, the contents of each cache set and block, including dirty bits and tags.

For more details and formatting, see [`display.py`](display.py). Example output:

```
===== Simulator configuration =====
BLOCKSIZE:             32
L1_SIZE:               1024
L1_ASSOC:              4
L2_SIZE:               8192
L2_ASSOC:              8
REPLACEMENT POLICY:    LRU
INCLUSION PROPERTY:    non-inclusive
trace_file:            tests\traces\gcc_trace.txt

L1 reads:              10000
L1 read misses:        1200
L1 writes:             5000
L1 write misses:       600
L1 miss rate:          0.12
L1 writebacks:         300
L2 reads:              1800
L2 read misses:        400
L2 writes:             900
L2 write misses:       200
L2 miss rate:          0.22
L2 writebacks:         100
Memory traffic:        700
```

This output helps you validate your implementation and analyze cache behavior under different configurations.


## Files Overview

- [`sim_cache.py`](sim_cache.py): Main entry point for running the simulator.
- [`cache.py`](cache.py): Core cache logic and data structures.
- [`lru.py`](lru.py), [`fifo.py`](fifo.py): Replacement policy implementations.
- [`display.py`](display.py): Output formatting and statistics display.
- [`graph_*.py`](graph_missrate.py), [`graph_inclusion.py`](graph_inclusion.py), [`graph_replacement.py`](graph_replacement.py): Scripts for generating performance graphs.
- [`tests/`](tests/): Contains trace files, validation runs, and debug runs.


## Requirements

- Python 3.x
- [`matplotlib`](https://matplotlib.org/) (for graph scripts)

---
For more details, refer to the [MP1 instructions](MP1_Instructions.pdf).