import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import argparse
import time
from typing import List, Tuple, Dict, Optional
import seaborn as sns

class OpinionDynamicsSimulator:
    """
    A comprehensive simulator for opinion dynamics on networks.
    
    Supports multiple models:
    - Voter Model: Binary opinions with simple copying mechanism
    - Bounded Confidence Model (Hegselmann-Krause): Continuous opinions with confidence threshold
    - Deffuant Model: Pairwise interactions with confidence bound
    """
    
    def __init__(self, network_size: int = 100, network_type: str = "random"):
        self.network_size = network_size
        self.network_type = network_type
        self.network = None
        self.opinions = None
        self.history = []
        
        # Model parameters
        self.confidence_threshold = 0.2  # For bounded confidence models
        self.convergence_parameter = 0.5  # How much agents adjust opinions
        
        self._generate_network()
        
    def _generate_network(self):
        """Generate network topology based on specified type."""
        if self.network_type == "random":
            # Erdős-Rényi random graph
            self.network = nx.erdos_renyi_graph(self.network_size, 0.1)
        elif self.network_type == "small_world":
            # Watts-Strogatz small-world network
            self.network = nx.watts_strogatz_graph(self.network_size, 6, 0.3)
        elif self.network_type == "scale_free":
            # Barabási-Albert scale-free network
            self.network = nx.barabasi_albert_graph(self.network_size, 3)
        elif self.network_type == "complete":
            # Complete graph (everyone connected to everyone)
            self.network = nx.complete_graph(self.network_size)
        elif self.network_type == "ring":
            # Ring lattice
            self.network = nx.cycle_graph(self.network_size)
        else:
            raise ValueError(f"Unknown network type: {self.network_type}")
    
    def initialize_opinions(self, model_type: str, **kwargs):
        """Initialize opinions based on model type."""
        if model_type == "voter":
            # Binary opinions (0 or 1)
            self.opinions = np.random.choice([0, 1], size=self.network_size)
        elif model_type in ["bounded_confidence", "deffuant"]:
            # Continuous opinions in [0, 1]
            if "distribution" in kwargs and kwargs["distribution"] == "bimodal":
                # Create polarized initial distribution
                self.opinions = np.concatenate([
                    np.random.normal(0.2, 0.1, self.network_size // 2),
                    np.random.normal(0.8, 0.1, self.network_size // 2)
                ])
                self.opinions = np.clip(self.opinions, 0, 1)
            else:
                # Uniform distribution
                self.opinions = np.random.uniform(0, 1, self.network_size)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        self.history = [self.opinions.copy()]
    
    def voter_model_step(self):
        """One step of the voter model."""
        # Select random agent
        agent = np.random.randint(self.network_size)
        neighbors = list(self.network.neighbors(agent))
        
        if neighbors:
            # Copy opinion from random neighbor
            neighbor = np.random.choice(neighbors)
            self.opinions[agent] = self.opinions[neighbor]
    
    def bounded_confidence_step(self):
        """One step of the bounded confidence model (Hegselmann-Krause)."""
        new_opinions = self.opinions.copy()
        
        for agent in range(self.network_size):
            # Find neighbors within confidence threshold
            neighbors = list(self.network.neighbors(agent))
            if not neighbors:
                continue
                
            similar_neighbors = []
            for neighbor in neighbors:
                if abs(self.opinions[agent] - self.opinions[neighbor]) <= self.confidence_threshold:
                    similar_neighbors.append(neighbor)
            
            if similar_neighbors:
                # Update opinion as average of similar neighbors
                neighbor_opinions = [self.opinions[n] for n in similar_neighbors]
                neighbor_opinions.append(self.opinions[agent])  # Include own opinion
                new_opinions[agent] = np.mean(neighbor_opinions)
        
        self.opinions = new_opinions
    
    def deffuant_step(self):
        """One step of the Deffuant model."""
        # Select two random connected agents
        edges = list(self.network.edges())
        if not edges:
            return
            
        agent1, agent2 = edges[np.random.randint(len(edges))]
        
        # Check if opinions are within confidence threshold
        if abs(self.opinions[agent1] - self.opinions[agent2]) <= self.confidence_threshold:
            # Both agents move closer to each other
            opinion1 = self.opinions[agent1]
            opinion2 = self.opinions[agent2]
            
            self.opinions[agent1] += self.convergence_parameter * (opinion2 - opinion1)
            self.opinions[agent2] += self.convergence_parameter * (opinion1 - opinion2)
    
    def simulate(self, model_type: str, steps: int = 1000, **kwargs):
        """Run simulation for specified number of steps."""
        self.initialize_opinions(model_type, **kwargs)
        
        step_function = {
            "voter": self.voter_model_step,
            "bounded_confidence": self.bounded_confidence_step,
            "deffuant": self.deffuant_step
        }[model_type]
        
        for step in range(steps):
            step_function()
            
            # Record history every 10 steps to save memory
            if step % 10 == 0:
                self.history.append(self.opinions.copy())
        
        return np.array(self.history)
    
    def get_polarization(self):
        """Calculate polarization measure."""
        if len(np.unique(self.opinions)) == 1:
            return 0.0
        return np.var(self.opinions)
    
    def get_consensus_time(self, threshold: float = 0.01):
        """Find time to consensus (for continuous models)."""
        for i, opinions in enumerate(self.history):
            if np.var(opinions) < threshold:
                return i * 10  # Multiply by 10 since we record every 10 steps
        return None
    
    def plot_opinion_evolution(self, save_path: Optional[str] = None):
        """Plot evolution of opinions over time."""
        history = np.array(self.history)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot individual opinion trajectories
        for agent in range(min(20, self.network_size)):  # Plot max 20 agents
            ax1.plot(history[:, agent], alpha=0.7, linewidth=0.8)
        
        ax1.set_xlabel('Time Steps (×10)')
        ax1.set_ylabel('Opinion')
        ax1.set_title('Individual Opinion Trajectories')
        ax1.grid(True, alpha=0.3)
        
        # Plot opinion distribution evolution
        times_to_plot = np.linspace(0, len(history)-1, 5, dtype=int)
        colors = plt.cm.viridis(np.linspace(0, 1, len(times_to_plot)))
        
        for i, (time_idx, color) in enumerate(zip(times_to_plot, colors)):
            ax2.hist(history[time_idx], bins=20, alpha=0.6, 
                    label=f't={time_idx*10}', color=color, density=True)
        
        ax2.set_xlabel('Opinion')
        ax2.set_ylabel('Density')
        ax2.set_title('Opinion Distribution Evolution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        # Only show if not in headless environment
        import os
        if os.environ.get('DISPLAY') is not None:
            plt.show()
        else:
            print(f"Plot saved to {save_path if save_path else 'display'}")
    
    def plot_network_opinions(self, save_path: Optional[str] = None):
        """Plot network with nodes colored by opinion."""
        if len(self.opinions) > 200:
            print("Network too large to visualize effectively. Skipping network plot.")
            return
            
        plt.figure(figsize=(12, 8))
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(self.network, k=1, iterations=50)
        
        # Color nodes by opinion
        if len(np.unique(self.opinions)) == 2:
            # Binary opinions
            colors = ['red' if op == 0 else 'blue' for op in self.opinions]
            nx.draw(self.network, pos, 
                    node_color=colors,
                    node_size=50,
                    alpha=0.8,
                    edge_color='gray')
        else:
            # Continuous opinions
            colors = self.opinions
            nodes = nx.draw_networkx_nodes(self.network, pos, 
                                         node_color=colors,
                                         node_size=50,
                                         alpha=0.8,
                                         cmap=plt.cm.RdYlBu)
            nx.draw_networkx_edges(self.network, pos, edge_color='gray', alpha=0.3)
            plt.colorbar(nodes, label='Opinion')
        
        plt.title(f'Network Opinions ({self.network_type} network)')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        # Only show if not in headless environment
        import os
        if os.environ.get('DISPLAY') is not None:
            plt.show()
        else:
            print(f"Plot saved to {save_path if save_path else 'display'}")


class InteractiveSimulation:
    """Interactive simulation with real-time plotting."""
    
    def __init__(self, simulator: OpinionDynamicsSimulator):
        self.simulator = simulator
        self.fig, self.axes = plt.subplots(2, 2, figsize=(15, 10))
        self.line_plots = []
        self.current_step = 0
        
    def animate(self, frame, model_type: str, max_agents_plot: int = 20):
        """Animation function for real-time plotting."""
        # Clear axes
        for ax in self.axes.flat:
            ax.clear()
        
        # Run one simulation step
        if model_type == "voter":
            self.simulator.voter_model_step()
        elif model_type == "bounded_confidence":
            self.simulator.bounded_confidence_step()
        elif model_type == "deffuant":
            self.simulator.deffuant_step()
        
        self.current_step += 1
        self.simulator.history.append(self.simulator.opinions.copy())
        
        # Keep only recent history for performance
        if len(self.simulator.history) > 200:
            self.simulator.history = self.simulator.history[-200:]
        
        history = np.array(self.simulator.history)
        
        # Plot 1: Opinion trajectories
        ax1 = self.axes[0, 0]
        for agent in range(min(max_agents_plot, self.simulator.network_size)):
            ax1.plot(history[:, agent], alpha=0.7, linewidth=1)
        ax1.set_title('Opinion Trajectories')
        ax1.set_ylabel('Opinion')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Current opinion distribution
        ax2 = self.axes[0, 1]
        ax2.hist(self.simulator.opinions, bins=20, alpha=0.7, density=True)
        ax2.set_title('Current Opinion Distribution')
        ax2.set_xlabel('Opinion')
        ax2.set_ylabel('Density')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Polarization over time
        ax3 = self.axes[1, 0]
        polarization = [np.var(h) for h in self.simulator.history]
        ax3.plot(polarization)
        ax3.set_title('Polarization Over Time')
        ax3.set_xlabel('Time Steps')
        ax3.set_ylabel('Variance')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Network visualization (if small enough)
        ax4 = self.axes[1, 1]
        if self.simulator.network_size <= 50:
            pos = nx.spring_layout(self.simulator.network, k=1, iterations=20)
            if len(np.unique(self.simulator.opinions)) == 2:
                colors = ['red' if op == 0 else 'blue' for op in self.simulator.opinions]
            else:
                colors = self.simulator.opinions
            
            nx.draw(self.simulator.network, pos, ax=ax4,
                   node_color=colors,
                   node_size=100,
                   alpha=0.8,
                   edge_color='gray',
                   cmap=plt.cm.RdYlBu)
            ax4.set_title('Network State')
        else:
            ax4.text(0.5, 0.5, 'Network too large\nto visualize', 
                    ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Network State')
        
        plt.tight_layout()


def run_batch_simulation():
    """Run batch simulations comparing different models and networks."""
    print("Running Opinion Dynamics Simulation Suite...")
    print("=" * 50)
    
    # Parameters to test
    network_types = ["random", "small_world", "scale_free"]
    model_types = ["voter", "bounded_confidence", "deffuant"]
    network_size = 100
    steps = 1000
    
    results = {}
    
    for net_type in network_types:
        print(f"\nTesting {net_type} network...")
        results[net_type] = {}
        
        for model_type in model_types:
            print(f"  Running {model_type} model...")
            
            # Create simulator
            sim = OpinionDynamicsSimulator(network_size, net_type)
            
            # Run simulation
            start_time = time.time()
            if model_type == "voter":
                history = sim.simulate(model_type, steps)
            else:
                history = sim.simulate(model_type, steps, distribution="bimodal")
            
            runtime = time.time() - start_time
            
            # Calculate metrics
            final_polarization = sim.get_polarization()
            consensus_time = sim.get_consensus_time()
            
            results[net_type][model_type] = {
                'final_polarization': final_polarization,
                'consensus_time': consensus_time,
                'runtime': runtime,
                'final_opinions': sim.opinions.copy()
            }
            
            print(f"    Final polarization: {final_polarization:.4f}")
            print(f"    Consensus time: {consensus_time}")
            print(f"    Runtime: {runtime:.2f}s")
    
    # Create summary plots
    create_summary_plots(results, network_types, model_types)
    
    return results


def create_summary_plots(results: Dict, network_types: List[str], model_types: List[str]):
    """Create summary comparison plots."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Final polarization comparison
    ax1 = axes[0, 0]
    polarization_data = []
    labels = []
    
    for net_type in network_types:
        for model_type in model_types:
            if model_type in results[net_type]:
                polarization_data.append(results[net_type][model_type]['final_polarization'])
                labels.append(f"{net_type}\n{model_type}")
    
    ax1.bar(range(len(polarization_data)), polarization_data)
    ax1.set_xticks(range(len(labels)))
    ax1.set_xticklabels(labels, rotation=45, ha='right')
    ax1.set_ylabel('Final Polarization')
    ax1.set_title('Final Polarization by Network and Model')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Consensus time comparison
    ax2 = axes[0, 1]
    consensus_times = []
    consensus_labels = []
    
    for net_type in network_types:
        for model_type in model_types:
            if model_type in results[net_type]:
                ct = results[net_type][model_type]['consensus_time']
                if ct is not None:
                    consensus_times.append(ct)
                    consensus_labels.append(f"{net_type}\n{model_type}")
    
    if consensus_times:
        ax2.bar(range(len(consensus_times)), consensus_times)
        ax2.set_xticks(range(len(consensus_labels)))
        ax2.set_xticklabels(consensus_labels, rotation=45, ha='right')
        ax2.set_ylabel('Consensus Time')
        ax2.set_title('Time to Consensus')
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'No consensus reached\nin simulation time', 
                ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title('Time to Consensus')
    
    # Plot 3: Opinion distributions for different models
    ax3 = axes[1, 0]
    for i, model_type in enumerate(model_types):
        opinions = results['small_world'][model_type]['final_opinions']
        ax3.hist(opinions, bins=20, alpha=0.6, label=model_type, density=True)
    
    ax3.set_xlabel('Opinion')
    ax3.set_ylabel('Density')
    ax3.set_title('Final Opinion Distributions (Small-World Network)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Runtime comparison
    ax4 = axes[1, 1]
    runtime_data = []
    runtime_labels = []
    
    for net_type in network_types:
        for model_type in model_types:
            if model_type in results[net_type]:
                runtime_data.append(results[net_type][model_type]['runtime'])
                runtime_labels.append(f"{net_type}\n{model_type}")
    
    ax4.bar(range(len(runtime_data)), runtime_data)
    ax4.set_xticks(range(len(runtime_labels)))
    ax4.set_xticklabels(runtime_labels, rotation=45, ha='right')
    ax4.set_ylabel('Runtime (seconds)')
    ax4.set_title('Simulation Runtime')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('opinion_dynamics_summary.png', dpi=300, bbox_inches='tight')
    
    # Only show if not in headless environment
    import os
    if os.environ.get('DISPLAY') is not None:
        plt.show()
    else:
        print("Summary plot saved to opinion_dynamics_summary.png")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='Opinion Dynamics Simulation')
    parser.add_argument('--mode', choices=['interactive', 'batch', 'single'], 
                       default='single', help='Simulation mode')
    parser.add_argument('--model', choices=['voter', 'bounded_confidence', 'deffuant'], 
                       default='bounded_confidence', help='Opinion dynamics model')
    parser.add_argument('--network', choices=['random', 'small_world', 'scale_free', 'complete', 'ring'], 
                       default='small_world', help='Network topology')
    parser.add_argument('--size', type=int, default=100, help='Network size')
    parser.add_argument('--steps', type=int, default=1000, help='Simulation steps')
    parser.add_argument('--confidence', type=float, default=0.2, 
                       help='Confidence threshold for bounded confidence models')
    parser.add_argument('--convergence', type=float, default=0.5, 
                       help='Convergence parameter for Deffuant model')
    
    args = parser.parse_args()
    
    if args.mode == 'batch':
        results = run_batch_simulation()
        print("\nBatch simulation completed!")
        print("Summary plots saved as 'opinion_dynamics_summary.png'")
        
    elif args.mode == 'interactive':
        print("Starting interactive simulation...")
        print("Close the plot window to stop the simulation.")
        
        # Create simulator
        sim = OpinionDynamicsSimulator(args.size, args.network)
        sim.confidence_threshold = args.confidence
        sim.convergence_parameter = args.convergence
        sim.initialize_opinions(args.model, distribution="bimodal")
        
        # Create interactive simulation
        interactive = InteractiveSimulation(sim)
        
        # Start animation
        anim = FuncAnimation(interactive.fig, interactive.animate, 
                           fargs=(args.model,), interval=100, blit=False)
        plt.show()
        
    else:  # single mode
        print(f"Running single simulation:")
        print(f"  Model: {args.model}")
        print(f"  Network: {args.network} (size={args.size})")
        print(f"  Steps: {args.steps}")
        
        # Create and run simulation
        sim = OpinionDynamicsSimulator(args.size, args.network)
        sim.confidence_threshold = args.confidence
        sim.convergence_parameter = args.convergence
        
        start_time = time.time()
        if args.model == "voter":
            history = sim.simulate(args.model, args.steps)
        else:
            history = sim.simulate(args.model, args.steps, distribution="bimodal")
        
        runtime = time.time() - start_time
        
        # Print results
        print(f"\nSimulation completed in {runtime:.2f} seconds")
        print(f"Final polarization: {sim.get_polarization():.4f}")
        consensus_time = sim.get_consensus_time()
        if consensus_time:
            print(f"Consensus time: {consensus_time}")
        else:
            print("Consensus not reached")
        
        # Create plots
        sim.plot_opinion_evolution('opinion_evolution.png')
        sim.plot_network_opinions('network_opinions.png')
        
        print("Plots saved as 'opinion_evolution.png' and 'network_opinions.png'")


if __name__ == "__main__":
    main()