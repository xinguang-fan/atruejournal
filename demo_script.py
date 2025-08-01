#!/usr/bin/env python3
"""
Demonstration script for Opinion Dynamics Simulation

This script demonstrates the key features and capabilities of the simulation framework.
Run this to see various models and their behaviors.
"""

import numpy as np
import matplotlib.pyplot as plt
from opinion_dynamics import OpinionDynamicsSimulator
import time
import os

def demo_single_simulations():
    """Demonstrate individual simulations with different models."""
    print("=" * 60)
    print("OPINION DYNAMICS SIMULATION DEMONSTRATION")
    print("=" * 60)
    
    models = ["voter", "bounded_confidence", "deffuant"]
    networks = ["small_world", "scale_free", "random"]
    
    print("\n1. Running individual simulations...")
    print("-" * 40)
    
    for model in models:
        for network in networks:
            print(f"\nTesting {model} model on {network} network...")
            
            # Create simulator
            sim = OpinionDynamicsSimulator(50, network)
            sim.confidence_threshold = 0.3  # More permissive for demonstration
            
            # Run simulation
            start_time = time.time()
            if model == "voter":
                history = sim.simulate(model, 500)
            else:
                history = sim.simulate(model, 500, distribution="bimodal")
            
            runtime = time.time() - start_time
            
            # Report results
            final_polarization = sim.get_polarization()
            consensus_time = sim.get_consensus_time()
            
            print(f"  Final polarization: {final_polarization:.4f}")
            print(f"  Consensus time: {consensus_time if consensus_time else 'Not reached'}")
            print(f"  Runtime: {runtime:.3f}s")

def demo_model_comparison():
    """Compare different models on the same network."""
    print("\n\n2. Model Comparison on Small-World Network")
    print("-" * 50)
    
    network_type = "small_world"
    network_size = 100
    steps = 1000
    
    results = {}
    
    for model in ["voter", "bounded_confidence", "deffuant"]:
        print(f"\nRunning {model} model...")
        
        # Create simulator
        sim = OpinionDynamicsSimulator(network_size, network_type)
        sim.confidence_threshold = 0.25
        sim.convergence_parameter = 0.3
        
        # Run simulation
        start_time = time.time()
        if model == "voter":
            history = sim.simulate(model, steps)
        else:
            history = sim.simulate(model, steps, distribution="bimodal")
        
        runtime = time.time() - start_time
        
        # Store results
        results[model] = {
            'polarization': sim.get_polarization(),
            'consensus_time': sim.get_consensus_time(),
            'runtime': runtime,
            'final_opinions': sim.opinions.copy(),
            'opinion_variance': np.var(sim.opinions)
        }
        
        print(f"  Final polarization: {results[model]['polarization']:.4f}")
        print(f"  Opinion variance: {results[model]['opinion_variance']:.4f}")
        print(f"  Runtime: {runtime:.3f}s")
    
    # Create comparison plot
    create_comparison_plot(results)
    return results

def demo_network_effects():
    """Demonstrate how network topology affects opinion dynamics."""
    print("\n\n3. Network Topology Effects (Bounded Confidence Model)")
    print("-" * 60)
    
    networks = ["random", "small_world", "scale_free", "complete", "ring"]
    network_size = 80
    steps = 800
    
    results = {}
    
    for network_type in networks:
        print(f"\nTesting {network_type} network...")
        
        # Create simulator
        sim = OpinionDynamicsSimulator(network_size, network_type)
        sim.confidence_threshold = 0.2
        
        # Run simulation
        start_time = time.time()
        history = sim.simulate("bounded_confidence", steps, distribution="bimodal")
        runtime = time.time() - start_time
        
        # Calculate network properties
        import networkx as nx
        avg_clustering = nx.average_clustering(sim.network)
        avg_path_length = nx.average_shortest_path_length(sim.network) if nx.is_connected(sim.network) else float('inf')
        
        # Store results
        results[network_type] = {
            'polarization': sim.get_polarization(),
            'consensus_time': sim.get_consensus_time(),
            'runtime': runtime,
            'clustering': avg_clustering,
            'path_length': avg_path_length,
            'final_opinions': sim.opinions.copy()
        }
        
        print(f"  Final polarization: {results[network_type]['polarization']:.4f}")
        print(f"  Average clustering: {avg_clustering:.3f}")
        print(f"  Average path length: {avg_path_length:.3f}")
        print(f"  Runtime: {runtime:.3f}s")
    
    return results

def demo_parameter_sensitivity():
    """Demonstrate how confidence threshold affects bounded confidence model."""
    print("\n\n4. Parameter Sensitivity Analysis")
    print("-" * 40)
    
    network_type = "small_world"
    network_size = 60
    steps = 600
    confidence_values = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    results = {}
    
    print("Testing different confidence thresholds...")
    
    for confidence in confidence_values:
        print(f"\nConfidence threshold: {confidence}")
        
        # Create simulator
        sim = OpinionDynamicsSimulator(network_size, network_type)
        sim.confidence_threshold = confidence
        
        # Run simulation
        history = sim.simulate("bounded_confidence", steps, distribution="bimodal")
        
        # Analyze results
        final_opinions = sim.opinions
        unique_clusters = count_opinion_clusters(final_opinions, threshold=0.05)
        
        results[confidence] = {
            'polarization': sim.get_polarization(),
            'clusters': unique_clusters,
            'consensus_time': sim.get_consensus_time(),
            'final_opinions': final_opinions.copy()
        }
        
        print(f"  Final polarization: {results[confidence]['polarization']:.4f}")
        print(f"  Opinion clusters: {unique_clusters}")
        print(f"  Consensus time: {results[confidence]['consensus_time'] if results[confidence]['consensus_time'] else 'Not reached'}")
    
    return results

def count_opinion_clusters(opinions, threshold=0.05):
    """Count the number of distinct opinion clusters."""
    sorted_opinions = np.sort(opinions)
    clusters = 1
    
    for i in range(1, len(sorted_opinions)):
        if sorted_opinions[i] - sorted_opinions[i-1] > threshold:
            clusters += 1
    
    return clusters

def create_comparison_plot(results):
    """Create a comparison plot for different models."""
    plt.figure(figsize=(15, 5))
    
    models = list(results.keys())
    
    # Plot 1: Final polarization
    plt.subplot(1, 3, 1)
    polarizations = [results[model]['polarization'] for model in models]
    plt.bar(models, polarizations, color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title('Final Polarization by Model')
    plt.ylabel('Polarization (Variance)')
    plt.xticks(rotation=45)
    
    # Plot 2: Opinion distributions
    plt.subplot(1, 3, 2)
    for i, model in enumerate(models):
        opinions = results[model]['final_opinions']
        plt.hist(opinions, bins=15, alpha=0.6, label=model, density=True)
    plt.title('Final Opinion Distributions')
    plt.xlabel('Opinion')
    plt.ylabel('Density')
    plt.legend()
    
    # Plot 3: Runtime comparison
    plt.subplot(1, 3, 3)
    runtimes = [results[model]['runtime'] for model in models]
    plt.bar(models, runtimes, color=['orange', 'purple', 'brown'])
    plt.title('Runtime Comparison')
    plt.ylabel('Runtime (seconds)')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('model_comparison_demo.png', dpi=300, bbox_inches='tight')
    
    # Only show if not in headless environment
    if os.environ.get('DISPLAY') is not None:
        plt.show()
    else:
        print("Model comparison plot saved to model_comparison_demo.png")

def print_summary():
    """Print summary of key findings."""
    print("\n\n" + "=" * 60)
    print("SUMMARY OF KEY FINDINGS")
    print("=" * 60)
    
    print("""
KEY INSIGHTS FROM OPINION DYNAMICS SIMULATION:

1. VOTER MODEL:
   - Always binary opinions (0 or 1)
   - Tends toward consensus through simple copying
   - Fast convergence in well-connected networks
   - Sensitive to network topology

2. BOUNDED CONFIDENCE MODEL (Hegselmann-Krause):
   - Continuous opinions in [0,1]
   - Agents only influenced by similar neighbors
   - Can lead to opinion fragmentation
   - Lower confidence threshold → more clusters

3. DEFFUANT MODEL:
   - Similar to bounded confidence but pairwise interactions
   - More gradual opinion changes
   - Can maintain multiple stable clusters
   - Convergence parameter affects speed

4. NETWORK EFFECTS:
   - Random networks: Efficient mixing, quick consensus
   - Small-world: Balance of clustering and shortcuts
   - Scale-free: Hubs drive opinion dynamics
   - Complete graphs: Fastest convergence
   - Ring networks: Slow, local diffusion

5. PARAMETER SENSITIVITY:
   - Confidence threshold crucial for fragmentation
   - High threshold → consensus
   - Low threshold → multiple clusters
   - Initial conditions matter for final state
""")

def main():
    """Run the complete demonstration."""
    print("Starting Opinion Dynamics Demonstration...")
    print("This will take a few minutes to complete.\n")
    
    # Run demonstrations
    demo_single_simulations()
    model_results = demo_model_comparison()
    network_results = demo_network_effects()
    param_results = demo_parameter_sensitivity()
    
    # Print summary
    print_summary()
    
    print("\nDemonstration completed!")
    print(f"Generated files:")
    print("- model_comparison_demo.png")
    
    # List any other generated files
    generated_files = [f for f in os.listdir('.') if f.endswith('.png')]
    for f in generated_files:
        if f != 'model_comparison_demo.png':
            print(f"- {f}")

if __name__ == "__main__":
    main()