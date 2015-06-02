# Mazes
Maze Generator Algorithms and Solver in Python (Pygame)

Generate a maze in Pygame using:
- generator_algorithm = depth_first_search, random_kruskal, random_prim, hunt_and_kill, binary_tree
- solver_algorithm = a_star, bidirectional_a_star
- heuristic = manhattan, euclidean, chebyshev

```Python
# visualize(height, width, generator_algorithm, solver_algorithm, heuristic)
from maze import *
visualize(25, 25, depth_first_search, a_star, manhattan)
```

![demo](/dfs.gif)
============================================================

**Random Kruskal:**

![demo](/kruskal.gif)

**Random Prim:**

![demo](/prim.gif)

**Hunt and Kill:**

![demo](/hunt.gif)

**Binary Tree:**

![demo](/tree.gif)

**Bidirectional A*:**

![demo](/ba.gif)
