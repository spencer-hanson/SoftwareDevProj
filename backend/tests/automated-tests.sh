#!/bin/bash
echo "Running CadenceServer"
./start.sh -test &
sleep 5
python tests/testServer.py | json validate --schema-file=tests/testSchema.json

rm .cache* 2> /dev/null
rm tmp_test.py 2> /dev/null
cat << "EOF" >> "tmp_test.py"
import requests
requests.get('http://localhost:5000/killserver');
EOF
python tmp_test.py
rm tmp_test.py 2> /dev/null

echo "Running LastFM"
python tests/testLastFM.py
