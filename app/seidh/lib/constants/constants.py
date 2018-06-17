'''
	This file contains the constants and directories used by Seidh.
	It also especifies some basic configuration such as:
	->MAX_AA: number of tries per aminoacid in a single peptide simulation
	->MAX_PEPTIDES: number of peptide simulations
	->NUM_PROC: number of processors to use. 

'''

import os

basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.realpath(os.path.join(basedir, '../../../'))

PROTEINS = basedir+'/static/pdb_files/protein_files/'
PEPTIDES = basedir+'/static/pdb_files/peptide_files/'
PREDICTIONS = basedir+'/static/pdb_files/prediction_files/'
LOG = basedir+'/static/log/'

ALLOWED_EXTENSIONS = set(['pdb','ent'])

MAX_AA=20
MAX_PEPTIDES=2
MIN_CONTACT=0.40


class textformat:
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	ENDC = '\033[0m'