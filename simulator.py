import numpy as np
import random
import matplotlib.pyplot as plt

def _run_simulation(historical_throughput, num_simulations, max_weeks):
    """
    Runs a Monte Carlo simulation for a fixed number of weeks.
    (Private helper function)
    """
    all_sims_data = np.zeros((num_simulations, max_weeks))
    
    for i in range(num_simulations):
        cumulative_work = 0
        for j in range(max_weeks):
            random_throughput = random.choice(historical_throughput)
            cumulative_work += random_throughput
            all_sims_data[i, j] = cumulative_work
            
    return all_sims_data

def _create_burnup_chart(sim_data, remaining_work, max_weeks, p50, p85, p95):
    """
    Creates a probabilistic burn-up chart with a "cone of uncertainty."
    (Private helper function)
    """
    weeks = np.arange(1, max_weeks + 1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the percentile lines
    ax.plot(weeks, p50, color='blue', linestyle='--', label='50% Likelihood')
    ax.plot(weeks, p85, color='orange', linestyle='--', label='85% Likelihood')
    ax.plot(weeks, p95, color='red', linestyle='--', label='95% Likelihood')
    
    # Add the shaded "cone of uncertainty"
    ax.fill_between(weeks, p50, p85, color='blue', alpha=0.1, label='50-85% Range')
    ax.fill_between(weeks, p85, p95, color='orange', alpha=0.1, label='85-95% Range')
    
    # Plot the target line
    ax.axhline(remaining_work, color='black', linestyle='-', label=f'Target ({remaining_work} Tasks)')
    
    ax.set_title('Probabilistic "Burn-Up" Forecast')
    ax.set_xlabel('Weeks')
    ax.set_ylabel('Cumulative Work Done')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.7)
    
    # Set plot limits
    ax.set_ylim(bottom=0, top=max(remaining_work * 1.2, np.max(p95)))
    ax.set_xlim(left=0, right=max_weeks)
    
    return fig

def _find_forecast(percentile_path, remaining_work, max_weeks):
    """
    Finds the week number when a percentile path crosses the target.
    (Private helper function)
    """
    cross_indices = np.where(percentile_path >= remaining_work)[0]
    
    if len(cross_indices) > 0:
        first_cross_week = cross_indices[0] + 1
        return f"{first_cross_week} Weeks"
    else:
        return f"> {max_weeks} Weeks"

def generate_forecast(history, remaining_work, num_sims, max_weeks):
    """
    The main public function that runs the full simulation and analysis.
    
    This is the ONLY function your app.py will call.
    """
    
    # simulation run 
    simulation_data = _run_simulation(history, num_sims, max_weeks)
    p50_path, p85_path, p95_path = np.percentile(simulation_data, [50, 85, 95], axis=0)

    forecast_50 = _find_forecast(p50_path, remaining_work, max_weeks)
    forecast_85 = _find_forecast(p85_path, remaining_work, max_weeks)
    forecast_95 = _find_forecast(p95_path, remaining_work, max_weeks)
    
    # plot
    chart_fig = _create_burnup_chart(
        simulation_data, remaining_work, max_weeks,
        p50_path, p85_path, p95_path
    )
    
    metrics = {
        "50%": forecast_50,
        "85%": forecast_85,
        "95%": forecast_95
    }
    
    return metrics, chart_fig