import itertools
import numpy as np
import json

import multiprocessing as mp


def make_job(molidx, line, torsion_bodies, torsion_resolutions, perworkpackage=3000):

    print(molidx)

    line = line.strip().split()

    N_torsions = line[1]
    N_torsions = int(N_torsions)

    torsion_idx = list(range(N_torsions))

    resolutions = range(torsion_resolutions+1)
    resolutions = list(resolutions)

    total = 0

    fjob = open("jobs/"+str(molidx) + ".wp", 'w')

    jobs = []

    for body in range(1, torsion_bodies+1):

        combinations = itertools.combinations(torsion_idx, body)

        for combination in combinations:

            resiter = itertools.product(resolutions, repeat=body)

            for reslist in resiter:

                N = [max(2**(r-1), 1) for r in reslist]
                N = np.prod(N)
                jobstr = " ".join([str(x) for x in [molidx, ",", *combination, ",", *reslist, ",", N]])

                jobs.append(jobstr + "\n")
                total += N


    # wrap jobs in workpackages
    workpackages = []
    counter = 0
    current = []
    perworkpackage = 3000

    for line in jobs:

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


    workpackages = workpackages.__repr__()

    fjob.write(workpackages)

    fjob.close()

    return


def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--torsion-bodies', type=int, help='', metavar='N', default=2)
    parser.add_argument('-r', '--torsion-resolutions', type=int, help='', metavar='N', default=2)
    parser.add_argument('-j', '--workers', type=int, help='', metavar='N', default=1)
    args = parser.parse_args()


    names = []
    lines = []

    with open("list_torsions", 'r') as f:

        for molidx, line in enumerate(f):

            names.append(molidx)
            lines.append(line)


    if args.workers == 1:

        for molidx, line in zip(names, lines):
            make_job(molidx, line, args.torsion_bodies, args.torsion_resolutions)


    else:

        worker = lambda x, y : make_job(x, y, args.torsion_bodies, args.torsion_resolutions)

        workers = args.workers

        processes = [mp.Process(target=worker, args=(names[i], lines[i])) for i in range(workers)]
        for p in processes: p.start() # Fork
        for p in processes: p.join()  # Join


    return

if __name__ == '__main__':
    main()


