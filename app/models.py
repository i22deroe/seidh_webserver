from app import db
import datetime

class Submission(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	submission_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	hash = db.Column(db.String(256), index=True, unique=True)
	protein_pdb_name = db.Column(db.String(120), index=True, unique=True)
	peptide_pdb_name = db.Column(db.String(120), index=True, unique=True)
	fasta_sequence = db.Column(db.String(20), index=True)
	prediction_name = db.Column(db.String(120))
	finishing_time = db.Column(db.DateTime, default=None)
	
	def __repr__(self):
		return '<Submission with ID %s and hash %s submitted on %s>' % (self.id,self.hash,self.submission_time)