#!/bin/bash

# Run app in the background
python app.py &
p1_pid=$!


# Running tests on Chrome

echo Running tests on Chrome
python tests.py chrome
ret=$?

# Check if tests fails or passes
if [ $ret != 0 ]
then
    ret=1
else
    ret=0
fi

# Kill streamlit process
kill $p1_pid

exit $ret