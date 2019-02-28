import itertools
import numpy as np
import json

import scipy.special as scs

import multiprocessing as mp


def group_cost(combinations):
    cost = 0
    for case in combinations:
        cost += np.prod([configuration_count(c) for c in case])

    return cost


def combinations_in_group(T, R):
    combinations = []
    for case in itertools.product(range(R+1), repeat=T):
        if R in case:
            combinations.append(case)
    return combinations


def configuration_count(resolution):
    if resolution == 0:
        return 1
    return 2**(resolution - 1)


def costfunc(r, t):
    rest = range(0, r+1)
    combinations = itertools.product(rest, repeat=t)
    combinations = list(combinations)
    combinations = [list(x) for x in combinations if r in x]
    return len(combinations)


def make_job(molidx, line, torsion_bodies, torsion_resolutions, perworkpackage=3000):

    # if molidx != 6091: return
    # if molidx != 0: return

    line = line.strip().split()

    N_torsions = line[1]
    N_torsions = int(N_torsions)

    torsion_idx = list(range(N_torsions))

    # guido cost func
    costmatrix = np.zeros((len(torsion_resolutions), len(torsion_bodies)), dtype=int)

    for i, R in enumerate(torsion_resolutions):
        for j, T in enumerate(torsion_bodies):

            cost = costfunc(R, T)

            cost = float(cost)
            cost = int(cost)

            costmatrix[i,j] = cost

    # resolutions = range(torsion_resolutions+1)
    # resolutions = list(resolutions)

    total = 0

    fjob = open("jobs/"+str(molidx) + ".wp", 'w')

    jobs = []

    for ib, body in enumerate(torsion_bodies):

        combinations = itertools.combinations(torsion_idx, body)

        for combination in combinations:

            combination = [str(x) for x in combination]
            combination = " ".join(combination)

            for ir, resolution in enumerate(torsion_resolutions):

                cost = costmatrix[ir, ib]

                job = [str(molidx), combination, str(resolution), str(cost)]
                job = ",".join(job)

                jobs.append(job)


    # wrap jobs in workpackages
    workpackages = []
    counter = 0
    current = []
    perworkpackage = 3000

    for line in jobs:

        line = line.strip()
        info = line.split(",")

        cost = info[-1]
        cost = int(cost)

        counter += cost
        # current += [",".join(info[:-1])]
        current += [line]

        if counter > perworkpackage:

            workpackages.append(";".join(current))

            counter = 0
            current = []


    workpackages.append(";".join(current))

    workpackages = "\n".join(workpackages)

    fjob.write(workpackages)

    fjob.close()

    return


def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--torsion-bodies', nargs="+", type=int, help='', metavar='N', default=[2])
    parser.add_argument('-r', '--torsion-resolutions', nargs="+", type=int, help='', metavar='N', default=[2])
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


