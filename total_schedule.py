import pandas as pd
import pulp
import matplotlib.pyplot as plt

# load the unit cost per hour from Excel file
file_path = "C:/Users/85817/PycharmProjects/WEI/abnormal_guide_price.xlsx"
unit_costs_df = pd.read_excel(file_path, header=None)

# details about users and tasks (Ready Time, Deadline, Maximum scheduled energy per hour, Energy Demand)
tasks = {
    "User1": [(20, 23, 1, 1), (18, 23, 1, 2), (19, 21, 1, 1), (12, 20, 1, 3), (6, 12, 1, 3),
              (18, 20, 1, 2), (4, 10, 1, 2), (12, 18, 1, 2), (7, 14, 1, 3), (8, 14, 1, 3)],
    "User2": [(11, 22, 1, 2), (5, 11, 1, 2), (5, 23, 1, 1), (6, 20, 1, 3), (19, 19, 1, 1),
              (18, 21, 1, 2), (3, 23, 1, 3), (21, 23, 1, 2), (13, 17, 1, 1), (6, 11, 1, 2)],
    "User3": [(20, 23, 1, 2), (15, 21, 1, 3), (11, 15, 1, 2), (2, 17, 1, 3), (13, 16, 1, 2),
              (10, 18, 1, 2), (21, 23, 1, 2), (20, 23, 1, 1), (7, 21, 1, 2), (0, 7, 1, 3)],
    "User4": [(1, 8, 1, 1), (11, 20, 1, 2), (12, 19, 1, 3), (11, 16, 1, 3), (16, 18, 1, 1),
              (19, 23, 1, 3), (22, 23, 1, 1), (12, 19, 1, 2), (8, 20, 1, 2), (4, 12, 1, 2)],
    "User5": [(4, 20, 1, 1), (18, 22, 1, 3), (4, 16, 1, 1), (2, 16, 1, 3), (16, 23, 1, 2),
              (6, 18, 1, 2), (2, 6, 1, 1), (13, 17, 1, 3), (15, 23, 1, 1), (17, 23, 1, 1)]
}

# accumulate the total demand
total_hourly_demand = {hour: {user: 0 for user in tasks} for hour in range(24)}

for index, unit_costs in unit_costs_df.iterrows():
    # set the LP problem
    lp_prob = pulp.LpProblem(f"Minimize_Energy_Cost_Day_{index}", pulp.LpMinimize)
    energy_usage = {}

    # set the constraints
    for user, task_list in tasks.items():
        for task_idx, (ready, deadline, max_energy, demand) in enumerate(task_list):
            # max energy usage
            for hour in range(24):
                energy_usage[(user, task_idx, hour)] = pulp.LpVariable(f"E_{user}_{task_idx}_{hour}", 0, max_energy)

            # satisfy the constraints
            lp_prob += (
                pulp.lpSum(energy_usage[(user, task_idx, hour)] for hour in range(ready, deadline + 1)) == demand,
                f"Demand_{user}_{task_idx}"
            )

    # define objective function and minimize the total costs
    lp_prob += pulp.lpSum(
        energy_usage[(user, task_idx, hour)] * unit_costs[hour]
        for user in tasks
        for task_idx, (ready, deadline, _, _) in enumerate(tasks[user])
        for hour in range(ready, deadline + 1)
    ), "Total_Cost"

    # solve the LP problem
    lp_prob.solve()

    # find the optimal solution and collect energy demand per hour
    if pulp.LpStatus[lp_prob.status] == "Optimal":
        for user in tasks:
            for task_idx in range(10):
                for hour in range(24):
                    energy = pulp.value(energy_usage[(user, task_idx, hour)]) or 0
                    total_hourly_demand[hour][user] += energy

# prepare the data for drawing
hours = list(range(24))
user_hourly_totals_demand = {user: [total_hourly_demand[hour][user] for hour in hours] for user in tasks}

# draw the bar chart
plt.figure(figsize=(12, 6))
bottom = [0] * 24
for user, usage in user_hourly_totals_demand.items():
    plt.bar(hours, usage, bottom=bottom, label=user)
    bottom = [bottom[i] + usage[i] for i in range(24)]

plt.xlabel("Hour")
plt.ylabel("Total Energy Demand")
plt.title("Total Hourly Energy Demand by User Contribution Across All Days")
plt.xticks(hours)
plt.legend()
plt.show()
