#!/usr/bin/env python3
"""
Test suite for the mail reader downloader.
"""

import os
import sys
import json
import unittest
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from download_mail_readers import MailReaderDownloader


class TestMailReaderDownloader(unittest.TestCase):
    """Test cases for MailReaderDownloader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.downloader = MailReaderDownloader(output_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test that downloader initializes correctly."""
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertEqual(self.downloader.output_dir, Path(self.test_dir))
    
    def test_mail_readers_dict(self):
        """Test that mail readers dictionary is properly configured."""
        self.assertIsInstance(self.downloader.mail_readers, dict)
        self.assertGreater(len(self.downloader.mail_readers), 0)
        
        # Check that each mail reader has required keys
        for key, info in self.downloader.mail_readers.items():
            self.assertIn('name', info)
            self.assertIn('url', info)
            self.assertIn('filename', info)
            self.assertIsInstance(info['name'], str)
            self.assertIsInstance(info['url'], str)
            self.assertIsInstance(info['filename'], str)
    
    def test_thunderbird_entries(self):
        """Test that Thunderbird entries exist."""
        self.assertIn('thunderbird_windows', self.downloader.mail_readers)
        self.assertIn('thunderbird_mac', self.downloader.mail_readers)
        self.assertIn('thunderbird_linux', self.downloader.mail_readers)
    
    def test_save_metadata(self):
        """Test metadata saving functionality."""
        self.downloader.save_metadata()
        metadata_path = Path(self.test_dir) / "download_metadata.json"
        
        self.assertTrue(metadata_path.exists())
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        self.assertIn('mail_readers', metadata)
        self.assertIn('output_directory', metadata)
    
    def test_list_available(self):
        """Test that list_available runs without errors."""
        # This should not raise any exceptions
        try:
            self.downloader.list_available()
        except Exception as e:
            self.fail(f"list_available() raised {type(e).__name__}: {e}")
    
    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        new_test_dir = os.path.join(self.test_dir, "subdir", "nested")
        downloader = MailReaderDownloader(output_dir=new_test_dir)
        self.assertTrue(os.path.exists(new_test_dir))


class TestConfigFile(unittest.TestCase):
    """Test cases for configuration file."""
    
    def test_config_file_exists(self):
        """Test that config.json exists."""
        config_path = Path(__file__).parent / "config.json"
        self.assertTrue(config_path.exists(), "config.json should exist")
    
    def test_config_file_valid_json(self):
        """Test that config.json is valid JSON."""
        config_path = Path(__file__).parent / "config.json"
        
        with open(config_path, 'r') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError as e:
                self.fail(f"config.json is not valid JSON: {e}")
        
        self.assertIsInstance(config, dict)
        self.assertIn('mail_readers', config)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
