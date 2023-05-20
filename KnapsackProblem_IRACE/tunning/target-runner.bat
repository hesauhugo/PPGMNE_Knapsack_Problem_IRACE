
#!/bin/bash
###############################################################################
# This script is the command that is executed every run.
# Check the examples in examples/
#
# This script is run in the execution directory (execDir, --exec-dir).
#
# PARAMETERS:
# $1 is the candidate configuration number
# $2 is the instance ID
# $3 is the seed
# $4 is the instance name
# The rest ($* after `shift 4') are parameters to the run
#
# RETURN VALUE:
# This script should print one numerical value: the cost that must be minimized.
# Exit with 0 if no error, with 1 in case of error
###############################################################################
EXE=C:/IRACE/KnapsackProblem_IRACE/build/exe.win-amd64-3.9/IRaceBuscaTabuHesau.exe
# EXE=
OUTS="C:/IRACE/KnapsackProblem_IRACE/tunning/OUT/"


CONFIG_ID=$1
INSTANCE_ID=$2
SEED=$3
INSTANCE=$4

shift 4 || error "Not enough parameters"
CONFIG_PARAMS=$*

STDOUT=${OUTS}c${CONFIG_ID}-${INSTANCE_ID}-${SEED}.stdout
STDERR=${OUTS}c${CONFIG_ID}-${INSTANCE_ID}-${SEED}.stderr

if [ ! -x "${EXE}" ]; then
    error "${EXE}: not found or not executable (pwd: $(pwd))"
fi

# If the program just prints a number, we can use 'exec' to avoid
# creating another process, but there can be no other commands after exec.
#exec $EXE ${FIXED_PARAMS} -i $INSTANCE ${CONFIG_PARAMS}
# exit 1
# 
# Otherwise, save the output to a file, and parse the result from it.
# (If you wish to ignore segmentation faults you can use '{}' around
# the command.)
echo "$EXE -i $INSTANCE ${CONFIG_PARAMS}" >> ${STDERR}.log
$EXE -i $INSTANCE ${CONFIG_PARAMS} 1> ${STDOUT} 2> ${STDERR}

# # This may be used to introduce a delay if there are filesystem
# # issues.
# SLEEPTIME=1
# while [ ! -s "${STDOUT}" ]; do
#     sleep $SLEEPTIME
#     let "SLEEPTIME += 1"
# done

# This is an example of reading a number from the output.
# It assumes that the objective value is the first number in
# the first column of the last line of the output.
if [ -s "${STDOUT}" ]; then
    COST=$(tail -n 1 ${STDOUT} | grep -e '^[[:space:]]*[+-]\?[0-9]' | cut -f1)
    echo "$COST"
    #rm -f "${STDOUT}" "${STDERR}"
    rm -f "${STDOUT}" "${STDERR}" "${STDERR}.log"
    exit 0
else
    error "${STDOUT}: No such file or directory"
fi

