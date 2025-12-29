# WAVE System - Installation Guide

**Version**: 1.0  
**Last Updated**: December 29, 2024  
**Estimated Setup Time**: 10-15 minutes

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (5 Minutes)](#quick-start-5-minutes)
3. [Detailed Installation](#detailed-installation)
4. [Verification](#verification)
5. [Running WAVE](#running-wave)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)
8. [Uninstallation](#uninstallation)

---

## 📌 Prerequisites

### System Requirements

#### Minimum:
- **OS**: Linux (Ubuntu 20.04+), macOS (10.14+), Windows 10+
- **Python**: 3.8 or higher
- **RAM**: 512 MB free
- **Storage**: 100 MB free
- **CPU**: Any modern processor (2+ cores recommended)

#### Recommended:
- **OS**: Ubuntu 22.04 LTS or macOS 13+
- **Python**: 3.10 or 3.11
- **RAM**: 2 GB free
- **Storage**: 1 GB free (for logs and data)
- **CPU**: 4+ cores for faster processing

### Software Prerequisites

#### Required:
- Python 3.8+ with pip
- Git (for cloning repository)

#### Optional:
- Virtual environment tool (venv, conda, or virtualenv)
- Code editor (VS Code, PyCharm, or Sublime)

---

## ⚡ Quick Start (5 Minutes)

For experienced users who just want to run the system quickly:

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/wave.git
cd wave

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run WAVE
python src/main.py

# 4. View results
ls -lh data/raw/wave_monitoring_data.csv
ls -lh data/logs/
open wave_dashboard.png  # macOS
xdg-open wave_dashboard.png  # Linux
```

**Done!** You should see output files in `data/` and `wave_dashboard.png`.

---

## 🔧 Detailed Installation

### Step 1: Check Python Version

First, verify you have Python 3.8 or higher installed:

```bash
python3 --version
```

**Expected Output**:
```
Python 3.8.10  (or higher)
```

**If Python is not installed or version is too old**:

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3.10 python3.10-pip
```

#### macOS:
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10
```

#### Windows:
Download from [python.org](https://www.python.org/downloads/) and run installer.
✅ Check "Add Python to PATH" during installation!

---

### Step 2: Install Git (if needed)

```bash
# Check if Git is installed
git --version
```

**If not installed**:

#### Ubuntu/Debian:
```bash
sudo apt install git
```

#### macOS:
```bash
brew install git
```

#### Windows:
Download from [git-scm.com](https://git-scm.com/download/win)

---

### Step 3: Clone Repository

```bash
# Option A: HTTPS (recommended for most users)
git clone https://github.com/YOUR_USERNAME/wave.git

# Option B: SSH (if you have SSH keys set up)
git clone git@github.com:YOUR_USERNAME/wave.git

# Navigate to project directory
cd wave
```

**Verify directory structure**:
```bash
ls -la
```

**Expected output**:
```
.
├── README.md
├── requirements.txt
├── prd.md
├── data/
├── src/
└── docs/
```

---

### Step 4: Create Virtual Environment (Recommended)

Virtual environments keep dependencies isolated and prevent conflicts.

#### Option A: Using venv (built-in)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**You'll see `(venv)` in your terminal prompt when activated.**

#### Option B: Using conda

```bash
# Create conda environment
conda create -n wave python=3.10

# Activate environment
conda activate wave
```

---

### Step 5: Install Dependencies

With your virtual environment activated:

```bash
# Install all required packages
pip install -r requirements.txt
```

**This will install**:
- numpy (1.24.3)
- pandas (2.0.3)
- scikit-learn (1.3.0)
- matplotlib (3.7.2)

**Installation time**: ~2-3 minutes depending on internet speed

**Expected output**:
```
Collecting numpy==1.24.3
  Downloading numpy-1.24.3-cp310-cp310-manylinux_2_17_x86_64.whl (17.3 MB)
Collecting pandas==2.0.3
  Downloading pandas-2.0.3-cp310-cp310-manylinux_2_17_x86_64.whl (12.3 MB)
...
Successfully installed numpy-1.24.3 pandas-2.0.3 scikit-learn-1.3.0 matplotlib-3.7.2
```

---

### Step 6: Verify Installation

Test that all dependencies are correctly installed:

```bash
python3 -c "import numpy, pandas, sklearn, matplotlib; print('✅ All dependencies installed successfully!')"
```

**Expected output**:
```
✅ All dependencies installed successfully!
```

**If you see errors**, see [Troubleshooting](#troubleshooting) section.

---

## ✅ Verification

### Quick Verification Test

Run a simple import test:

```bash
python3 << EOF
import sys
print(f"Python version: {sys.version}")

import numpy as np
print(f"NumPy version: {np.__version__}")

import pandas as pd
print(f"Pandas version: {pd.__version__}")

import sklearn
print(f"scikit-learn version: {sklearn.__version__}")

import matplotlib
print(f"Matplotlib version: {matplotlib.__version__}")

print("\n✅ All checks passed! WAVE is ready to run.")
EOF
```

**Expected output**:
```
Python version: 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]
NumPy version: 1.24.3
Pandas version: 2.0.3
scikit-learn version: 1.3.0
Matplotlib version: 3.7.2

✅ All checks passed! WAVE is ready to run.
```

---

## 🚀 Running WAVE

### Basic Run

```bash
# Make sure you're in the wave/ directory
cd wave

# Run the main system
python src/main.py
```

### What Happens During Execution

```
┌─────────────────────────────────────────┐
│  WAVE - Water Quality Monitoring        │
└─────────────────────────────────────────┘

[1/8] Initializing components...
  ✓ Simulator initialized
  ✓ Pipeline validator ready
  ✓ ML Engine loaded (3 models)
  ✓ Adaptive learner ready
  ✓ Explainer initialized
  ✓ Dashboard generator ready

[2/8] Generating sensor data...
  ✓ Created 1000 time-series readings
  ✓ Injected 2 contamination events

[3/8] Training ML models...
  ✓ Using 800 baseline readings
  ✓ Isolation Forest trained
  ✓ One-Class SVM trained
  ✓ Rolling Statistics initialized

[4/8] Monitoring phase...
  Processing readings 801-1000...
  🚨 ALERT #1 detected at reading 850
     Parameter: pH (8.9, normally 7.2)
     Cause: Alkaline industrial discharge
     Action: Investigate industrial zone
  
  🚨 ALERT #2 detected at reading 920
     Parameter: Turbidity (18.2 NTU, normally 1.5)
     Cause: Sewage discharge
     Action: IMMEDIATE investigation required

[5/8] Adaptive learning...
  ✓ Recorded 10 operator feedbacks
  ✓ Adjusted sensitivity: 0.05 → 0.03
  ✓ False positive improvement: 52%

[6/8] Generating dashboard...
  ✓ Created visualization: wave_dashboard.png

[7/8] Saving results...
  ✓ Raw data: data/raw/wave_monitoring_data.csv (5.4 KB)
  ✓ Alerts log: data/logs/alerts_log.json (8.2 KB)
  ✓ Learning metrics: data/logs/learning_metrics.json (3.1 KB)

[8/8] Summary:
  Total Readings: 1000
  Anomalies Detected: 2/2 (100%)
  False Positives: 8 (38% after learning)
  Detection Time: <1 second average
  Processing Time: 45.2 seconds

✅ WAVE execution completed successfully!

📁 Output Files:
  • data/raw/wave_monitoring_data.csv
  • data/logs/alerts_log.json
  • data/logs/learning_metrics.json
  • wave_dashboard.png
```

**Execution time**: 45-60 seconds

---

### Viewing Results

#### 1. View Raw Data (CSV)

```bash
# View first 10 lines
head -10 data/raw/wave_monitoring_data.csv

# Or open in spreadsheet application
libreoffice data/raw/wave_monitoring_data.csv  # Linux
open data/raw/wave_monitoring_data.csv  # macOS
```

#### 2. View Alerts (JSON)

```bash
# Pretty-print alerts
cat data/logs/alerts_log.json | python3 -m json.tool

# Or open in text editor
code data/logs/alerts_log.json  # VS Code
nano data/logs/alerts_log.json  # Terminal editor
```

#### 3. View Dashboard

```bash
# Open dashboard image
xdg-open wave_dashboard.png  # Linux
open wave_dashboard.png  # macOS
start wave_dashboard.png  # Windows
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: "ModuleNotFoundError: No module named 'numpy'"

**Cause**: Dependencies not installed

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

#### Issue 2: "pip: command not found"

**Cause**: pip not installed

**Solution**:

Ubuntu/Debian:
```bash
sudo apt install python3-pip
```

macOS:
```bash
python3 -m ensurepip --upgrade
```

Windows:
```bash
python -m ensurepip --upgrade
```

---

#### Issue 3: "Permission denied" when running main.py

**Cause**: File permissions issue

**Solution**:
```bash
# Add execute permission
chmod +x src/main.py

# Or run with python explicitly
python3 src/main.py
```

---

#### Issue 4: matplotlib "backend" error

**Cause**: Display backend not available

**Solution**:
```bash
# Set backend to non-interactive
export MPLBACKEND=Agg

# Then run WAVE
python src/main.py
```

Or add to `src/main.py`:
```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
```

---

#### Issue 5: "No space left on device"

**Cause**: Insufficient disk space

**Solution**:
```bash
# Check available space
df -h

# Clean up old data
rm -rf data/logs/*.json
rm -rf data/raw/*.csv

# Run WAVE again
python src/main.py
```

---

#### Issue 6: "scikit-learn version mismatch"

**Cause**: Incompatible scikit-learn version

**Solution**:
```bash
# Uninstall current version
pip uninstall scikit-learn

# Install specific version
pip install scikit-learn==1.3.0
```

---

#### Issue 7: Slow execution (>2 minutes)

**Cause**: System resource constraints

**Solutions**:

1. **Reduce dataset size** (edit `src/config.py`):
```python
NUM_READINGS = 500  # Instead of 1000
```

2. **Close other applications**:
```bash
# Check memory usage
free -h  # Linux
top  # macOS

# Close unnecessary applications
```

3. **Use PyPy** (Python alternative, 2-3× faster):
```bash
# Install PyPy
sudo apt install pypy3

# Run with PyPy
pypy3 src/main.py
```

---

### Getting Help

If you encounter issues not covered here:

1. **Check logs**: Look at error messages carefully
2. **GitHub Issues**: Search existing issues at `github.com/YOUR_USERNAME/wave/issues`
3. **Create new issue**: Provide:
   - Error message (full traceback)
   - Python version (`python3 --version`)
   - OS details (`uname -a` on Linux/macOS)
   - Steps to reproduce

---

## ⚙️ Advanced Configuration

### Customizing System Parameters

Edit `src/config.py` to customize behavior:

```python
# Dataset configuration
NUM_READINGS = 1000  # Total readings to generate
NUM_ANOMALIES = 2    # Contamination events to inject
TRAINING_SIZE = 800  # Readings for baseline training

# ML model parameters
CONTAMINATION_RATE = 0.05  # Initial sensitivity (5%)
ROLLING_WINDOW = 24        # Hours for rolling statistics
ISOLATION_FOREST_ESTIMATORS = 100  # Number of trees

# Alert thresholds
HIGH_SEVERITY_THRESHOLD = 3.0    # Standard deviations
CRITICAL_SEVERITY_THRESHOLD = 5.0

# Adaptive learning
FEEDBACK_BATCH_SIZE = 20  # Adjust after N feedbacks
MIN_CONTAMINATION_RATE = 0.01  # Lower sensitivity limit
MAX_CONTAMINATION_RATE = 0.10  # Upper sensitivity limit

# Dashboard
DASHBOARD_DPI = 100       # Image resolution
DASHBOARD_FIGSIZE = (15, 10)  # Size in inches
```

### Running with Custom Parameters

```bash
# Option 1: Edit config.py then run
nano src/config.py
python src/main.py

# Option 2: Override via environment variables
export NUM_READINGS=500
export NUM_ANOMALIES=3
python src/main.py
```

---

### Integration with Real Sensors

To use WAVE with actual hardware sensors:

1. **Replace simulator** in `src/main.py`:

```python
# Original (simulated):
from simulator import SensorSimulator
simulator = SensorSimulator()
data = simulator.generate_dataset(1000)

# Updated (real sensors):
from sensor_interface import RealSensorReader
sensor = RealSensorReader(port='/dev/ttyUSB0')
data = sensor.read_continuous()
```

2. **Create sensor interface** (`src/sensor_interface.py`):

```python
import serial
import pandas as pd

class RealSensorReader:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.serial = serial.Serial(port, baudrate)
    
    def read_single(self):
        # Read from serial port
        line = self.serial.readline().decode('utf-8')
        # Parse sensor data
        pH, turbidity, tds, temp = self.parse(line)
        return {
            'timestamp': pd.Timestamp.now(),
            'pH': pH,
            'turbidity_ntu': turbidity,
            'tds_mgl': tds,
            'temp_celsius': temp
        }
    
    def read_continuous(self, duration_hours=24):
        readings = []
        # Implement continuous reading loop
        return pd.DataFrame(readings)
```

3. **Install serial library**:
```bash
pip install pyserial
```

---

### Deployment Options

#### Option 1: Raspberry Pi Deployment

```bash
# 1. Install Raspberry Pi OS (64-bit recommended)

# 2. Install Python and dependencies
sudo apt update
sudo apt install python3-pip python3-venv
python3 -m venv wave-env
source wave-env/bin/activate
pip install -r requirements.txt

# 3. Set up autostart
sudo nano /etc/systemd/system/wave.service
```

**Service file content**:
```ini
[Unit]
Description=WAVE Water Quality Monitor
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/wave
ExecStart=/home/pi/wave/wave-env/bin/python /home/pi/wave/src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 4. Enable and start service
sudo systemctl enable wave.service
sudo systemctl start wave.service

# 5. Check status
sudo systemctl status wave.service
```

---

#### Option 2: Cloud Deployment (AWS/GCP)

**AWS EC2 Setup**:

```bash
# 1. Launch EC2 instance (t2.micro or larger)

# 2. Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Install dependencies
sudo apt update
sudo apt install python3-pip git
git clone https://github.com/YOUR_USERNAME/wave.git
cd wave
pip3 install -r requirements.txt

# 4. Run continuously with nohup
nohup python3 src/main.py > wave.log 2>&1 &

# 5. Monitor logs
tail -f wave.log
```

---

#### Option 3: Docker Deployment

**Create Dockerfile**:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY data/ ./data/

# Run WAVE
CMD ["python", "src/main.py"]
```

**Build and run**:
```bash
# Build image
docker build -t wave:latest .

# Run container
docker run -v $(pwd)/data:/app/data wave:latest

# Run with custom config
docker run -e NUM_READINGS=500 wave:latest
```

---

## 🗑️ Uninstallation

### Remove Virtual Environment

```bash
# Deactivate if active
deactivate

# Remove venv directory
rm -rf venv/

# Or for conda
conda env remove -n wave
```

### Remove Project Files

```bash
# Remove entire project
cd ..
rm -rf wave/

# Or keep code, remove data
cd wave
rm -rf data/logs/*
rm -rf data/raw/*
rm wave_dashboard.png
```

### Uninstall Dependencies (Optional)

```bash
# If using system Python (not recommended)
pip uninstall -r requirements.txt -y

# Virtual environment users can just delete the venv folder
```

---

## 📚 Additional Resources

### Documentation
- [README.md](README.md) - Project overview
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- [RESULTS.md](docs/RESULTS.md) - Performance metrics
- [CONCEPT_NOTE.md](docs/CONCEPT_NOTE.md) - Technical details

### External Resources
- [Python Documentation](https://docs.python.org/3/)
- [scikit-learn Docs](https://scikit-learn.org/stable/)
- [pandas Documentation](https://pandas.pydata.org/docs/)

### Support
- **GitHub Issues**: [YOUR_REPO/issues](https://github.com/YOUR_USERNAME/wave/issues)
- **Email**: your-email@example.com

---

## ✅ Installation Checklist

Before running WAVE, verify:

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Git installed (`git --version`)
- [ ] Repository cloned (`cd wave && ls`)
- [ ] Virtual environment created (`python3 -m venv venv`)
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Installation verified (`python3 -c "import sklearn, pandas"`)
- [ ] Can run WAVE (`python src/main.py`)
- [ ] Output files generated (`ls data/logs/`)

**All checked?** ✅ You're ready to use WAVE!

---

## 🎓 Next Steps

After successful installation:

1. **Run the system**: `python src/main.py`
2. **Examine outputs**: Check CSV, JSON, and PNG files
3. **Read documentation**: [ARCHITECTURE.md](docs/ARCHITECTURE.md), [RESULTS.md](docs/RESULTS.md)
4. **Customize parameters**: Edit `src/config.py`
5. **Integrate real sensors**: See [Advanced Configuration](#advanced-configuration)

