#!/usr/bin/env python3
"""
Offline Mail Reader Download Tool
Downloads popular offline mail client applications for backup purposes.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from urllib.request import urlretrieve, urlopen
from urllib.error import URLError, HTTPError


class MailReaderDownloader:
    """Download offline mail reader applications."""
    
    def __init__(self, output_dir="mail_readers_backup"):
        """Initialize the downloader with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Popular mail readers with direct download links
        self.mail_readers = {
            "thunderbird_windows": {
                "name": "Mozilla Thunderbird (Windows)",
                "url": "https://download.mozilla.org/?product=thunderbird-latest&os=win64&lang=en-US",
                "filename": "thunderbird_windows.exe"
            },
            "thunderbird_mac": {
                "name": "Mozilla Thunderbird (macOS)",
                "url": "https://download.mozilla.org/?product=thunderbird-latest&os=osx&lang=en-US",
                "filename": "thunderbird_mac.dmg"
            },
            "thunderbird_linux": {
                "name": "Mozilla Thunderbird (Linux)",
                "url": "https://download.mozilla.org/?product=thunderbird-latest&os=linux64&lang=en-US",
                "filename": "thunderbird_linux.tar.bz2"
            }
        }
    
    def download_file(self, url, filename, description):
        """Download a file from URL to the output directory."""
        output_path = self.output_dir / filename
        
        try:
            print(f"\nDownloading {description}...")
            print(f"URL: {url}")
            print(f"Destination: {output_path}")
            
            # Use urlretrieve with a reporthook for progress
            def report_progress(block_num, block_size, total_size):
                if total_size > 0:
                    percent = min(100, block_num * block_size * 100 / total_size)
                    sys.stdout.write(f"\rProgress: {percent:.1f}%")
                    sys.stdout.flush()
            
            urlretrieve(url, output_path, reporthook=report_progress)
            print(f"\n✓ Successfully downloaded {description}")
            return True
            
        except (URLError, HTTPError) as e:
            print(f"\n✗ Error downloading {description}: {e}")
            return False
        except Exception as e:
            print(f"\n✗ Unexpected error downloading {description}: {e}")
            return False
    
    def download_all(self, platforms=None):
        """Download all mail readers or specific platforms."""
        if platforms:
            readers_to_download = {k: v for k, v in self.mail_readers.items() if k in platforms}
        else:
            readers_to_download = self.mail_readers
        
        if not readers_to_download:
            print("No mail readers selected for download.")
            return
        
        print(f"Starting download to: {self.output_dir.absolute()}")
        print(f"Downloading {len(readers_to_download)} mail reader(s)...")
        
        success_count = 0
        fail_count = 0
        
        for key, info in readers_to_download.items():
            if self.download_file(info["url"], info["filename"], info["name"]):
                success_count += 1
            else:
                fail_count += 1
        
        print(f"\n{'='*60}")
        print(f"Download Summary:")
        print(f"  ✓ Successful: {success_count}")
        print(f"  ✗ Failed: {fail_count}")
        print(f"  Output directory: {self.output_dir.absolute()}")
        print(f"{'='*60}")
    
    def list_available(self):
        """List all available mail readers."""
        print("Available mail readers for download:")
        print(f"{'='*60}")
        for key, info in self.mail_readers.items():
            print(f"  {key:25} - {info['name']}")
        print(f"{'='*60}")
    
    def save_metadata(self):
        """Save metadata about downloaded files."""
        metadata = {
            "mail_readers": self.mail_readers,
            "output_directory": str(self.output_dir.absolute())
        }
        
        metadata_path = self.output_dir / "download_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Metadata saved to: {metadata_path}")


def main():
    """Main function to parse arguments and run the downloader."""
    parser = argparse.ArgumentParser(
        description="Download offline mail reader applications for backup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all mail readers
  python download_mail_readers.py --all
  
  # Download specific platforms
  python download_mail_readers.py --platforms thunderbird_windows thunderbird_mac
  
  # List available mail readers
  python download_mail_readers.py --list
  
  # Specify output directory
  python download_mail_readers.py --all --output /path/to/backup
        """
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Download all available mail readers'
    )
    
    parser.add_argument(
        '--platforms',
        nargs='+',
        help='Specific platforms to download (e.g., thunderbird_windows thunderbird_mac)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available mail readers'
    )
    
    parser.add_argument(
        '--output',
        default='mail_readers_backup',
        help='Output directory for downloaded files (default: mail_readers_backup)'
    )
    
    parser.add_argument(
        '--save-metadata',
        action='store_true',
        help='Save metadata about downloads'
    )
    
    args = parser.parse_args()
    
    downloader = MailReaderDownloader(output_dir=args.output)
    
    if args.list:
        downloader.list_available()
    elif args.all:
        downloader.download_all()
        if args.save_metadata:
            downloader.save_metadata()
    elif args.platforms:
        downloader.download_all(platforms=args.platforms)
        if args.save_metadata:
            downloader.save_metadata()
    else:
        parser.print_help()
        print("\nPlease specify --all, --platforms, or --list")
        sys.exit(1)


if __name__ == "__main__":
    main()
