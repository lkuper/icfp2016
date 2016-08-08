#/bin/bash

# Usage: submit_solution <problem_id> <solution_file>

curl --compressed -L -H Expect: -H "X-API-Key: `cat POSTMORTEM_APIKEY`" -F "problem_id=$1" -F "solution_spec=@$2" 'http://130.211.240.134/api/solution/submit'
echo ""


