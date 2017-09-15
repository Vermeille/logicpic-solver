# logicpic-solver

A solver for the game [LogicPic](https://play.google.com/store/apps/details?id=br.com.tapps.logicpic)

The game is a grid initialized with blanks, some of the cell must be checked.
Each column and row contains constraints of which cell must be in it. For
instance, "3 4 1" means that there must be 3 consecutive checked cells, at
least a blank, 4 consecutive checked cells, at list one blank, and one checked
cell.

The algorithm works as follow:

1. Initialize a worklist containing all rows and columns
2. Until the worklist is empty
    1. Read the first element of that worklist
    2. Generate all the possible combinations satisfying the constraints on the
       given row/column
    3. Eliminate the ones that are ruled out by what's already on the grid
    4. Find the cells that remain checked / unchecked among all valid
       combinations
    5. Write in the grid '.' for all the cells that are sure to remain
       unchecked, '#' for all the cells that are sure to be checked, leave a
       blank where we don't know for sure.
    6. Push in the worklist all the modified rows / columns.
3. Enjoy your solution!
