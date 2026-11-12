"""
Summary chart comparing model performance across the project's
key milestones — for presentation and LinkedIn use.
"""

import matplotlib.pyplot as plt
import numpy as np

milestones = [
    "v1: Synthetic\n(no split)",
    "v2: Train/test\nsplit",
    "v3: Tuned\n(contamination=0.07)",
    "v4: Real Pass/Fail\n(placeholder limits)",
    "v5: Real Codex\nlimits (final)",
]
precision = [93.3, 100.0, 57.1, 80.0, 75.0]
recall = [93.3, 75.0, 100.0, 100.0, 100.0]

x = np.arange(len(milestones))
width = 0.35

fig, ax = plt.subplots(figsize=(11, 6))
bars1 = ax.bar(x - width/2, precision, width, label="Precision", color="steelblue")
bars2 = ax.bar(x + width/2, recall, width, label="Recall", color="darkorange")

ax.set_ylabel("Percent")
ax.set_title("Model Performance Across Project Milestones")
ax.set_xticks(x)
ax.set_xticklabels(milestones, fontsize=9)
ax.set_ylim(0, 110)
ax.legend()
ax.axhline(100, color="gray", linewidth=0.5, linestyle="--")

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.1f}", xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8)

plt.tight_layout()
plt.savefig("reports/results_summary.png", dpi=150)
print("Saved -> reports/results_summary.png")