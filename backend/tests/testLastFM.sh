#!/bin/bash
cd backend
result=$(python tests/testLastFM.py)
if [[ $? != 0 ]]; then
	echo "Fail!"
	exit 1
fi
cd ..

