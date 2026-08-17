import matplotlib.pyplot as plt
from forecast.forecasting import load_time_series


for metric in ["revenue", "orders", "customers", "aov"]:

    df = load_time_series(1,metric)

    plt.figure(figsize=(8,4))
    plt.plot(df["ds"], df["y"], marker="o")
    plt.title(metric)
    plt.grid(True)
    plt.show()

   