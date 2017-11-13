#/bin/bash
echo "Cleaning build enviornment"
rm util/*.pyc 2> /dev/null
rm apis/*.pyc 2> /dev/null
rm tests/.cache* 2> /dev/null
rm server/*.pyc 2>/dev/null
rm *.pyc 2> /dev/null
rm .cache* 2>/dev/null
echo "Finished!"
