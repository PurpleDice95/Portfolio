# A Star Search Visualization  

A visualization, on an editable grid maze, of the A-star pathfinding algorithm  

# Run instructions  
  - Requires modules *numpy* and *pygame*  
  - Desired *grid size*, *speed of execution*, and *weightage between heuristics* can be set in main.py  
  - Run *main.py*  
  - Each grid square is colored according to:
    * **blue** - obstructed square  
    * **green** - empty square
    * **red** - start square
    * **pink** - end square
    * **white** - square in queue to be explored
    * **black** - square is part of the shortest path
  - Controls are as follows:  
    * **Tab** - toggles all squares between blue and green
    * **LMB** - places a blue square on the cursor
    * **RMB** - places a green square on the cursor
    * **MMB** - toggles between placing a red square and a green square on the cursor, starting with red
    * ***Any numeric key*** - sets the weightage between heuristics to be *0.1 times the number pressed*
  - After both start and end squares are present the program will begin pathfinding


