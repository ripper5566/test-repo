# Offline Mail Reader Download Tool

A Python tool to download popular offline mail client applications for backup purposes.

## Overview

This tool automates the download of offline mail reader applications, making it easy to create backups of mail client installers. It currently supports Mozilla Thunderbird across multiple platforms (Windows, macOS, and Linux).

## Features

- 📥 Download multiple mail clients automatically
- 🔧 Configurable through JSON configuration file
- 💾 Support for multiple platforms (Windows, macOS, Linux)
- 📊 Progress reporting during downloads
- 🗂️ Organized output with metadata
- ⚙️ Command-line interface for automation

## Requirements

- Python 3.6 or higher
- Internet connection for downloading

## Installation

No installation required! Just ensure you have Python 3 installed:

```bash
python3 --version
```

## Usage

### List Available Mail Readers

```bash
python3 download_mail_readers.py --list
```

### Download All Mail Readers

```bash
python3 download_mail_readers.py --all
```

### Download Specific Platforms

```bash
python3 download_mail_readers.py --platforms thunderbird_windows thunderbird_mac
```

### Specify Output Directory

```bash
python3 download_mail_readers.py --all --output /path/to/backup
```

### Save Download Metadata

```bash
python3 download_mail_readers.py --all --save-metadata
```

## Configuration

The tool can be customized by editing the `config.json` file:

```json
{
  "mail_readers": {
    "thunderbird_windows": {
      "name": "Mozilla Thunderbird (Windows)",
      "url": "https://download.mozilla.org/?product=thunderbird-latest&os=win64&lang=en-US",
      "filename": "thunderbird_windows.exe",
      "enabled": true
    }
  }
}
```

### Adding More Mail Readers

To add additional mail readers, edit `config.json` and add new entries following the same structure:

```json
"your_reader_key": {
  "name": "Your Mail Reader Name",
  "url": "https://download-url.com/installer",
  "filename": "output_filename.ext",
  "enabled": true
}
```

## Supported Mail Readers

Currently supported mail readers:

- **Mozilla Thunderbird**
  - Windows (64-bit)
  - macOS
  - Linux (64-bit)

Additional mail readers can be easily added via the configuration file.

## Examples

### Backup All Mail Readers

```bash
# Download all available mail readers to default directory
python3 download_mail_readers.py --all

# Download to specific directory with metadata
python3 download_mail_readers.py --all --output ~/mail_backups --save-metadata
```

### Selective Download

```bash
# Download only Windows version
python3 download_mail_readers.py --platforms thunderbird_windows

# Download Windows and Mac versions
python3 download_mail_readers.py --platforms thunderbird_windows thunderbird_mac
```

## Output Structure

Downloaded files are organized in the output directory:

```
mail_readers_backup/
├── thunderbird_windows.exe
├── thunderbird_mac.dmg
├── thunderbird_linux.tar.bz2
└── download_metadata.json (if --save-metadata is used)
```

## Command-Line Options

```
--all                 Download all available mail readers
--platforms [NAMES]   Download specific platforms
--list                List all available mail readers
--output DIR          Output directory (default: mail_readers_backup)
--save-metadata       Save metadata about downloads
```

## Troubleshooting

### Download Fails

- Check your internet connection
- Verify the URLs in the configuration are still valid
- Some downloads may redirect; the tool handles this automatically

### Permission Errors

Make sure you have write permissions to the output directory:

```bash
mkdir -p mail_readers_backup
chmod 755 mail_readers_backup
```

## Contributing

To add support for more mail readers:

1. Add the mail reader information to `config.json`
2. Test the download URL
3. Verify the file downloads correctly

## License

This tool is provided as-is for backup and archival purposes. Please respect the licenses of the downloaded mail client applications.

## Notes

- Downloaded files should be scanned for viruses before use
- Keep backups in a secure location
- Periodically update backups to get the latest versions
- This tool downloads from official sources (Mozilla for Thunderbird)

## Security

- Only downloads from official sources
- Does not modify downloaded files
- Transparent download URLs displayed during operation
