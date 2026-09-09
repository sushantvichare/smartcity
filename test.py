# Power BI Python visual script - single player radar
# Drag these fields into the "Values" well before running:
#   Attribute  (Pace, Shooting, Passing, Dribbling, Defending, Physical)
#   Score      (that player's value for each attribute)
#
# Power BI auto-creates a "dataset" DataFrame from those fields.
# If testing outside Power BI, uncomment the sample dataset below.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- Sample data for testing outside Power BI ---
dataset = pd.DataFrame({
    "Attribute": ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"],
    "Score":     [80, 86, 83, 90, 78, 85],
})

categories = dataset["Attribute"].tolist()
values = dataset["Score"].tolist()

num_vars = len(categories)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]
values += values[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

ax.plot(angles, values, linewidth=2, color="#2a78d6")
ax.fill(angles, values, alpha=0.15, color="#2a78d6")

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11)
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=8, color="gray")
ax.set_rlabel_position(0)

plt.title("Player Attribute Radar", fontsize=13, pad=20)
plt.tight_layout()
plt.show()