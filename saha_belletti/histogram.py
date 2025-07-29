# ===================================================================
# Visualization Module - Statistical Analysis and Plotting
# Part of the research paper: "Analyzing, Fixing and Optimizing a 
# Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"
# ===================================================================

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Example data structure showing expected format (commented out):
# data = {
#     'ibm_osaka': {
#         'Minimum Depth': [0.5947265625, 0.5693359375, 0.5693359375, 0.5791015625, 0.5966796875],
#         'Minimum Width': [0.5126953125, 0.5322265625, 0.51953125, 0.4912109375, 0.4970703125],
#         'Balanced': [0.5595703125, 0.572265625, 0.5361328125, 0.6044921875, 0.572265625],
#         'Fixed Original': [0.5654296875, 0.5634765625, 0.5703125, 0.54296875, 0.5439453125]
#     },
#     'ibm_kyoto': {
#         'Minimum Depth': [0.5771484375, 0.5771484375, 0.5712890625, 0.59375, 0.5693359375],
#         'Minimum Width': [0.5673828125, 0.5634765625, 0.5302734375, 0.544921875, 0.5234375],
#         'Balanced': [0.5380859375, 0.55078125, 0.5498046875, 0.560546875, 0.5322265625],
#         'Fixed Original': [0.5693359375, 0.5693359375, 0.53515625, 0.546875, 0.546875]
#     },
#     'ibm_brisbane': {
#         'Minimum Depth': [0.8486328125, 0.8466796875, 0.873046875, 0.85546875, 0.841796875],
#         'Minimum Width': [0.7734375, 0.80078125, 0.7958984375, 0.8125, 0.8076171875],
#         'Balanced': [0.8330078125, 0.845703125, 0.830078125, 0.8349609375, 0.8046875],
#         'Fixed Original': [0.8330078125, 0.826171875, 0.8310546875, 0.82421875, 0.7998046875]
#     },
#     'ibm_sherbrooke': {
#         'Minimum Depth': [0.8173828125, 0.8232421875, 0.8193359375, 0.8291015625, 0.8115234375],
#         'Minimum Width': [0.783203125, 0.7822265625, 0.79296875, 0.7978515625, 0.8056640625],
#         'Balanced': [0.8056640625, 0.80859375, 0.8173828125, 0.7978515625, 0.802734375],
#         'Fixed Original': [0.796875, 0.8232421875, 0.8095703125, 0.798828125, 0.767578125]
#     }
# }


def plot_simulation_data(data, random_guess_chance):
    """
    Creates a comprehensive bar chart comparing oracle performance across noise models.
    
    This function generates publication-quality plots showing the performance of
    different oracle implementations under various IBM quantum device noise models.
    The plot includes confidence intervals and comparison with random guessing baseline.
    
    Args:
        data: Nested dictionary of experimental results
              Format: {noise_model: {system: [correct_chance_values]}}
        random_guess_chance: Theoretical probability of random correct guess (baseline)
    """
    # Convert probability values from 0-1 scale to 0-100 percentage scale
    for model in data:
        for configuration in data[model]:
            data[model][configuration] = [x * 100 for x in
                                          data[model][configuration]]

    # Set global font size for publication quality
    plt.rcParams.update({'font.size': 20})

    # Configuration for histogram plot
    labels = list(data.keys())  # Noise model names (IBM backends)
    model_names = list(data[labels[0]].keys())  # Oracle implementation names
    x = np.arange(len(labels))  # X-axis positions for noise model groups
    width = 0.2  # Width of individual bars
    
    # Color scheme for different oracle implementations
    colors = ['skyblue', 'lightgreen', 'salmon', 'violet']

    # Map internal system names to formal publication names
    formal_name = {"simple": "Minimum depth oracle",
                   "balanced": "Balanced oracle", 
                   "original": "Original paper oracle",
                   "minimal": "Minimum width oracle"}

    def mean_confidence_interval(data, confidence=0.95):
        """
        Calculates mean and 95% confidence interval for a dataset.
        
        Uses t-distribution for small sample sizes, which is more appropriate
        than normal distribution for typical experimental datasets.
        
        Args:
            data: List of numerical values
            confidence: Confidence level (default 95%)
            
        Returns:
            Tuple of (mean, lower_bound, upper_bound)
        """
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), stats.sem(a)  # Mean and standard error
        # Calculate margin of error using t-distribution
        h = se * stats.t.ppf((1 + confidence) / 2., n-1)
        return m, m-h, m+h

    # Create the main figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    max_value = 0  # Track maximum value for y-axis scaling
    
    # Plot bars for each oracle implementation
    for i, model_name in enumerate(model_names):
        means = []      # Mean performance for each noise model
        cis = []        # Confidence intervals for each noise model
        
        # Calculate statistics for each noise model
        for label in labels:
            mean, ci_low, ci_high = mean_confidence_interval(data[label][model_name])
            means.append(mean)
            # Store error bar data (distance from mean to bounds)
            cis.append((mean-ci_low, ci_high-mean))
            max_value = max(max_value, ci_high)  # Update maximum for y-axis
        
        # Plot bars with error bars for this oracle implementation
        cis = np.array(cis).T  # Transpose for matplotlib error bar format
        ax.bar(x + i*width, means, width, 
               label=formal_name[model_name], 
               yerr=cis, capsize=5, color=colors[i])
    
    # Customize x-axis labels and positions
    ax.set_xticks(x + width*(len(model_names)-1)/2)  # Center group labels
    ax.set_xticklabels(labels)
    
    # Add axis labels and legend
    ax.set_xlabel('Noise Models')
    ax.set_ylabel('Correct Result Probability (%)')
    ax.legend(title="Model")
    
    # Add horizontal line for random guessing baseline
    ax.axhline(y=random_guess_chance * 100, color='r', linestyle='--',
               label='Random Correct Guess Probability (' +
               str(random_guess_chance * 100) + '%)')
    ax.legend()  # Refresh legend to include baseline
    
    # Set y-axis ticks for clear readability
    ytick_spacing = 5  # 5% increments
    ax.set_yticks(np.arange(0, 100 + ytick_spacing, step=ytick_spacing))
    
    # Display and clean up
    plt.show()
    plt.close()
