#!/bin/bash
cat << 'EOF' > /tmp/stage5.sh
mkdir /home/user/newdir
ls /home/user
exit
EOF
python3 -m src.main --vfs data/filesystem.csv --script /tmp/stage5.sh