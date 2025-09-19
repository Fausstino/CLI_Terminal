# CLI_Terminal
## Simple CLI Terminal emulator fully written in Python

### How to use:
#### Step 1: Clone Repository:
```bash
git clone https://github.com/Fausstino/cli_terminal
```
#### Step 2: Basic usage
```bash
python3 terminal.py
```

#### Step 3: Usage with options:
```bash
# With logging enabled
python3 terminal.py --logfile terminal_log.csv

# With Virtual File System
python3 terminal.py --vfs ./test_vfs

# With startup script
python3 terminal.py --script startup_script.txt

# All features combined
python3 terminal.py --vfs ./test_vfs --logfile logs/terminal.csv --script init.txt
```

### Command line arguments

Argument: --logfile	| short: -l	| description: Path to CSV log file	| default: None	| usage: --logfile output.csv

Argument: --script	| short: -s	| description: Path to startup script	| default: None	| usage: --script commands.txt

Argument: --vfs	| short: None | description: Path to virtual file system source | default:	None | usage: --vfs ./data
