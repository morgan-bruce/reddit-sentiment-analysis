if [ ! -d venv ]
then
    echo "Creating virtual environment for initialization"
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
fi

VENV_PYTHON=./venv/bin/python

echo "Pulling data from Reddit API"
pull_data_start=`date +%s.%N`
$VENV_PYTHON pull_data.py
pull_data_end=`date +%s.%N`
pull_data_runtime=$(echo "$pull_data_end - $pull_data_start" | bc -l)
echo "Pulling data completed in $pull_data_runtime seconds"

echo "Running sentiment analysis on pulled data"
$VENV_PYTHON predict.py
