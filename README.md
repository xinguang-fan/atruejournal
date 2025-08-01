# Opinion Dynamics Simulation

A comprehensive simulation framework for modeling opinion dynamics in social networks. This implementation includes multiple classical models and network topologies to explore how opinions evolve and spread through populations.

## Features

### Opinion Models
- **Voter Model**: Binary opinions with simple copying mechanism
- **Bounded Confidence Model (Hegselmann-Krause)**: Continuous opinions with confidence threshold
- **Deffuant Model**: Pairwise interactions with confidence bounds

### Network Topologies
- **Random Networks**: Erdős-Rényi graphs
- **Small-World Networks**: Watts-Strogatz model
- **Scale-Free Networks**: Barabási-Albert model
- **Complete Networks**: All-to-all connections
- **Ring Networks**: Circular lattice

### Visualization Features
- Real-time interactive simulations
- Opinion trajectory plots
- Network visualization with opinion-colored nodes
- Comparative analysis across models and networks
- Polarization and consensus metrics

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Single Simulation
Run a single simulation with default parameters:
```bash
python opinion_dynamics.py
```

Customize parameters:
```bash
python opinion_dynamics.py --model bounded_confidence --network small_world --size 150 --steps 2000 --confidence 0.3
```

#### Interactive Mode
Launch real-time visualization:
```bash
python opinion_dynamics.py --mode interactive --model deffuant --network scale_free
```

#### Batch Analysis
Compare all models across different networks:
```bash
python opinion_dynamics.py --mode batch
```

### Parameters

- `--mode`: Simulation mode (`single`, `interactive`, `batch`)
- `--model`: Opinion model (`voter`, `bounded_confidence`, `deffuant`)
- `--network`: Network topology (`random`, `small_world`, `scale_free`, `complete`, `ring`)
- `--size`: Number of agents (default: 100)
- `--steps`: Simulation steps (default: 1000)
- `--confidence`: Confidence threshold for bounded confidence models (default: 0.2)
- `--convergence`: Convergence parameter for Deffuant model (default: 0.5)

## Model Descriptions

### Voter Model
In the voter model, agents have binary opinions (0 or 1). At each time step:
1. A random agent is selected
2. The agent adopts the opinion of a randomly chosen neighbor
3. This leads to clustering and eventual consensus

### Bounded Confidence Model (Hegselmann-Krause)
Agents have continuous opinions in [0,1]. At each time step:
1. All agents simultaneously update their opinions
2. Each agent averages opinions of neighbors within their confidence threshold
3. Agents ignore neighbors with very different opinions
4. Can lead to opinion clusters or fragmentation

### Deffuant Model
Similar to bounded confidence but with pairwise interactions:
1. Two connected agents are randomly selected
2. If their opinions are within the confidence threshold, both move closer
3. The convergence parameter controls how much they adjust
4. More gradual opinion changes than Hegselmann-Krause

## Network Effects

Different network topologies produce different dynamics:

- **Random Networks**: Efficient mixing, quick consensus
- **Small-World Networks**: Balance of clustering and long-range connections
- **Scale-Free Networks**: Hubs can drive opinion spread
- **Complete Networks**: Maximum interaction, fastest consensus
- **Ring Networks**: Local interactions, slow diffusion

## Output

The simulation generates several types of output:

### Single Mode
- `opinion_evolution.png`: Shows opinion trajectories and distribution evolution
- `network_opinions.png`: Network visualization with opinion-colored nodes
- Console output with metrics (polarization, consensus time, etc.)

### Interactive Mode
- Real-time plots showing:
  - Individual opinion trajectories
  - Current opinion distribution
  - Polarization over time
  - Network state (for small networks)

### Batch Mode
- `opinion_dynamics_summary.png`: Comparative analysis across all models and networks
- Console output with detailed metrics for each combination

## Example Results

### Typical Behavior Patterns

1. **Voter Model**: Always reaches consensus, time depends on network structure
2. **Bounded Confidence**: Can fragment into opinion clusters if confidence threshold is low
3. **Deffuant Model**: Similar to bounded confidence but with smoother transitions

### Key Metrics

- **Polarization**: Measured as variance of opinion distribution
- **Consensus Time**: Steps needed to reach agreement (variance < 0.01)
- **Final Clusters**: Number of distinct opinion groups

## Scientific Background

This simulation implements models from computational social science and statistical physics:

- **Voter Model**: Originally from interacting particle systems, models social conformity
- **Bounded Confidence**: Models selective exposure - people only listen to similar others
- **Network Effects**: Different topologies represent various social structures

## Extensions

The framework can be easily extended with:
- New opinion update rules
- Additional network topologies
- Multi-dimensional opinions
- Heterogeneous confidence thresholds
- External influence (media, leaders)

## References

- Castellano, C., Fortunato, S., & Loreto, V. (2009). Statistical physics of social dynamics. Reviews of Modern Physics, 81(2), 591.
- Hegselmann, R., & Krause, U. (2002). Opinion dynamics and bounded confidence models, analysis, and simulation. Journal of Artificial Societies and Social Simulation, 5(3).
- Deffuant, G., et al. (2000). Mixing beliefs among interacting agents. Advances in Complex Systems, 3(01n04), 87-98.