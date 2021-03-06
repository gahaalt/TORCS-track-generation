# Flags

1. Set up the right flags for your system and torcs installation
2. Run `python test_run.py --num_races=10`, which should print results of 10 (identical) races

Other flags for `test_run.py`:
* `--log=INFO|DEBUG`
* `--track_length=4` number of points for tracks
* `--track_scale=10` range for generating points

### Example `flags.py`:
```
TORCS_DIR = "/home/$USER/.torcs/"
TORCS_EXEC = "/usr/games/torcs"
RACE_CONFIG = "$PROJECT_DIR/templates/quickrace_template.xml"
RESULTS_DIR = "/home/$USER/.torcs/results/"
TRACKS_DIR = "/usr/local/share/games/torcs/tracks/evolution"
```

Ignore your changes to `flags.py`, e.g. using `git update-index --assume-unchanged flags.py`.

# TORCS modifications

The directory `torcs` contains modifications needed to collect some data, as well as fixes for bugs that prevent the original code from compiling.

## Installation

1. Download the "all-in-one" source package from [the TORCS website](http://torcs.sourceforge.net/index.php?name=Sections&op=viewarticle&artid=3)
2. Copy the contents of the `torcs` directory into the extracted source code
3. Follow the installation instructions

# Running the evolution

Before running the evolution:
1. Set up `flags.py`
2. Prepare a JSON config file containing parameters for the evolution. Example files are provided in the `configs` directory.

Then you can run the script `evolution.py`. You can call `python evolution.py --help` for the list of available options.

**Warning**: be cautious of your disk space when the evolution is running, as some torcs processes fail to exit properly, which may lead to gathering large log files.
