import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# 1) Load data
df = pd.read_excel("evaluation_results_final-2.xlsx", sheet_name="Sheet2", skiprows=2)
df = df[df["Row Labels"] != "Grand Total"]

print(df.columns.tolist())

# 2) Define your grouping function
def group_url(url):
    if "/inland-article" in url:
        return "Inland Article"
    if any(x in url for x in ["inland-1-jsonld","inland-2-jsonld",
                              "inland-3-jsonld","inland-4-jsonld",
                              "inland-5-jsonld","/inland-jsonld"]):
        return "Inland JSON-LD"
    if url.rstrip("/") == "http://localhost:3000/inland":
        return "Inland Base"

    if "/table-page-1-pagination/with-json-ld-and-microdata" in url:
        return "Table Paginated + JSON-LD & Microdata"
    if "/table-page-1-pagination/with-json-ld" in url:
        return "Table Paginated + JSON-LD"
    if "/table-page-1-pagination/with-microdata" in url:
        return "Table Paginated + Microdata"
    if "/table-page-1-pagination" in url:
        return "Table Paginated"

    if "/table-page-1/with-json-ld-and-microdata" in url:
        return "Table + JSON-LD & Microdata"
    if "/table-page-1/with-json-ld" in url:
        return "Table + JSON-LD"
    if "/table-page-1/with-microdata" in url:
        return "Table + Microdata"
    if url.startswith("http://localhost:3000/table-page-1"):
        return "Table Base"

    if "interactiveEasy" in url or "interactiveHard" in url:
        return "Interactive"
    if "jsheavy" in url:
        return "JS-Heavy"
    if "media" in url:
        return "Media"
    if "semantic" in url:
        return "Semantic Markup"
    if "wiki" in url:
        return "Wiki-Style"

    return "Other"

# 3) Apply grouping
df["Group"] = df["Row Labels"].apply(group_url)

# 4) Pick the metric columns
metric_cols = [
    "Average of score_response_completeness",
    "Average of score_response_relevance",
    "Average of score_valid_response",
    "Average of score_accuracy"
]

# after grouping…
grouped = df.groupby("Group")[metric_cols].mean().sort_index()

# Rename for display
grouped.columns = [
    "Avg Response Completeness",
    "Avg Response Relevance",
    "Avg Response Validity",
    "Avg Accuracy"
]

wrapped_labels = [
    "\n".join(textwrap.wrap(label, width=12))
    for label in grouped.columns
]
# Then plot
fig, ax = plt.subplots(figsize=(10, 6))

# your heatmap…
cax = ax.imshow(grouped.values, aspect='auto', cmap='YlGn', vmin=0, vmax=1)

# Add numeric labels inside the heatmap cells
for i in range(grouped.shape[0]):  # rows
    for j in range(grouped.shape[1]):  # columns
        value = grouped.values[i, j]
        text_color = "black" if value < 0.7 else "white"
        ax.text(
            j, i, f"{value:.2f}",
            ha='center', va='center',
            color=text_color, fontsize=7
        )

# Use wrapped labels, horizontal, smaller font
ax.set_xticks(range(len(wrapped_labels)))
ax.set_xticklabels(wrapped_labels, rotation=0, ha='center', fontsize=8)

# Y-labels (you can also shrink these if needed)
ax.set_yticks(range(len(grouped.index)))
ax.set_yticklabels(grouped.index, fontsize=9)

cbar = fig.colorbar(
    cax,
    ax=ax,
    orientation='vertical',
    fraction=0.046,
    pad=0.04
)

# Tweak margins to give x-labels room
fig.subplots_adjust(bottom=0.25)

plt.tight_layout()
fig.savefig("heatmap.pdf", bbox_inches="tight")
plt.show()

