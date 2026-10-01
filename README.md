# Python Automation Scripts

> A collection of Windows-focused Python utilities for system management and network diagnostics — built with the Python standard library and native Windows command-line tools.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Platform-Windows-0078d6?logo=windows&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-None-5fa04e)
![CSV](https://img.shields.io/badge/Logging-CSV-217346)
![License](https://img.shields.io/badge/License-MIT-0f766e)

Python Automation Scripts is a set of standalone command-line tools for common administrative tasks on Windows machines. The collection includes a shutdown utility with an optional delay and a five-step network diagnostics tool that logs to CSV.

Each script is a single file with no external packages, so nothing needs to be installed beyond Python itself.

> ⚠️ **Warning:** `shutdown.py` shuts the computer down as soon as it runs, with no confirmation prompt. Save your work before running it.

## Contents

- [Script coverage](#script-coverage)
- [Features](#features)
- [Quick start](#quick-start)
- [Using the scripts](#using-the-scripts)
- [Output format](#output-format)
- [Project structure](#project-structure)
- [Technology](#technology)
- [Development commands](#development-commands)
- [Script execution](#script-execution)
- [Troubleshooting](#troubleshooting)
- [Complete command reference](#complete-command-reference)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Script coverage

The project contains **2 scripts**.

| Script           | Purpose                                              | Windows tools used                     | Standard library modules              |
| ---------------- | ---------------------------------------------------- | -------------------------------------- | ------------------------------------- |
| `shutdown.py`    | Shuts down the computer, with an optional delay      | `shutdown`                             | `subprocess`, `time`                  |
| `network_log.py` | Runs 5 network diagnostics and logs each step to CSV | `ping`, `ipconfig`, `netsh`, `tracert` | `subprocess`, `csv`, `os`, `datetime` |

### Shutdown utility

`shutdown.py` defines `shutdown_laptop(delay_seconds=0)`. When the delay is greater than zero, it prints a message and waits, then runs `shutdown /s /t 0`. It prints `✓ Shutdown initiated` on success or `✗ Failed to shutdown` with the error.

### Network diagnostics

`network_log.py` runs five checks in order and logs each result:

| Step | Check                   | Command                      | Success message                |
| :--: | ----------------------- | ---------------------------- | ------------------------------ |
|  1   | Internet connectivity   | `ping -n 1 google.com`       | `✓ Internet connection active` |
|  2   | Local IP configuration  | `ipconfig`                   | `✓ IP configuration retrieved` |
|  3   | Google DNS reachability | `ping -n 1 8.8.8.8`          | `✓ Google DNS reachable`       |
|  4   | WiFi interface state    | `netsh wlan show interfaces` | `✓ WiFi is connected`          |
|  5   | Trace route to Google   | `tracert -d -h 4 google.com` | `✓ Trace route completed`      |

After the five steps, an `Overall` row reports one of three results:

- `✓ All 5 network checks completed successfully!`
- `⚠ Partially successful: N/5 network checks done`
- `✗ Failed to perform any network checks (0/5)`

## Features

| Area        | Capabilities                                                                                        |
| ----------- | --------------------------------------------------------------------------------------------------- |
| System      | Shuts down the computer, with an optional delay in seconds                                          |
| Networking  | Runs ping, IP configuration, DNS, WiFi state, and trace route checks                                |
| Logging     | Writes each network step to a timestamped CSV file as it runs                                       |
| Resilience  | Catches `PermissionError`, `OSError`, and other exceptions, and prints warnings instead of crashing |
| Console     | Shows `✓`, `✗`, and `⚠` status indicators for every step                                            |
| Portability | Needs only Python and the Windows command-line tools, with no package installation                  |

## Quick start

### Requirements

- Python 3.10 or newer
- Windows 10 or 11, which provides `netsh`, `ipconfig`, `tracert`, and `shutdown`
- Administrative privileges are recommended if any command fails
- Visual Studio Code is recommended

### Clone the repository

```powershell
git clone https://github.com/saravanansaranraj27/python-automation-scripts.git
cd python-automation-scripts
```

### Install dependencies

No packages are required. The project uses only the Python standard library, and `requirement.txt` documents this.

### Verify Python

```powershell
python --version
```

### Verify the scripts

Check that both scripts compile. This does not run them:

```powershell
python -m py_compile shutdown.py
python -m py_compile network_log.py
```

## Using the scripts

Run the scripts from PowerShell or Command Prompt in the project folder.

### Network diagnostics

```powershell
python network_log.py
```

The script prints the log file name, runs the five steps, and prints each result and the overall summary. Results are written to a CSV file in the current folder.

### Shutdown

> ⚠️ Running this command shuts the computer down immediately. Save your work first.

```powershell
python shutdown.py
```

### Shutdown with a delay

The delay is set in the code, not on the command line. Edit the last line of `shutdown.py`:

```python
if __name__ == '__main__':
    shutdown_laptop(delay_seconds=30)
```

The script then prints `Shutting down in 30 seconds...` and waits before issuing the shutdown. Press `Ctrl + C` during the countdown to stop it. Once the shutdown command has been issued, the script cannot cancel it.

## Output format

Only `network_log.py` writes a CSV file. `shutdown.py` prints to the console only.

### File name

```text
network_log_{ddmmyyyy_HHMMSS}.csv
```

For example, `network_log_ddmmyyyy_HHMMSS.csv`. The name is set once when the script starts, so each run creates a new file in the current folder.

### Columns

| Column | Description                                      | Example                  |
| ------ | ------------------------------------------------ | ------------------------ |
| Step   | Step number from 1 to 5, or `Overall`            | `3`                      |
| Output | Status message with a `✓`, `✗`, or `⚠` indicator | `✓ Google DNS reachable` |

The header row is written when the file is created, and each step is written as soon as it finishes. The `Overall` message begins with a line break, so its cell spans two lines.

## Project structure

```text
python-automation-scripts/
├── shutdown.py            # Shutdown utility with optional delay
├── network_log.py         # Network diagnostics with CSV logging
├── requirement.txt        # Notes that only the standard library is used
├── .gitignore             # Excludes generated logs, Python cache, and editor files
└── README.md              # Project documentation
```

## Technology

- [Python](https://www.python.org/) standard library — `subprocess`, `csv`, `os`, `time`, and `datetime`
- Windows command-line tools — `ping`, `ipconfig`, `netsh`, `tracert`, and `shutdown`
- CSV — structured logging for the network diagnostics

## Development commands

### File exploration

```powershell
Get-ChildItem
Get-ChildItem -Force
Get-ChildItem -Filter *.py
tree /F /A
```

### Script validation

```powershell
python -m py_compile shutdown.py
python -m py_compile network_log.py
```

## Script execution

### Run the network diagnostics

```powershell
python network_log.py
```

### Run the shutdown utility

```powershell
python shutdown.py
```

### Run from an administrator terminal

Open PowerShell or Command Prompt with **Run as administrator**, go to the project folder, and run the script. The scripts do not request elevation themselves.

### Review a log

```powershell
Get-ChildItem network_log_*.csv
Import-Csv .\network_log_ddmmyyyy_HHMMSS.csv
```

Replace the file name with the log you want to view.

## Troubleshooting

### `python` is not recognized

Install Python 3.10 or newer and make sure it is on your `PATH`. The Python launcher may also work:

```powershell
py --version
py network_log.py
```

### The computer shut down when I ran `shutdown.py`

This is the intended behavior. The script runs `shutdown /s /t 0`, which shuts down immediately. To add a countdown, see [Shutdown with a delay](#shutdown-with-a-delay).

### The shutdown did not start

Run the script from an administrator terminal, and check that `shutdown` works in your terminal. The script suppresses the command's own output, so a failed command may not print an error.

### `⚠ Warning: Permission denied to write to ...`

The script cannot write the CSV file in the current folder. Run it from a folder you can write to, or from an administrator terminal.

### A network step fails

- Steps 1 and 3 fail when the machine has no internet access or blocks ICMP ping
- Step 5 prints `⚠ Trace route failed or timed out` when `tracert` does not finish successfully
- Endpoints are fixed in the code (`google.com` and `8.8.8.8`), so edit them for networks that block those addresses

### The WiFi step shows a result that looks wrong

See [Limitations](#limitations).

### Commands are not found on macOS or Linux

The scripts call Windows-only tools and will not work on other systems.

## Complete command reference

```powershell
git clone https://github.com/saravanansaranraj27/python-automation-scripts.git
python --version
python -m py_compile shutdown.py
python -m py_compile network_log.py
python network_log.py
python shutdown.py
Get-ChildItem network_log_*.csv
tree /F /A
```

## Limitations

- **Windows only:** The scripts rely on `ipconfig`, `netsh`, `tracert`, `ping -n`, and the `shutdown /s` flag.
- **Immediate shutdown:** `shutdown.py` has no confirmation prompt, and the delay can only be set by editing the code.
- **No admin escalation:** The scripts do not request UAC elevation. Run them as administrator if commands fail.
- **Hard-coded endpoints:** The network checks target `google.com` and `8.8.8.8`. Edit the code for air-gapped or restricted networks.
- **Limited detail in logs:** The CSV stores one status line per step. The output of `ping`, `ipconfig`, and `tracert` is not saved.
- **WiFi check accuracy:** Step 4 looks for the word `connected` in the `netsh` output, which also matches `disconnected`. The step also counts as a success even when the message reads `⚠ WiFi is not connected or not available`, so the overall count can be higher than the number of passing checks.
- **One file per run:** Each run creates a new timestamped CSV, so log files accumulate in the folder. Delete old files or add rotation for long-term use. Generated `network_log_*.csv` files are excluded by `.gitignore`.
- **Console only for shutdown:** `shutdown.py` writes no CSV log, and neither script shows notifications or progress bars.
- **No automated tests:** The project includes no test suite.

## Contributing

Improvements and new automation scripts are welcome.

Keep changes focused, and follow the existing conventions:

- Follow the existing CSV logging pattern in new scripts that produce logs
- Handle `PermissionError`, `OSError`, and generic exceptions
- Use `✓`, `✗`, and `⚠` status indicators consistently in console output

Verify scripts before opening a pull request:

```powershell
python -m py_compile shutdown.py
python -m py_compile network_log.py
```

## License

This project is licensed under the MIT License.
