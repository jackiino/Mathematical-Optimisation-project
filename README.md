# Mathematical-Optimisation-project
This repository includes a project for a course named Mathematical Optimisation, which is a course released by University of Trieste. The rules of the project are specified on a website of the professor who teaches the course, Lorenzo Castelli (https://sites.units.it/castelli/didattica/?file=mathopt.html). 

I implemented the pseudocodes for solving the Rainbow Steiner Tree Problem (RSTP) presented in the following paper: 
Daniele Ferone, Paola Festa, Francesca Guerriero,
The Rainbow Steiner Tree Problem,
Computers & Operations Research,
Volume 139,
2022,
105621,
ISSN 0305-0548,
https://doi.org/10.1016/j.cor.2021.105621.
(https://www.sciencedirect.com/science/article/pii/S030505482100335X)
Abstract: Given an undirected and edge-colored graph with non-negative edge lengths, the aim of the Rainbow Steiner Tree Problem (RSTP) is to find a minimum Steiner Tree that uses at most one edge for each color. In this paper, the RSTP is introduced, a mathematical model is proposed to formally represent the problem and its theoretical properties are investigated. Since the RSTP belongs to the NP-class, two heuristic methods are designed: a Lagrangian relaxation approach and a multistart algorithm. Extensive computational experiments are carried out on a significant set of test problems to empirically evaluate the performance of the proposed approaches. The computational results show that the two approaches are both effective and efficient compared to the ILOG CPLEX solver.
Keywords: Steiner tree; Edge-colored graphs; Spanning tree

## Remark
The code for fonding optimal solution is implemented with gurobi solver.

## Content

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
