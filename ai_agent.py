import random
import time
import tkinter as tk

# Define grid size
GRID_SIZE = 5
DIRT_PROB = 0.01  # Probability of dirt appearing per turn
TURNS = 200
CELL_SIZE = 50  # Pixel size of each grid cell

# Actions the agent can take
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'SUCK', 'STAY']



class Environment:
    def __init__(self, canvas):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # 0 = clean, 1 = dirty
        self.agent_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
        self.score = 0
        self.canvas = canvas
        self.rects = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.visited = set()
        self.consecutive_clean_count = 0
        self.draw_grid()
    
    def randomly_add_dirt(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if random.random() < DIRT_PROB:
                    self.grid[i][j] = 1
    
    def perform_action(self, action, performance_function):
        x, y = self.agent_pos
        prev_pos = (x, y)
        if action == 'UP' and x > 0:
            self.agent_pos[0] -= 1
            
        elif action == 'DOWN' and x < GRID_SIZE - 1:
            self.agent_pos[0] += 1
        elif action == 'LEFT' and y > 0:
            self.agent_pos[1] -= 1
        elif action == 'RIGHT' and y < GRID_SIZE - 1:
            self.agent_pos[1] += 1
        
        # Compute reward based on performance function
        self.score += performance_function(self, action, prev_pos)
        self.update_grid()

    def count_ones(self):
        # Count how many 1's are in the grid
        count = 0
        for row in self.grid:
            count += row.count(1)  # Count 1's in each row
        return count

    
    def draw_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x0, y0 = j * CELL_SIZE, i * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                self.rects[i][j] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
        self.update_grid()
    
    def update_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = "white"
                if self.grid[i][j] == 1:
                    color = "brown"  # Dirty tile
                if [i, j] == self.agent_pos:
                    color = "blue"  # Agent
                self.canvas.itemconfig(self.rects[i][j], fill=color)
        self.canvas.update()
        time.sleep(0.2)

# Performance Function
def configurable_performance(env, action, prev_pos):
    score = 0
    log = []

    # Reward for cleaning a dirty tile
    if action == 'SUCK' and env.grid[env.agent_pos[0]][env.agent_pos[1]] == 1:
        score += CLEANED_TILE
        log.append(f"CLEANED_TILE +{CLEANED_TILE}")
        env.grid[env.agent_pos[0]][env.agent_pos[1]] = 0

    # Penalty for unnecessary suction
    elif action == 'SUCK' and env.grid[env.agent_pos[0]][env.agent_pos[1]] == 0:
        score += UNNECESSARY_SUCK
        # print("HERE: ", env.grid[env.agent_pos[0]][env.agent_pos[1]])
        log.append(f"UNNECESSARY_SUCK {UNNECESSARY_SUCK}")
    
    # Penalty for moving
    if action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        score += MOVE_PENALTY
        log.append(f"MOVE_PENALTY {MOVE_PENALTY}")
    
    # Penalty for attempting to go out of bounds
    if env.agent_pos == list(prev_pos) and action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        score += OUT_OF_BOUNDS_ATTEMPT
        log.append(f"OUT_OF_BOUNDS_ATTEMPT {OUT_OF_BOUNDS_ATTEMPT}")
    
    # Reward for efficiency: every 3 consecutive cleans give extra points
    if action == 'SUCK' and env.grid[env.agent_pos[0]][env.agent_pos[1]] == 1:
        env.consecutive_clean_count += 1
        if env.consecutive_clean_count % 3 == 0:
            score += CONSECUTIVE_CLEANS_BONUS
            log.append(f"CONSECUTIVE_CLEANS_BONUS +{CONSECUTIVE_CLEANS_BONUS}")
    else:
        env.consecutive_clean_count = 0  # Reset if not cleaning
    
    # Penalty for idling
    if action == 'STAY':
        score += IDLE_PENALTY
        log.append(f"IDLE_PENALTY {IDLE_PENALTY}")
    
    # Reward for exploring a new tile
    if tuple(env.agent_pos) not in env.visited:
        env.visited.add(tuple(env.agent_pos))
        score += EXPLORED_NEW_TILE
        log.append(f"EXPLORED_NEW_TILE +{EXPLORED_NEW_TILE}")
    
    # Print concise summary for each move
    if log:
        print(" | ".join(log))
    
    return score


# Agent Strategy
def lazy_agent(env):
    x, y = env.agent_pos
    if env.grid[x][y] == 1:
        return 'SUCK'
    
    # Check neighboring cells in all 4 directions and avoid going out of bounds
    for dx, dy, action in [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:  # Only consider valid positions
            if env.grid[nx][ny] == 1:
                return action
    
    # If no valid moves, stay in place (avoiding out-of-bounds movements)
    return 'STAY'

def custom_agent(env):
    '''
    Based on the current state of the environment, this function returns an ACTION (which is a String).
    Currently, the agent just returns 'STAY' by default. So, it will NOT move at all.
    Modify the function to make the agent cool and efficient. 
    Try to implement a strategy that gives you the best performance measure (aka score). 
    The performance measure is the same for everyone and you CAN NOT change the performance measure below in the code.

    Valid actions: ['UP', 'DOWN', 'LEFT', 'RIGHT', 'SUCK', 'STAY']

    Some of the variables you can access (but are not limited to) are:

    env.agent_pos --> returns a tuple (x,y) which is the current position of the agent
    env.grid[x][y] --> 1 if there is dirt on x,y location, 0 otherwise.
    GRID_SIZE --> Set as 5. You can not change it but you can use it for calculations.
    '''
    # Grid is 0-indexed (0,1,2,3,4) and x and y are flipped (origin is top left)
    # It is better to move than to stay idle since 
    # Idle Penalty is -20 and Move penalty is -10
    x, y = env.agent_pos
    # dirty_cells = [
    #     (-1, 0, 'UP', False),
    #     (1, 0, 'DOWN', False),
    #     (0, -1, 'LEFT', False),
    #     (0, 1, 'RIGHT', False),
    #     (-1, -1, 'UP', False), # Top left
    #     (-1, 1, 'UP', False), # Top right
    #     (1, -1, 'DOWN', False), # Bottom left
    #     (1, 1, 'DOWN', False), # Bottom right
    #     (-2, 0, 'UP', False), # Two away up
    #     (2, 0, 'DOWN', False), # Two away down
    #     (0, -2, 'LEFT', False), # Two away left
    #     (0, 2, 'RIGHT', False), # Two away right
    #     (-2, -1, 'UP', False), # Two away top left
    #     (-2, 1, 'DOWN', False), # Two away top right
    #     (1, -2, 'LEFT', False), # Two away bottom left
    #     (1, 2, 'RIGHT', False), # Two away bottom right

    #     # These diagonals need double actions returned to SEE dirty tiles
    #     (-2, -2, 'UP', True), # Two away top left
    #     (-2, 2, 'UP', True), # Two away top right
    #     (2, -2, 'DOWN', True), # Two away bottom left
    #     (2, 2, 'DOWN', True), # Two away bottom right

    #     (-3, 0, 'UP', False), # Three away up
    #     (3, 0, 'DOWN', False), # Three away down
    #     (0, -3, 'LEFT', False), # Three away left
    #     (0, 3, 'RIGHT', False), # Three away right
    #     (-4, 0, 'UP', False), # Four away up
    #     (4, 0, 'DOWN', False), # Four away down
    #     (0, -4, 'LEFT', False), # Four away left
    #     (0, 4, 'RIGHT', False) # Four away right
    #     ]

    if env.grid[x][y] == 1:
        return 'SUCK'
    
    # # Check neighboring cells in all 8 directions (including diagonals and multiples) and avoid going out of bounds
    # for dx, dy, action, diag_parity in dirty_cells:
    #     nx, ny = x + dx, y + dy
    #     if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:  # Only consider valid positions
    #         if env.grid[nx][ny] == 1:
    #             if diag_parity:
    #                 return action * 2
    #             return action

    # Checks every cell on grid for dirtiness and adds it to list
    dirty_cells = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if env.grid[i][j] == 1:
                dirty_cells.append((i, j))
    
    # Makes vacuum NOT lazy by reversing check for dirty cells
    # to instead check for clean cells
    # Why? Because it is better to move than to stay idle (due to penalties)
    if not dirty_cells:
        for dx, dy, action in [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:  # Only consider valid positions
                if env.grid[nx][ny] == 0:
                    return action
    
    # Function calculates distance to the next dirty cell
    def distance_to_dirty(coordinates):
        i, j = coordinates
        return abs(i - x) + abs(j - y)
    
    # Sorts the dirty cells to find the closest dirty cell to curr posi
    dirty_cells.sort(key=distance_to_dirty)
    target_x, target_y = dirty_cells[0]
    
    # Moves vacuum closer to dirty cell from list (vertically, then horizontally)
    if x < target_x:
        return 'DOWN'
    elif x > target_x:
        return 'UP'
    elif y < target_y:
        return 'RIGHT'
    elif y > target_y:
        return 'LEFT'

    # Move away from edges to gain better LOS of environment
    # if x == 4:
    #     return 'UP'
    # elif x == 0:
    #     return 'DOWN'
    # if y == 4:
    #     return 'LEFT'
    # elif y == 0:
    #     return 'RIGHT'
    
    # This might never return
    return 'STAY'

# Simulation
def run_simulation(canvas, performance_function):
    env = Environment(canvas)
    for _ in range(TURNS):
        env.randomly_add_dirt()
        action = selected_agent(env)
        env.perform_action(action, performance_function)
        
    remaining_dirt = env.count_ones()
    print("Total Score:", env.score)
    print("Dirty tiles left: ", remaining_dirt)
    print("Penalty for left dirty tiles: ",PENALTY_PER_REMAINING_DIRTY_TILES_AT_THE_END*remaining_dirt)
    print("Final Score:", env.score + PENALTY_PER_REMAINING_DIRTY_TILES_AT_THE_END*remaining_dirt)

# Dictionary to store agent functions
agents = {
    "custom": custom_agent
}

# Performance variable multipliers
#DO NOT CHANGE
CLEANED_TILE = 200
UNNECESSARY_SUCK = -3*CLEANED_TILE
MOVE_PENALTY = -10
OUT_OF_BOUNDS_ATTEMPT = -500
CONSECUTIVE_CLEANS_BONUS = 400
IDLE_PENALTY = -20
EXPLORED_NEW_TILE = 10
PENALTY_PER_REMAINING_DIRTY_TILES_AT_THE_END= -200

selected_agent= agents["custom"]


# GUI Setup
root = tk.Tk()
root.title("Vacuum Cleaner Simulation")
canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.pack()
root.after(100, lambda: run_simulation(canvas, configurable_performance))
root.mainloop()
