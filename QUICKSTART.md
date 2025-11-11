# Quick Start Guide

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed:
   ```bash
   python3 --version
   ```

## Basic Usage

### 1. List Available Mail Readers
```bash
python3 download_mail_readers.py --list
```

### 2. Download All Mail Readers
```bash
python3 download_mail_readers.py --all
```

This will download all available mail readers to the `mail_readers_backup/` directory.

### 3. Download Specific Platforms
```bash
# Windows only
python3 download_mail_readers.py --platforms thunderbird_windows

# Multiple platforms
python3 download_mail_readers.py --platforms thunderbird_windows thunderbird_mac
```

## Common Scenarios

### Scenario 1: Create a Complete Backup
```bash
# Download all mail readers with metadata
python3 download_mail_readers.py --all --save-metadata
```

### Scenario 2: Backup to External Drive
```bash
# Specify custom output directory
python3 download_mail_readers.py --all --output /mnt/external/mail_backups
```

### Scenario 3: Regular Updates
```bash
# Create a backup with timestamp
python3 download_mail_readers.py --all --output "mail_backup_$(date +%Y%m%d)"
```

## What Gets Downloaded

Currently supported mail readers:
- **Mozilla Thunderbird** (Windows, macOS, Linux)

## Where Files Are Saved

By default, files are saved to: `mail_readers_backup/`

Example structure:
```
mail_readers_backup/
├── thunderbird_windows.exe
├── thunderbird_mac.dmg
├── thunderbird_linux.tar.bz2
└── download_metadata.json (if --save-metadata used)
```

## Testing

Run the test suite to verify everything works:
```bash
python3 test_download_mail_readers.py
```

## Troubleshooting

**Problem:** Download fails  
**Solution:** Check your internet connection and verify URLs are valid

**Problem:** Permission denied  
**Solution:** Ensure you have write permissions to the output directory

**Problem:** File already exists  
**Solution:** Remove old files or use a different output directory

## Next Steps

- Read the full [README.md](README.md) for more details
- Customize [config.json](config.json) to add more mail readers
- Schedule regular backups using cron or Task Scheduler
