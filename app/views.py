import os
import datetime as dt
import hashlib
from constants import PROTEINS,PEPTIDES,PREDICTIONS
from flask import Flask, request, redirect, url_for, render_template, flash
from app import app,db,models,celery
from Bio.PDB import *
from seidh.lib.auxiliar import *
from seidh.lib.seidh import *

@celery.task
def seidh_simulation(hash):
	if not os.path.exists(os.path.join(PREDICTIONS,hash)):
		os.makedirs(os.path.join(PREDICTIONS,hash))
	if not os.path.exists(os.path.join(PREDICTIONS,"tmp/discarded/"+hash)):
		os.makedirs(os.path.join(PREDICTIONS,"tmp/discarded/"+hash))
	if not os.path.exists(os.path.join(PREDICTIONS,"tmp/valid/"+hash)):
		os.makedirs(os.path.join(PREDICTIONS,"tmp/valid/"+hash))

	submission=models.Submission.query.filter_by(hash=hash).first()

	peptide=open_pdb_peptide(submission.peptide_pdb_name)
	protein=open_pdb_protein(submission.protein_pdb_name)
	fasta=cut_peptide(peptide,fasta_ambiguity(submission.fasta_sequence))
	
	print fasta
	
	seidh(hash,protein,peptide,fasta,NUM_PROC=1)
	predicted_files=""
	for file in os.listdir(os.path.join(PREDICTIONS,hash)):
		if os.path.isfile(os.path.join(os.path.join(PREDICTIONS,hash),file)) and file.endswith(".pdb"):
			predicted_files=predicted_files+file+";"
	submission.prediction_name=predicted_files[:-1]
	submission.finishing_time=dt.datetime.utcnow()
	db.session.add(submission)		
	db.session.commit()

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
	if request.method == "POST":
	
		if not is_fasta(request.form['fasta_sequence']):
			flash('The sequence provided was not in FASTA-1 code. Please provide a valid FASTA-1 code.')
			return render_template('index.html')
	
		if 'protein_pdb' not in request.files or 'peptide_pdb' not in request.files:
			flash('Please upload a valid PDB file.')
			return render_template('index.html')
		
		protein_pdb=request.files['protein_pdb']
		peptide_pdb=request.files['peptide_pdb']

		if protein_pdb.filename == '' or peptide_pdb.filename == "":
			flash('Please upload a valid PDB file.')
			return render_template('index.html')
		
		if protein_pdb and allowed_file(protein_pdb.filename):
			protein_pdb_name=name_generator("protein")
			protein_pdb.save(os.path.join(PROTEINS,protein_pdb_name))
			protein=open_pdb_protein(protein_pdb_name)
			try:
				protein[int(request.form['protein_model'])][str(request.form['protein_chain'])]
			except KeyError:
				del_file("protein",protein_pdb_name)
				flash('There was an error with the especification of model or chain of the protein PDB model. Please try again.\nModel especified:%r, chain especified:%r'%(int(request.form['protein_model']),str(request.form['protein_chain'])))
				return render_template('index.html')
			del_file("protein",protein_pdb_name)
			structure_adaptation(protein,int(request.form['protein_model']),str(request.form['protein_chain']),"protein",protein_pdb_name)
		else:
			flash('Please upload a valid PDB file.')
			return render_template('index.html')
			
		if peptide_pdb and allowed_file(peptide_pdb.filename):
			peptide_pdb_name=name_generator("peptide")
			peptide_pdb.save(os.path.join(PEPTIDES,peptide_pdb_name))
			peptide=open_pdb_peptide(peptide_pdb_name)
			try:
				peptide[int(request.form['peptide_model'])][str(request.form['peptide_chain'])]
			except KeyError:
				del_file("peptide",peptide_pdb_name)
				del_file("protein",protein_pdb_name)
				flash('There was an error with the especification of model or chain of the peptide PDB model. Please try again.\nModel especified:%r, chain especified:%r'%(int(request.form['protein_model']),str(request.form['protein_chain'])))
				return render_template('index.html')
			del_file("peptide",peptide_pdb_name)
			structure_adaptation(peptide,int(request.form['peptide_model']),str(request.form['peptide_chain']),"peptide",peptide_pdb_name)
		else:
			del_file("protein",protein_pdb_name)
			flash('Please upload a valid PDB file.')
			return render_template('index.html')			

		hash=hashlib.sha224(str(protein_pdb_name)).hexdigest()
		
		new_submission=models.Submission(hash=hash,
											protein_pdb_name=protein_pdb_name,
											peptide_pdb_name=peptide_pdb_name,
											fasta_sequence=request.form['fasta_sequence'],
											prediction_name="")
		db.session.add(new_submission)
		db.session.commit()
		
		seidh_simulation.delay(hash)
		
		flash('Thank you for trusting us! You can check your work at the following URL. Make sure you copy and paste it and do not lose it!\n%s' % (request.base_url+"p/"+hash))		
		return render_template('index.html')
	else:
		return render_template('index.html')

@app.route('/p/<hash>')
def wip(hash):
	if hash is not None:
		submission=models.Submission.query.filter_by(hash=hash).first()
		if submission is not None:
			then=submission.finishing_time
			if submission.prediction_name:
				files=submission.prediction_name.split(";")
				return render_template('submission.html',files=files,hash=submission.hash)
			else:
				return render_template('submission.html',files=2,hash=0)
		else:
			return render_template('submission.html',files=1,hash=0)
	else:
		return render_template('submission.html',files=0,hash=0)
		
def name_generator(entity):
	name=str(dt.datetime.now()).replace(" ","_").replace(":",".")
	i=0
	if entity=="protein":
		name="prot_"+name+".pdb"
		if not os.path.exists(PROTEINS+name):
			return name
		else:
			while os.path.exists(PROTEINS+name):
				name=str(i)+"_"+name
		return name
	if entity=="peptide":
		name="pept_"+name+".pdb"
		if not os.path.exists(PEPTIDES+name):
			return name
		else:
			while os.path.exists(PEPTIDES+name):
				name=str(i)+"_"+name
		return name
	if entity=="prediction":
		name="pred_"+name+".pdb"
		if not os.path.exists(PREDICTIONS+name):
			return name
		else:
			while os.path.exists(PREDICTIONS+name):
				name=str(i)+"_"+name
		return name
	else:
		return 1


	
