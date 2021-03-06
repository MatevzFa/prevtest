

### **Disclaimer: I do not guarantee that any of the tests programs or their XMLs located in [`test_programs`](/test_programs) are correct. Always check your results and please report any errors [here](https://github.com/MatevzFa/prevtest/issues).**

# PREVTEST

This repository contains test cases for the course on compilers for year 2018/19.
Snapshots for previous years can be found in respective branches of this repository:

- [2017/18](/MatevzFa/prevtest/tree/prev-2017/18)

## Installation

Clone this repository into a folder next to your `prev` folder.
```
...
├── prev
└── prevtest
```

To install Python dependencies, run `pip3 install -r requirements.txt`.

**Note:** If `pip3` is not installed, you can install it with `sudo apt install python3-pip`.


## Usage

```
usage: prevtest.py [-h] [--update-tests] [--verbose] [--no-build]
                   PHASE [FILTER]

positional arguments:
  PHASE           Target phase
  FILTER          Filter for test cases

optional arguments:
  -h, --help      show this help message and exit
  --update-tests  Update tests for some phase
  --verbose       Verbose output
  --no-build      Don't rebuild the compiler
```

## Contribution

If you want your tests added to this repository, make a pull request with your tests in an appropriate folder (see current structure).

Feel free to change (or completely rewrite :sweat_smile: ) the [program](prevtest.py).

### Contributors

- [Jakob Erzar](https://github.com/jakoberzar/)
- [Rok Kos](https://github.com/RokKos)
