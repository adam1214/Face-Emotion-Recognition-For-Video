@echo OFF
set FER_ROOT="%cd%"

IF [%1] == [] (
		echo NO arguments passed
		docker run --rm ^
		-v %FER_ROOT%:/media ^
		biicgitlab.ee.nthu.edu.tw:5050/prod/engineer/fer_offline:latest ^
		/bin/bash -c "cd /media; python3 main.py fer_input/ fer_result/ fer_finished/ fer_model/ 720p compress.zip"
	) ELSE	(
		echo Arguments passed
		docker run --rm  ^
		-v %FER_ROOT%:/media ^
		biicgitlab.ee.nthu.edu.tw:5050/prod/engineer/fer_offline:latest ^
		/bin/bash -c "cd /media; python3 main.py fer_input/%1 fer_result/%1 fer_finished/%1 fer_model/ 720p %1.zip"
	)
pause
