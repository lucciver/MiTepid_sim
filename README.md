# MiTepid_sim
Simulating a stratified model for the spread of COVID19 in any population with known age structure, Made in Tübingen. 

For detailed info of the basis of the model, please look at:
http://people.tuebingen.mpg.de/vbokharaie/pdf_files/Quantifying_COVID19_Containment_Policies.pdf
All the figures in the above-mentioned manuscript are produced using this repository.

In essence, this code simply simulates a set of nonlinear ODEs which can simulate the spread of a virus in a population, using both SIR and SIS models. The parameters of this model are estimated based on the available data on the spread of COVID-19. The details of that method, which relies on an optimisation scheme, are explined in the mansucript. The optimisation itself is done using GLobal Optimisation Toolbox in Matlab. But the optimsed values of contact rates are uploaded with this code. Hence the code should work well under Python 3. 

Updates on the model and how it cna be used to predict the spread of COVID-19 can be found in:
https://people.tuebingen.mpg.de/vbokharaie/
