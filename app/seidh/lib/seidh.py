'''
	Seidh library main function. It should be called providing a Biopython's PDB-structured protein,
	a Biopython's PDB-structured peptide (representing the binding point) and the fasta sequence with 
	the aminoacids to add (string type).

	NOTE THAT the fasta sequence should lack as many residues at they are present within the binding point.

	NUM_PROC can be also especified in order to provide multi-core processing capabilities. If no number of
	cores is specified, it will run with the minimum (single-core)
	
	It requires the following external packages:
		-Numpy
		
	In addition to the following, required by additional, internal packages:
		-Biopython
		-PeptideBuilder
		-Multiprocessing
	
'''

import os
import numpy
from datetime import datetime
from cuckoo import cuckoo,rank
from auxiliar import save_structure
from copy import deepcopy
from distance import molecule_contacts
from constants.constants import PROTEINS,PEPTIDES,PREDICTIONS,LOG
from sd.driver import SeidhAdapt
from sd.scoring import seidh_calculate_energy
from constants.constants import MAX_PEPTIDES,MIN_CONTACT,MAX_AA
from clusterize import find_clusters

def seidh(hash,protein,peptide,fasta,NUM_PROC=1):
	'''
		Main function of the seidh library. It requires:
			-A protein structure
			-A binding point (a peptide structure)
			-A fasta sequence
			-(optional) The number of cores to be used.
			
		It creates MAX_PEPTIDES peptides and classify them depending their closeness to the protein to bind.
		It also classify the peptides in clusters depending their distance, in order to identify different conformations. 
			The best peptide overall is then proposed as a solution.
	'''
	start_time=(str(datetime.now())) #time in which the simulation started
	print ("Running simulation with %d cores." % (NUM_PROC))
	adapted_protein=SeidhAdapt(protein)
	i=0
	attempt_times=[0,0,0]
	prediction_list=list()
	while i<MAX_PEPTIDES:
		print ("Peptide number %d simulation begins." % (i+1))
		if not attempt_times[0]:
			attempt_times[0]=(str(datetime.now()))#index0:starting time; index1: definitive version calculated; index2: energy calculated
		tmp_peptide=deepcopy(peptide) #avoiding undesired changes in original peptide
		tmp_peptide=cuckoo(fasta,tmp_peptide,adapted_protein,NUM_PROC)
		attempt_data=([i,1,0])
		if not tmp_peptide:
			print ("The peptide collided. Starting over.\n")
			attempt_data[1]+=1 #adds 1 to the overall attempts counter
			continue
		attempt_times[1]=(str(datetime.now()))
		attempt_data[2]=molecule_contacts(SeidhAdapt(tmp_peptide),adapted_protein)
		if attempt_data[2] < MIN_CONTACT:
			print("Peptide number %d wasn't good enough, but it is saved nonetheless.\nIt won't be taken into account for the best prediction. Still %d peptides to go"%(i+1,MAX_PEPTIDES-i-1))
			attempt_data[0]="discarded_test_"+str(i)
			save_structure(tmp_peptide,"tmp/discarded/"+hash+"/test_"+str(i))
			i+=1
		else:
			save_structure(tmp_peptide,"tmp/valid/"+hash+"/"+str(i))
			c_energy=seidh_calculate_energy(adapted_protein,SeidhAdapt(tmp_peptide))
			attempt_times[2]=(str(datetime.now()))
			prediction_list.append((tmp_peptide,c_energy,i,attempt_data,attempt_times))
			print("Peptide number %d generated! %d to go."%(i+1,MAX_PEPTIDES-i-1))
			i+=1
		attempt_times=[0,0,0]
	if prediction_list:
		clusters=find_clusters([pred[2] for pred in prediction_list],PREDICTIONS+"tmp/valid/"+hash+"/")
		with open(LOG+'simmulation_summary_'+hash+'.log', 'w') as output:
			if clusters > 1:
				output.write("Simulation started:%s\tTotal clusters: %d\tNumber of simulations:%d\tNumber of variants per aminoacid:%d\n" % (start_time,len(clusters),MAX_PEPTIDES,MAX_AA))
				for id_cluster,ids in clusters.iteritems():
					output.write("\nCluster number: %d. Contains %d peptides.\nPeptide ID\tPeptide energy\tN.Attempts\tContact\tStarting time\tCalc. time\tEnergy calc.time\n" % (id_cluster,len(ids)))
					pept_cluster=list()
					for id in ids:
						for prediction in prediction_list:
							if id == prediction[2]:
								output.write("%s\t%f\t%d\t%.2f%%\t%s\t%s\t%s\n"%(str(prediction[3][0]),prediction[1],prediction[3][1],prediction[3][2]*100,prediction[4][0],prediction[4][1],prediction[4][2]))
								pept_cluster.append(prediction)
					pept_cluster.sort(key=lambda x: x[1],reverse=True)
					save_structure(pept_cluster[0][0],hash+"/test_finest_for_cluster_"+str(id))
			else:
				output.write("Simulation started:%s\tTotal clusters: 1\n" % (start_time))
				prediction_list.sort(key=lambda x: x[1],reverse=True)
				prediction=prediction_list[0]
				save_structure(prediction[0],"test_finest")
				output.write("%s\t%f\t%d\t%.2f%%\t%s\t%s\t%s\n"%(str(prediction[3][0]),prediction[1],prediction[3][1],prediction[3][2],prediction[4][0],prediction[4][1],prediction[4][2]))
	else:
		print("No peptide was ok.")
	print("We are done!")

	
	
	