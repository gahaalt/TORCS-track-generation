import argparse
import json

from tools_evolution import Evolution


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True, help="Path to a JSON config file")
    parser.add_argument("-i", "--iterations", type=int, required=True, help="Number of evolution iterations")
    parser.add_argument("-s", "--save-path", help="Where to save the population")
    return parser.parse_args()


def main(args):
    with open(args.config) as f:
        config = json.load(f)
    evolution = Evolution(**config)
    evolution.initialize()
    evolution.print_fitness_statistics()
    try:
        for iter_ in range(args.iterations):
            evolution.step()
            evolution.print_fitness_statistics()
        evolution.generate_population_xmls()
        print("Final fitness:")
        evolution.print_specimen_fitness()
    finally:
        if args.save_path is not None:
            evolution.save_population(args.save_path)


if __name__ == '__main__':
    args = parse_args()
    main(args)