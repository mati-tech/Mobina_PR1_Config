#!/bin/bash
echo "ls" > /tmp/stage2_test.sh
echo "cd /home" >> /tmp/stage2_test.sh
echo "ls" >> /tmp/stage2_test.sh
echo "exit" >> /tmp/stage2_test.sh
python3 -m src.main --vfs data/filesystem.csv --script /tmp/stage2_test.sh