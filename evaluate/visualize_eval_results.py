import pandas as pd
import matplotlib.pyplot as plt



# Load just the pivot table from the specific sheet
df = pd.read_excel("evaluation_results_excel.xlsx", sheet_name="Sheet2", skiprows=2)

# Optional: remove footer or 'Grand Total' row if present
df = df[df["Row Labels"] != "Grand Total"]

# Add grouping
def group_url(url):
    # If it's not a string (e.g. NaN), treat as "other"
    if not isinstance(url, str):
        return "other"
    if "json-ld" in url:
        return "json-ld"
    elif "microdata" in url:
        return "microdata"
    elif "inland-article" in url:
        return "inland-articles"
    elif "interactive" in url:
        return "interactive"
    elif "wiki" in url:
        return "wiki"
    else:
        return "other"

df["Group"] = df["Row Labels"].apply(group_url)

# Group by category and average
grouped = df.groupby("Group")[
    [
        "Average of score_response_completeness",
        "Average of score_response_relevance",
        "Average of score_valid_response",
        "Average of score_accuracy"
    ]
].mean()

ax = grouped.plot(
    kind='bar',
    figsize=(10, 6),
    colormap='viridis',
    legend=True
)

# Move legend to the right, outside the plot
ax.legend(
    title="Score Type",
    loc='lower rightove',
    bbox_to_anchor=(1.02, 1.02),   # x-offset (to the right), y-offset (top)
    borderaxespad=0            # pad between axes and legend
)

# Tweak layout so the legend is fully visible
plt.tight_layout(rect=[0, 0, 0.85, 1])  # leave 15% space on the right
plt.show()
