# PREVTEST

## Installation

Clone this repository into a folder next to your `prev` folder.
```
...
├── prev
└── prevtest
```
**Warning: you might want to .gitignore it**

To install Python dependencies, run `pip install -r requirements.txt`.


## Usage

The script accepts two arguments. The first one specifies the phase to test, the second one can be used to only run matching tests.

```
./prevtest.py <PHASE> [<FILTER>]
```