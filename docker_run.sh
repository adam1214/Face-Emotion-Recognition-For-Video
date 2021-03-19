export FER_ROOT=$(pwd)

if [ $# -eq 0 ]
then
	echo "NO arguments supplied"
    docker run --rm \
    -v ${FER_ROOT}:/media \
    biicgitlab.ee.nthu.edu.tw:5050/prod/engineer/fer_offline \
    /bin/bash -c "cd /media; python3 main.py fer_input/ fer_result/ fer_finished/ fer_model/ 720p compress.zip"

else
	echo "Arguments supplied"
    docker run --rm \
    -v ${FER_ROOT}:/media \
    biicgitlab.ee.nthu.edu.tw:5050/prod/engineer/fer_offline \
    /bin/bash -c "cd /media; python3 main.py fer_input/$1 fer_result/$1 fer_finished/$1 fer_model/ 720p compress.zip"
fi