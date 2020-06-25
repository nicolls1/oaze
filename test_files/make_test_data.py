START_FILE = '1000.csv'


def duplicate_csv():
    with open(START_FILE, 'r') as f:
        first_line = f.readline()
        base_file = f.read()

    with open('10_000.csv', 'w') as f:
        f.write(first_line)
        for i in range(10):
            f.write(base_file)

    with open('100_000.csv', 'w') as f:
        f.write(first_line)
        for i in range(100):
            f.write(base_file)

    with open('1_000_000.csv', 'w') as f:
        f.write(first_line)
        for i in range(1000):
            f.write(base_file)

    with open('10_000_000.csv', 'w') as f:
        f.write(first_line)
        for i in range(10000):
            f.write(base_file)

    with open('100_000_000.csv', 'w') as f:
        f.write(first_line)
        for i in range(100000):
            f.write(base_file)


if __name__ == "__main__":
    duplicate_csv()
