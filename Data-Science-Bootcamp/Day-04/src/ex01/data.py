try:
    from termgraph import Data, BarChart, Args, Colors
except ModuleNotFoundError:
    print("Termgraph is not installed. Please activate your environment or run: pip install termgraph")
    exit(1)


def main():
    data = Data(
        data=[
            [73.32, 70.52],   # 2007: Pies, Bars
            [81.23, 93.00],   # 2008: Pies, Bars
            [181.43, 135.10],  # 2009: Pies, Bars
            [110.21, 95.00],   # 2010: Pies, Bars
            [93.97, 98.45]     # 2011: Pies, Bars
        ],
        labels=["2007", "2008", "2009", "2010", "2011"],
        categories=["Pies", "Bars"]
    )

    args = Args(
        colors=[Colors.Black, Colors.Green],
        width=50
    )

    chart = BarChart(data, args)
    chart.draw()


if __name__ == '__main__':
    main()
