This folder contains the files to run the algorithms for solving the RSTP, written by Giacomo Davide
email: Jackk.davide@gmail.com

The folder contains two files:
-test.py
	it is used to test the algorithms for very easy instances. You can change the values of the instance from the file "instance_test.py" which is located in the package folder.

-scalability.py
	it is used to test the scalability of the algorithms over large instances. The instances used for scalability analysis are located in the folder Instances_scalability.


The folder contains the following folders:
-package:
	it is a folder used to store every includes in which you can also modify the hyperparameters

-Instances_scalability
	it contains the files used to perform scalability. The file are organised in the following way:
		b-xy : contains small instances (number of nodes 50-100, number of edges 63-200, number of terminals 9-50)
		i080-xyz : contains large instances (number of nodes 80, number of edges 632-3160, number of terminals 8)
		pxyz : contains large instances (number of nodes 100, number of edges 4950, number of terminals 50)

Hyperparameters of MA can be changed directly from "multistart1.py" code. While, for LR hyperparameters can be changed from the file named "LR_hyperparameters".

A brief description of the structure of the code:
When you run test.py a folder named "Results_test" will be created. Here, you will find the results for each algorithm (the results of MA and LR are an average over several iterations you can decide in the hyperparameters). Anyway, results of each iteration will be stored in folders named "Results_iterations".
While, when you run scalability.py a folder named "Results" will be created. Here, you will find the results as well. Also in this case, results of each iteration are stored in the folder named "Results_iterations_test" 