export FER_ROOT=$(pwd)
PROJECT_NAME="fer_batch_processing"

if [ $# -eq 0 ]
then
	echo "NO arguments supplied"
    docker run -ti --rm  --name fer_batch_processing \
    -v ${FER_ROOT}/fer_input:/media/$PROJECT_NAME/fer_input \
    -v ${FER_ROOT}/fer_output:/media/$PROJECT_NAME/fer_output \
    -v ${FER_ROOT}/fer_finished:/media/$PROJECT_NAME/fer_finished \
    -v ${FER_ROOT}/fer_model:/media/$PROJECT_NAME/fer_model \
    -v ${FER_ROOT}/fer_result:/media/$PROJECT_NAME/fer_result \
    biicgitlab.ee.nthu.edu.tw:5050/prod/engineer/fer_offline \
    /bin/bash -c "python3 main.py fer_input/ fer_output/ fer_result/ fer_finished/ fer_model/ 720p"

else
	echo "Arguments supplied"
    docker run -ti --rm  --name fer_batch_processing \
    -v ${FER_ROOT}/fer_input:/media/$PROJECT_NAME/fer_input \
    -v ${FER_ROOT}/fer_output:/media/$PROJECT_NAME/fer_output \
    -v ${FER_ROOT}/fer_finished:/media/$PROJECT_NAME/fer_finished \
    -v ${FER_ROOT}/fer_model:/media/$PROJECT_NAME/fer_model \
    -v ${FER_ROOT}/fer_result:/media/$PROJECT_NAME/fer_result \
    biicgitlab.ee.nthu.edu.tw:5050/prod/engineer/fer_offline \
    /bin/bash -c "python3 main.py fer_input/$1 fer_output/$1 fer_result/$1 fer_finished/$1 fer_model/ 720p"
fi

