#!/bin/bash

# Run app in the background
python ./twa_app/app.py -test > log_file 2>&1 &
p1=$!

# Running tests on Chrome
echo Running tests on Chrome
python tests.py
ret=$?

# Check if tests fails or passes
if [ $ret != 0 ]
then
    ret=1
else
    ret=0
fi

# Showing log
echo LOGS
cat log_file

# Kill streamlit process
kill $p1

exit $ret