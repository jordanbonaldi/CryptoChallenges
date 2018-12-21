#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

function msg() {
    if [ $? -eq "0" ]
    then
	echo -e "test" $1 ": ${GREEN}OK${NC}"
    else
	echo -e "test" $1 ": ${RED}KO${NC}"
    fi
}

./src/challenge01 inputs/input01 > log
diff log outputs/ex01/output.txt
msg 1
./src/challenge02 inputs/input02 > log
diff log outputs/ex02/output.txt
msg 2
./src/challenge03 inputs/input03 > log
diff log outputs/ex03/output.txt
msg 3
./src/challenge04 inputs/input04 > log
diff log outputs/ex04/output.txt
msg 4
./src/challenge05 inputs/input05 > log
diff log outputs/ex05/output.txt
msg 5
./src/challenge06 inputs/input06 > log
diff log outputs/ex06/output.txt
msg 6
./src/challenge07 inputs/input07 > log
diff log outputs/ex07/output.txt
msg 7
./src/challenge08 inputs/input08 > log
diff log outputs/ex08/output.txt
msg 8
./src/challenge09 inputs/input09 > log
diff log outputs/ex09/output.txt
msg 9
rm log
