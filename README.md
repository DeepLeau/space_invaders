![Space Invaders PyGames 2D](https://github.com/DeepLeau/space_invaders/blob/main/assets/space_invaders.png)

# Space Shooter ECS

Welcome to the **Space Shooter ECS** project! This is a 2D space shooter game built using the **Entity-Component-System (ECS)** architecture in Python with Pygame. The game showcases a modular design approach, inspired by ECS principles, ensuring better separation of concerns and easier scalability.

## Features

- **ECS Architecture**:
  - Entities composed of reusable components such as `Transform`, `Renderable`, `Health`, and `Shooter`.
  - Systems like `RenderSystem`, `MovementSystem`, `CollisionSystem`, and `WaveSystem` handle logic and interactions.

- **Gameplay Mechanics**:
  - Navigate the player's ship using keyboard controls (Z, Q, S, D, Space).
  - Shoot lasers to destroy incoming enemies.
  - Health bars for the player and enemies.
  - Progressive difficulty with increasing waves of enemies.

- **Modular Design**:
  - Components and systems are easily extendable for new features or mechanics.

## Future Aspirations

This 2D version of Space Shooter ECS is a precursor to a **3D Space Shooter project** developed in Unity using **Unity DOTS (Data-Oriented Technology Stack)**. While the 3D version is currently non-functional, it demonstrates the ambition to bring the ECS paradigm into a 3D environment.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame library

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/space-shooter-ecs.git
   ```

2. Navigate to the project directory:
   ```bash
   cd space-shooter-ecs
   ```

3. Install dependencies:
   ```bash
   pip install pygame
   ```

4. Ensure the `assets` folder is present with all required images.

### Run the Game

To start the game, run:
```bash
python main.py
```

## Controls

- **Z, Q, S, D**: Move the player's ship.
- **Space**: Shoot lasers.

**Enjoy the game!**
