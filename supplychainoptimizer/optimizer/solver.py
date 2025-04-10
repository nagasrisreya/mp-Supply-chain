import pulp

def optimize_supply_chain(suppliers, warehouses, products, transportation_costs):
    # Define the problem
    prob = pulp.LpProblem("SupplyChainOptimization", pulp.LpMinimize)

    # Decision variables
    x = pulp.LpVariable.dicts("Shipment", 
                              ((s, w, p) for s in suppliers for w in warehouses for p in products), 
                              lowBound=0, cat='Continuous')

    # Objective function: Minimize total cost
    prob += pulp.lpSum(
        transportation_costs[s][w] * x[(s, w, p)] 
        for s in suppliers for w in warehouses for p in products
    )

    # Constraints
    for s in suppliers:
        prob += pulp.lpSum(x[(s, w, p)] for w in warehouses for p in products) <= suppliers[s]['capacity']

    for w in warehouses:
        prob += pulp.lpSum(x[(s, w, p)] for s in suppliers for p in products) <= warehouses[w]['storage_capacity']

    for p in products:
        prob += pulp.lpSum(x[(s, w, p)] for s in suppliers for w in warehouses) >= products[p]['demand']

    # Solve the problem
    prob.solve()

    # Extract results
    results = {}
    for s in suppliers:
        for w in warehouses:
            for p in products:
                results[(s, w, p)] = x[(s, w, p)].varValue

    return results