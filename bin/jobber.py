import itertools
import numpy as np


def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, help='', metavar='file')
    parser.add_argument('-b', '--torsion-bodies', type=int, help='', metavar='N', default=2)
    parser.add_argument('-r', '--torsion-resolutions', type=int, help='', metavar='N', default=2)
    args = parser.parse_args()

    with open("list_torsions", 'r') as f:

        for molidx, line in enumerate(f):

            line = line.strip().split()

            N_torsions = line[1]
            N_torsions = int(N_torsions)

            torsion_idx = list(range(N_torsions))

            resolutions = range(args.torsion_resolutions+1)
            resolutions = list(resolutions)

            total = 0

            for body in range(1, args.torsion_bodies+1):

                combinations = itertools.combinations(torsion_idx, body)

                for combination in combinations:

                    resiter = itertools.product(resolutions, repeat=body)

                    for reslist in resiter:

                        N = [max(2**(r-1), 1) for r in reslist]
                        N = np.prod(N)
                        print(molidx, ",", *combination, ",", *reslist, ",", N)

                        total += N

            print(total)
            quit()


    return

if __name__ == '__main__':
    main()


