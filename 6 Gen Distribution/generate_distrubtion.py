import numpy as np
import matplotlib.pyplot as plt

def generate_terrain_distribution(num_bins, total_points, loc1, scale1, ratio1, loc2=None, scale2=None, ratio2=None):
    if loc2 is None or scale2 is None or ratio2 is None:
        # Single mode distribution
        values = np.random.normal(loc=loc1, scale=scale1, size=total_points)
    else:
        # Multi mode distribution
        size1 = int(total_points * ratio1)
        size2 = total_points - size1
        values1 = np.random.normal(loc=loc1, scale=scale1, size=size1)
        values2 = np.random.normal(loc=loc2, scale=scale2, size=size2)
        values = np.concatenate((values1, values2))

    values = np.clip(values, 0, num_bins - 1)
    hist, _ = np.histogram(values, bins=num_bins, range=(0, num_bins))
    hist = normalize_distribution(hist, total_points)
    return hist

def normalize_distribution(hist, total_points):
    diff = total_points - sum(hist)
    if diff > 0:
        indices = np.random.choice(np.arange(len(hist)), diff)
        for idx in indices:
            hist[idx] += 1
    elif diff < 0:
        indices = np.random.choice(np.arange(len(hist)), -diff)
        for idx in indices:
            hist[idx] -= 1
    return hist

def plot_distribution(distribution, title):
    plt.bar(range(len(distribution)), distribution)
    plt.title(title)
    plt.xlabel('Elevation Range')
    plt.ylabel('Number of Data Points')
    plt.show()


# loc 1 is the mean of the first peak (can be 2)
# scale is standard deviation
# ratio is how much is to that mean (only for 2 locs)


# Island Distribution: Most values low, some high peaks
island_distribution = generate_terrain_distribution(
    num_bins=32, total_points=256, loc1=1, scale1=5, ratio1=0.7, loc2=25, scale2=10, ratio2=0.3)

# Mountain Distribution: Most values high
mountain_distribution = generate_terrain_distribution(
    num_bins=32, total_points=256, loc1=25, scale1=5, ratio1=1.0)

# Hill Distribution: Most values in the middle range
hill_distribution = generate_terrain_distribution(
    num_bins=32, total_points=256, loc1=16, scale1=5, ratio1=1.0)

# Mostly flat
plains_distribution = generate_terrain_distribution(
    num_bins=32, total_points=256, loc1=5, scale1=2, ratio1=1.0)

# Plateaus Distribution: Mostly high, flat values
plateaus_distribution = generate_terrain_distribution(
    num_bins=32, total_points=256, loc1=25, scale1=2, ratio1=1.0)

# Archipelago Distribution: Multiple low values, some high peaks (more intermediate ones than island)
archipelago_distribution = generate_terrain_distribution(
    num_bins=32, total_points=256, loc1=10, scale1=5, ratio1=0.6, loc2=25, scale2=10, ratio2=0.4)

# Plot the distributions
plot_distribution(island_distribution, "Island Distribution")
plot_distribution(mountain_distribution, "Mountain Distribution")
plot_distribution(hill_distribution, "Hill Distribution")
plot_distribution(plains_distribution, "Plains Distribution")
plot_distribution(plateaus_distribution, "Plateaus Distribution")
plot_distribution(archipelago_distribution, "Archipelago Distribution")

print("Island Distribution:", island_distribution)
print("Mountain Distribution:", mountain_distribution)
print("Hill Distribution:", hill_distribution)
print("Plains Distribution:", plains_distribution)
print("Plateaus Distribution:", plateaus_distribution)
print("Archipelago Distribution:", archipelago_distribution)