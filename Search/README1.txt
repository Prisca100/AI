For search, we are basically solving one problem...Getting from initial state to a desired state. For that, we define some properties:


State: Any configuration of the agent in it's environments

Initial State: The starting point of the search
Goal State: The desired endpoint
Actions: Ideally a function that takes in a state and spits out all the possible steps it can take in that state.
Transition model: Given a state and an action, the resulting possible states obtained from applying the action to the given state
Agent: Percieves the environment and act on it's environement.
Optimal solution: The best solution out of all possible solutions.




How to perform searches?
1. Start with a frontier that contains the initial state
2. Start with an empty explored set
Repeat (Loop)
3. if frontier is empty: return no solution
4. Remove a node fron the frontier
5. if node contains goal state return, call it goal
6. Add node to the explored set
7. Expand node: add resulting node to the frontier if they are not already in the frontier or expanded set.