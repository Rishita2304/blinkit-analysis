"""
Blinkit Product Analysis
========================
Author : [Your Name]
Dataset: Simulated 5,000 orders · Delhi NCR · 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

BLINKIT_YELLOW = "#F8D000"
COLORS = ["#F8D000","#378ADD","#1D9E75","#D85A30","#7F77DD","#888780","#BA7517"]

df = pd.read_csv("data/orders.csv", parse_dates=["timestamp"])

# ── 1. KPIs ──────────────────────────────────────────────────────────────────
total_revenue   = df["revenue"].sum()
total_orders    = len(df)
avg_order_val   = df.groupby("order_id")["revenue"].sum().mean()
avg_delivery    = df["delivery_mins"].mean()
refund_rate     = df["refunded"].mean() * 100
avg_rating      = df["rating"].mean()

print("=" * 50)
print("  BLINKIT PRODUCT ANALYSIS — KEY METRICS")
print("=" * 50)
print(f"  Total Revenue     : ₹{total_revenue:,.0f}")
print(f"  Total Orders      : {total_orders:,}")
print(f"  Avg Order Value   : ₹{avg_order_val:.0f}")
print(f"  Avg Delivery Time : {avg_delivery:.1f} min")
print(f"  Refund Rate       : {refund_rate:.1f}%")
print(f"  Avg Rating        : {avg_rating:.2f} / 5")
print("=" * 50)

# ── 2. Monthly Revenue Trend ──────────────────────────────────────────────────
month_order = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]
monthly = (df.groupby("month")["revenue"]
             .sum()
             .reindex(month_order) / 1e5)          # in ₹ Lakh

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Blinkit Product Analysis Dashboard", fontsize=16, fontweight="bold", y=0.98)

ax = axes[0, 0]
ax.plot(monthly.index, monthly.values, color=BLINKIT_YELLOW,
        linewidth=2.5, marker="o", markersize=5)
ax.fill_between(monthly.index, monthly.values, alpha=0.15, color=BLINKIT_YELLOW)
ax.set_title("Monthly Revenue (₹ Lakh)", fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("₹ Lakh")
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.tick_params(axis="x", rotation=45)

# ── 3. Category Revenue Share ─────────────────────────────────────────────────
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)

ax = axes[0, 1]
wedges, texts, autotexts = ax.pie(
    cat_rev.values,
    labels=cat_rev.index,
    autopct="%1.0f%%",
    colors=COLORS,
    startangle=140,
    wedgeprops={"width": 0.55}
)
for t in autotexts:
    t.set_fontsize(9)
ax.set_title("Category Revenue Share", fontweight="bold")

# ── 4. Top 10 Products by Revenue ────────────────────────────────────────────
top_products = (df.groupby("product_name")["revenue"]
                  .sum()
                  .sort_values()
                  .tail(10))

ax = axes[1, 0]
bars = ax.barh(top_products.index, top_products.values / 1e3,
               color=BLINKIT_YELLOW, edgecolor="none")
ax.set_title("Top 10 Products by Revenue (₹K)", fontweight="bold")
ax.set_xlabel("Revenue (₹ Thousands)")
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.tick_params(axis="y", labelsize=9)

# ── 5. Delivery Time Distribution ────────────────────────────────────────────
ax = axes[1, 1]
ax.hist(df["delivery_mins"], bins=20, color=BLINKIT_YELLOW,
        edgecolor="white", linewidth=0.5)
ax.axvline(avg_delivery, color="#D85A30", linewidth=2,
           linestyle="--", label=f"Mean: {avg_delivery:.1f} min")
ax.set_title("Delivery Time Distribution", fontweight="bold")
ax.set_xlabel("Delivery Time (minutes)")
ax.set_ylabel("Number of Orders")
ax.legend(fontsize=9)
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("visuals/dashboard.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  Chart saved → visuals/dashboard.png")

# ── 6. Category Deep Dive ─────────────────────────────────────────────────────
cat_summary = df.groupby("category").agg(
    total_revenue   = ("revenue",       "sum"),
    total_orders    = ("order_id",      "count"),
    avg_order_value = ("revenue",       "mean"),
    avg_rating      = ("rating",        "mean"),
    refund_pct      = ("refunded",      lambda x: x.mean() * 100),
    avg_delivery    = ("delivery_mins", "mean"),
    gross_profit    = ("gross_profit",  "sum"),
).sort_values("total_revenue", ascending=False)

cat_summary["margin_pct"] = (cat_summary["gross_profit"] /
                              cat_summary["total_revenue"] * 100).round(1)
cat_summary["total_revenue"] = cat_summary["total_revenue"].apply(
    lambda x: f"₹{x/1e5:.1f}L")

print("\n  CATEGORY DEEP DIVE")
print(cat_summary[["total_revenue","total_orders","avg_rating",
                   "refund_pct","margin_pct"]].to_string())

# ── 7. Hourly Demand Pattern ──────────────────────────────────────────────────
hourly = df.groupby("hour")["order_id"].count()

fig, ax = plt.subplots(figsize=(12, 4))
ax.bar(hourly.index, hourly.values, color=BLINKIT_YELLOW,
       edgecolor="white", linewidth=0.5, width=0.8)
for peak_hour in [8, 13, 21]:
    ax.axvline(peak_hour, color="#D85A30", linewidth=1.5,
               linestyle="--", alpha=0.7)
ax.annotate("Morning\npeak", xy=(8, hourly[8]),
            xytext=(8.5, hourly[8]+5), fontsize=8, color="#D85A30")
ax.annotate("Lunch\npeak", xy=(13, hourly[13]),
            xytext=(13.5, hourly[13]+5), fontsize=8, color="#D85A30")
ax.annotate("Night\npeak", xy=(21, hourly[21]),
            xytext=(21.5, hourly[21]+5), fontsize=8, color="#D85A30")
ax.set_title("Hourly Order Demand Pattern — Blinkit 2024",
             fontweight="bold", fontsize=13)
ax.set_xlabel("Hour of Day"); ax.set_ylabel("Number of Orders")
ax.set_xticks(range(0, 24))
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("visuals/hourly_demand.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  Chart saved → visuals/hourly_demand.png")
print("\n  Analysis complete!")
