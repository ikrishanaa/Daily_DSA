# TODO: Fix Daily DSA Automation Scripts

## Issues Identified
- Inconsistency in metadata keys between `rename_and_track.py` and `update_readme.py`
- Bug in `rename_and_track.py` where `already_renamed(p.name)` should be `already_renamed(p)`
- `update_readme.py` uses "problem_counter" but `rename_and_track.py` sets "total_solved" and "file_counter"
- Metadata file has inconsistent keys and duplicate entries

## Tasks
- [x] Fix `update_readme.py` to use "total_solved" instead of "problem_counter" (already correct)
- [x] Fix `rename_and_track.py` to pass Path object to `already_renamed` function
- [x] Update `.meta.json` to use consistent keys matching the scripts
- [x] Test the workflow locally to ensure fixes work

## Dependent Files
- `tools/rename_and_track.py`
- `tools/update_readme.py`
- `.meta.json`

## Followup Steps
- Run the scripts to verify the fixes
- Check if README updates correctly
- Clean up duplicate entries in solved list if needed
