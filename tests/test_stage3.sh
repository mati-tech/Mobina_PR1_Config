#!/bin/bash
echo "--- Testing valid VFS ---"
echo "ls /" | python3 -m src.main --vfs data/filesystem.csv
echo ""
echo "--- Testing invalid VFS ---"
echo "ls /" | python3 -m src.main --vfs data/nonexistent.csv