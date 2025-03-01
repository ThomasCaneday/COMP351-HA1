# Vacuum Cleaner Simulation

## Overview
This program simulates an intelligent vacuum cleaner that moves around a 5x5 grid, detecting and cleaning dirt while optimizing its movements based on a performance function. The simulation is visualized using a Tkinter GUI, where the vacuum moves, cleans, and interacts with the environment in real-time.

## Features
- **Grid-based Environment**: A 5x5 grid where dirt can randomly appear.
- **Vacuum Agent**: The agent moves in the grid to clean dirt using a defined strategy.
- **Performance Evaluation**: The agent's actions are scored based on efficiency and penalties for unnecessary actions.
- **GUI Visualization**: Real-time movement and dirt-cleaning visualization using Tkinter.

## How It Works
1. The simulation initializes a 5x5 grid where the vacuum starts at a random position.
2. The environment generates dirt randomly at each turn.
3. The agent selects an action based on its strategy:
   - Move (`UP`, `DOWN`, `LEFT`, `RIGHT`)
   - Clean (`SUCK`)
   - Stay idle (`STAY`)
4. The performance function evaluates the agent’s actions with rewards and penalties.
5. The final score is displayed after 200 turns, along with the remaining dirty tiles penalty.

## Performance Scoring
| Action | Score |
|--------|-------|
| Cleaned Tile | +200 |
| Unnecessary Suck | -600 |
| Move Penalty | -10 |
| Out of Bounds Attempt | -500 |
| Consecutive Cleans Bonus | +400 |
| Idle Penalty | -20 |
| Explored New Tile | +10 |
| Remaining Dirty Tiles Penalty | -200 per tile |

## Agents
- **Lazy Agent**: Stays idle unless a nearby tile has dirt.
- **Custom Agent** (Default):
  - Moves proactively to clean.
  - Prioritizes the closest dirty tile.
  - Prefers moving over idling to minimize penalties.

## Installation & Usage
### Prerequisites
- Python 3.x
- Tkinter (included with most Python installations)

### Running the Simulation
1. Save the script as `ai_agent.py`.
2. Run the script using:
   ```sh
   python ai_agent.py
   ```
3. Observe the agent's behavior in the Tkinter window.
4. After 200 turns, the performance summary will be displayed in the console.

## Customization
- Modify `custom_agent()` to implement different movement strategies.
- Adjust `GRID_SIZE`, `DIRT_PROB`, and `TURNS` to test different conditions.
- Change penalties and rewards in the performance function.

## License
This project is for educational purposes and is free to use and modify.

## Author
Developed by Thomas Caneday.
