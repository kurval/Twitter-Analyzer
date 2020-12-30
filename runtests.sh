#!/bin/bash

# Run app in the background
python ./twa_app/app.py > output_file 2>&1 &
p1=$!

# Running unittests
echo ****UNIT TESTS****
python -m unittest discover -s tests/unit_tests
ret1=$?

# Running UI tests on Chrome
echo ****UI TESTS ON CHROME****
python -m unittest discover -s tests/ui_tests
ret2=$?

# Check if tests fails or passes
if [ $ret1 != 0 ] || [ $ret2 != 0 ]
then
    ret=1
else
    ret=0
fi

# Showing output
echo ****LOGS****
cat output_file

# Kill streamlit process
kill $p1

exit $ret