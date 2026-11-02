# Smart Emergency Resource Allocator

**DAA Assignment 2 — GUI-Based Algorithm Implementation**

## Overview
A desktop application that selects the most valuable set of emergency resources under a fixed carrying capacity. It uses the **0/1 Knapsack algorithm with Dynamic Programming**.

## Requirements
- Python 3.9 or later
- Tkinter (usually included with standard Python installations)

No third-party Python packages are required.

## Run
```bash
python app.py
```

## How to use
1. Review the sample emergency resources, or add your own.
2. Enter a resource name, positive integer weight, and non-negative priority value; click **Add resource**.
3. Remove a resource by selecting it and clicking **Remove selected**.
4. Enter the maximum carrying capacity.
5. Click **Find optimal allocation**.
6. Use **Next step** and **Previous step** to inspect how each DP row is built. Select **Show complete table** to display the final table.

## Algorithm
Let `dp[i][w]` be the maximum priority obtainable using the first `i` resources and capacity `w`.

- If resource `i` is too heavy: `dp[i][w] = dp[i-1][w]`
- Otherwise: `dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]])`

Each resource can be selected at most once.

## Complexity
- Time: O(nW)
- Space: O(nW)
where `n` is the number of resources and `W` is the capacity.

## Validation
The GUI accepts integer capacity from 0 to 200, requires positive resource weights and non-negative priority values, and displays validation messages for invalid input.
