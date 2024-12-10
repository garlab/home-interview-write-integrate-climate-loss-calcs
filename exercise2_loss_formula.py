import json
import math

# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def loss_estimate(construction_cost, floor_area, inflation_rate, hazard_probability, discount_rate, years):
    return (construction_cost * math.exp(inflation_rate * floor_area / 1000) * hazard_probability) / (1 + discount_rate) ** years


# Main execution function
def main():
    data = load_data('data.json')
    years = 10 # The number of years to consider
    discount_rate = 0.05 # Assuming an annual 5% discount rate

    total_estimated_loss = 0
    for building in data:
        building_id = building['buildingId']
        floor_area = building['floor_area']
        construction_cost_per_sm = building['construction_cost'] # Construction cost per square meter
        hazard_probability = building['hazard_probability']
        inflation_rate = building['inflation_rate']

        hazard_probability_over_years = 1 - (1 - hazard_probability) ** years
        # Assuming the formula takes in the full construction cost, not per s/m
        construction_cost = construction_cost_per_sm * floor_area
        inflation_rate_over_years = 1 - (1 + inflation_rate) ** years

        estimated_loss = loss_estimate(construction_cost, floor_area, inflation_rate_over_years, hazard_probability_over_years, discount_rate, years)
        print(f"Estimated Loss for ${building_id}: ${total_estimated_loss:.2f}")
        total_estimated_loss += estimated_loss

    print(f"Total Estimated Loss: ${total_estimated_loss:.2f}")

if __name__ == '__main__':
    main()
