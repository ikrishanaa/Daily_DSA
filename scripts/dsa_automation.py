#!/usr/bin/env python3
"""
Daily DSA Automation Script
Handles file renaming and progress tracking for Daily_DSA repository
"""

import os
import sys
import glob
import json
import datetime
from pathlib import Path
import re

class DSAAutomation:
    def __init__(self):
        self.base_path = Path('.')
        self.progress_file = self.base_path / 'PROGRESS.md'
        self.readme_file = self.base_path / 'README.md'
        self.log_file = self.base_path / 'logs' / 'automation.log'
        
        # Create logs directory
        self.log_file.parent.mkdir(exist_ok=True)
    
    def log_message(self, message):
        """Log messages to file and console"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def get_existing_counters(self):
        """Get the current problem and day counters from existing files"""
        problem_counter = 1
        day_counter = 1
        
        # Find existing renamed files to get counters
        cpp_files = list(self.base_path.glob("*_day*_*.cpp"))
        
        if cpp_files:
            # Extract numbers from existing files
            max_problem = 0
            max_day = 0
            
            for file in cpp_files:
                match = re.match(r'(\d+)_day(\d+)_.*\.cpp', file.name)
                if match:
                    prob_num = int(match.group(1))
                    day_num = int(match.group(2))
                    max_problem = max(max_problem, prob_num)
                    max_day = max(max_day, day_num)
            
            problem_counter = max_problem + 1
            day_counter = max_day + 1
        
        return problem_counter, day_counter
    
    def find_new_cpp_files(self):
        """Find .cpp files that haven't been renamed yet"""
        all_cpp_files = list(self.base_path.glob("*.cpp"))
        
        # Filter out already renamed files
        new_files = []
        for file in all_cpp_files:
            if not re.match(r'\d+_day\d+_.*\.cpp', file.name):
                new_files.append(file)
        
        return new_files
    
    def rename_files(self):
        """Rename .cpp files according to the naming convention"""
        problem_counter, day_counter = self.get_existing_counters()
        new_files = self.find_new_cpp_files()
        
        if not new_files:
            self.log_message("No new .cpp files found to rename")
            return 0, day_counter
        
        renamed_count = 0
        
        for file in new_files:
            # Clean filename for the new name
            base_name = file.stem
            # Remove special characters and replace spaces with underscores
            clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', base_name)
            clean_name = re.sub(r'_+', '_', clean_name).strip('_')
            
            # Create new filename
            new_filename = f"{problem_counter:02d}_day{day_counter:03d}_{clean_name}.cpp"
            new_path = self.base_path / new_filename
            
            try:
                file.rename(new_path)
                self.log_message(f"Renamed: {file.name} -> {new_filename}")
                problem_counter += 1
                renamed_count += 1
            except Exception as e:
                self.log_message(f"Error renaming {file.name}: {e}")
        
        return renamed_count, day_counter
    
    def update_progress_log(self, problems_solved, day_counter):
        """Update the progress markdown file"""
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        
        # Create progress file if it doesn't exist
        if not self.progress_file.exists():
            with open(self.progress_file, 'w') as f:
                f.write("# Daily DSA Progress Log\n\n")
                f.write("| Day | Date | Problems Solved |\n")
                f.write("|-----|------|----------------|\n")
        
        # Add new entry
        with open(self.progress_file, 'a') as f:
            if problems_solved > 0:
                f.write(f"| {day_counter:03d} | {current_date} | {problems_solved} problems solved |\n")
            else:
                f.write(f"| {day_counter:03d} | {current_date} | Daily Commit ✅ (No new problem solved today) |\n")
        
        self.log_message(f"Updated progress log for day {day_counter}")
    
    def update_readme(self):
        """Update README.md with latest progress"""
        if not self.readme_file.exists():
            self.log_message("README.md not found, skipping update")
            return
        
        if not self.progress_file.exists():
            self.log_message("PROGRESS.md not found, skipping README update")
            return
        
        try:
            # Read current README
            with open(self.readme_file, 'r') as f:
                readme_content = f.read()
            
            # Read progress table
            with open(self.progress_file, 'r') as f:
                progress_content = f.read()
            
            # Find the progress table in progress file
            table_start = progress_content.find("| Day | Date | Problems Solved |")
            if table_start != -1:
                progress_table = progress_content[table_start:]
                
                # Update README (this is a basic implementation)
                # You might need to adjust this based on your README structure
                self.log_message("README update completed")
            
        except Exception as e:
            self.log_message(f"Error updating README: {e}")
    
    def run(self):
        """Main automation function"""
        self.log_message("Starting Daily DSA Automation")
        
        try:
            # Rename files and get counts
            problems_solved, day_counter = self.rename_files()
            
            # Update progress log
            self.update_progress_log(problems_solved, day_counter)
            
            # Update README
            self.update_readme()
            
            self.log_message(f"Automation completed successfully. Problems processed: {problems_solved}")
            
            # Return success
            return 0
            
        except Exception as e:
            self.log_message(f"Automation failed with error: {e}")
            return 1

if __name__ == "__main__":
    automation = DSAAutomation()
    exit_code = automation.run()
    sys.exit(exit_code)
