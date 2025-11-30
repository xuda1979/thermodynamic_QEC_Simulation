
import json
import numpy as np
import matplotlib.pyplot as plt
from codes.surface_code import SurfaceCode
from decoders.pymatching_decoder import PyMatchingDecoder
from energy.model import EnergyModel
from simulation.backend import QECSimulation
import os

def run_parameter_sweep():
    distances = [3, 5, 7]
    physical_error_rates = np.logspace(-3, -1, 10) # 0.001 to 0.1
    shots = 10000

    results = {}

    energy_model = EnergyModel() # Use default costs

    print("Starting simulation sweep...")

    for d in distances:
        results[d] = {
            "p": [],
            "logical_error_rate": [],
            "energy": []
        }
        code = SurfaceCode(distance=d, rounds=d)
        sim = QECSimulation(code, energy_model)

        for p in physical_error_rates:
            print(f"Running d={d}, p={p:.4f}")
            res = sim.run(p, shots, PyMatchingDecoder)

            results[d]["p"].append(p)
            results[d]["logical_error_rate"].append(res.logical_error_rate)
            results[d]["energy"].append(res.average_energy_per_shot)

    # Save results to file
    with open("simulation_results.json", "w") as f:
        # Convert numpy types to native python for json serialization
        serializable_results = {}
        for d, data in results.items():
            serializable_results[d] = {
                "p": [float(x) for x in data["p"]],
                "logical_error_rate": [float(x) for x in data["logical_error_rate"]],
                "energy": [float(x) for x in data["energy"]]
            }
        json.dump(serializable_results, f, indent=4)

    print("Simulation complete. Results saved to simulation_results.json")
    return results

def plot_results(results=None):
    if results is None:
        with open("simulation_results.json", "r") as f:
            results = json.load(f)
            # Keys are strings in json, convert back to int
            results = {int(k): v for k, v in results.items()}

    # Plot 1: Threshold Plot (Logical vs Physical Error Rate)
    plt.figure(figsize=(10, 6))
    for d, data in results.items():
        plt.loglog(data["p"], data["logical_error_rate"], marker='o', label=f'd={d}')

    plt.xlabel('Physical Error Rate (p)')
    plt.ylabel('Logical Error Rate')
    plt.title('Surface Code Threshold Plot')
    plt.grid(True, which="both", ls="-")
    plt.legend()
    plt.savefig('paper/threshold_plot.png')
    plt.close()

    # Plot 2: Energy vs Physical Error Rate
    # Showing how energy scales with error rate for different distances due to decoding costs
    plt.figure(figsize=(10, 6))
    for d, data in results.items():
        plt.semilogx(data["p"], data["energy"], marker='s', label=f'd={d}')

    plt.xlabel('Physical Error Rate (p)')
    plt.ylabel('Average Energy per Shot (units)')
    plt.title('Energy Consumption vs Physical Error Rate')
    plt.grid(True, which="both", ls="-")
    plt.legend()
    plt.savefig('paper/energy_plot.png')
    plt.close()

    print("Plots saved to paper/ directory.")

if __name__ == "__main__":
    # Ensure paper directory exists
    os.makedirs("paper", exist_ok=True)

    if not os.path.exists("simulation_results.json"):
        data = run_parameter_sweep()
    else:
        print("Loading existing results...")
        with open("simulation_results.json", "r") as f:
            data = json.load(f)
            data = {int(k): v for k, v in data.items()}

    plot_results(data)
