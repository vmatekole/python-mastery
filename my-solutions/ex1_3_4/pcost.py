from rich import print

# AA 100 32.20
# IBM 50 91.10
# CAT 150 83.44
# MSFT 200 51.23
# GE 95 40.37
# MSFT 50 65.10
# IBM 100 70.44


def portfolio_cost(input_file: str) -> float:
    with open(input_file, 'r') as f:
        table = []
        total_cost = 0.0
        for line in f:
            stock, amt, price = line.split()
            try:
                subtotal = int(amt) * float(price)
                table.append((stock, amt, price, subtotal))
                total_cost += subtotal
            except ValueError as e:
                print(f"Couldn't parse {e}")

    with open('./portfolio_with_amt.data', 'w') as fw:
        for entry in table:
            row: str = f"\n{entry[0]} {entry[1]} {entry[2]} {entry[3]:.2f}"
            print(row)
            fw.write(row)

    return total_cost


if __name__ == '__main__':
    print(f'\nTotal cost: {portfolio_cost('../Data/portfolio2.dat'):.2f}')
