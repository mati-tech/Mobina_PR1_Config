#!/bin/bash
cat << 'EOF' > /tmp/stage4.sh
find / -name test.txt
tac /home/user/docs/test.txt
who
exit
EOF
python3 -m src.main --vfs data/filesystem.csv --script /tmp/stage4.sh