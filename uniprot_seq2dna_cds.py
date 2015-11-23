# Gets DNA CDS sequence from uniprot protein sequence
# usage python uniprot_seq2dna_cds.py *.fa > *_dna.fa
from urllib2 import urlopen
from Bio.SeqIO import parse
from sys import argv


with open('dna.log','w') as f:
  for rec in parse(argv[1],'fasta'):
#	embl=list(parse(urlopen('http://www.uniprot.org/uniprot/'+uni+'.txt'),'swiss'))[0]#.dbxrefs # does not work
#	print embl		
	uni=rec.id.split('|')
	id1=urlopen('http://www.uniprot.org/uniprot/'+uni[1]+'.txt').read().replace(';','').split('EMBL')
#	n=id1.index('mRNA.')
	if len(id1)==1:
		f.write('failed: '+rec.id)
	for i in id1[:-1]:
		id2= i[-20:].split()[-2]
		dna=list(parse(urlopen('http://www.ebi.ac.uk/ena/data/view/'+id2.split('.')[0]+'&display=fasta'),'fasta'))[0]
#		f.write( id2 + ' '+ str(len(rec)) + ' '+ dna.id + ' ' + str(len(dna.seq)) + '\n' )
		if len(dna)==len(rec)*3+3:
#			f.write( id2 + ' '+ str(len(rec)) + ' '+ dna.id + ' ' + str(len(dna.seq)) + '\n' )
			print '>'+uni[0]+'|'+uni[2]
			print dna.seq	
			break	
		else:
			f.write('failed: '+rec.id)	
