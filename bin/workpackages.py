

def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, help='', metavar='file')
    args = parser.parse_args()

    perworkpackage = 3000

    workpackages = []

    current = []
    counter = 0

    with open(args.filename) as f:

        for line in f:

            line = line.strip()
            info = line.split(",")
            N = info[-1]
            N = int(N)

            counter += N
            current += [line]

            if counter > perworkpackage:

                workpackages.append(current)

                counter = 0
                current = []


    for workpackage in workpackages:
        print(workpackage)


    return

if __name__ == '__main__':
    main()
