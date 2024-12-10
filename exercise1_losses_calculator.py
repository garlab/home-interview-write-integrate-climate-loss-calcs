import json
import math

# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Calculate total projected loss with additional complexity and errors
def calculate_projected_losses(building_data, years):
    total_loss = 0
    for building in building_data:
        floor_area = building['floor_area']
        construction_cost = building['construction_cost'] # Construction cost per square meter
        hazard_probability = building['hazard_probability']
        inflation_rate = building['inflation_rate']

        # Initial cost
        initial_cost = construction_cost * floor_area 

        # Calculate future cost
        future_cost = initial_cost * (1 + inflation_rate) ** years

        # Assuming hazard_probability is probability within a year
        hazard_probability_over_years = 1 - (1 - hazard_probability) ** years

        # Calculate risk-adjusted loss
        risk_adjusted_loss = future_cost * hazard_probability_over_years

        # Calculate present value of the risk-adjusted loss
        discount_rate = 0.05 # Assuming an annual 5% discount rate

        present_value_loss = risk_adjusted_loss / (1 + discount_rate) ** years

        # Calculate maintenance and total maintenance cost
        maintenance_cost = floor_area * 50 * years # assuming a flat rate per square meter per year
        total_maintenance_cost = maintenance_cost / (1 + discount_rate) ** years

        # Total loss calculation
        total_loss += present_value_loss + total_maintenance_cost

    return total_loss

# Main execution function
def main():
    data = load_data('data.json')
    years = 10 # The number of years to consider
    total_projected_loss = calculate_projected_losses(data, years)
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")

if __name__ == '__main__':
    main()