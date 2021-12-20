from ga import GA
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--problem', help='problem name', required=True)
parser.add_argument('--traveller', help='number of travellers', default=5, required=False)
parser.add_argument('--population', help='number of popilation', default=100, required=False)
parser.add_argument('--generations', help='number of generations', default=200, required=False)
parser.add_argument('--mutation', help='mutation rate', default=0.2, required=False)
args = parser.parse_args()
if __name__ == "__main__":
    ga = GA(args.problem, args.traveller, args.population, args.generations, args.mutation)
    runtime, optimal_length, optimal_path, minfun1val_per_round = ga.solve()
    print(f"Runtime: {runtime}s")
    print(f"Optimal length: {optimal_length}")
    print(f"Optimal path: {optimal_path}")