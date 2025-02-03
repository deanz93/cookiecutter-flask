#!/bin/bash
set -e

cmd="$@"

if [ ${IS_CELERY} = "true" ]
then

    echo "-----------------------------------------------------"
    echo "FINISHED CELERY ENTRYPOINT --------------------------"
    echo "-----------------------------------------------------"
    echo "Executing Celery server $cmd for Production"
else

    echo "-----------------------------------------------------"
    echo "FINISHED DJANGO ENTRYPOINT --------------------------"
    echo "-----------------------------------------------------"
    echo "Executing Flask server $cmd for Production"
fi


# Run the CMD
echo "got command $cmd"
exec /bin/sh -c "$cmd"

