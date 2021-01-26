import tools
import flags
from os import path
import time
import os

NUM_RACES = 10

if __name__ == "__main__":
    with open(flags.RACE_CONFIG, 'r') as f:
        race_config = f.read()

    t = time.time()

    # Create artificial configs
    xml_config_paths = []
    for idx in range(NUM_RACES):
        new_race_config_path = path.join(os.getcwd(),
                                         'temp',
                                         f'temp_config{idx}.xml')
        with open(new_race_config_path, 'w') as f:
            f.write(race_config)
        xml_config_paths.append(new_race_config_path)

    # Run configured races
    results = tools.run_races_read_results(xml_config_paths)
    for i, r in enumerate(results):
        print(f'{i}: {r}')
    print("Time taken:", time.time() - t)
