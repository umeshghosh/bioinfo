# Makes coarse grain PDB file visible by adding CONNECT records
#!/usr/bin/python
import sys, os, re

class Atom:
	def __init__(self, line):
		self.resid = line[17:20]
		self.resn = int( line[22:26] )
		self.atomn = int( line[7:11] )
		self.atomid = line[12:16]
		
def parsePDB( name ):
	f = None
	try:
		f = open( name )
	except IOError:
		print "No such filename"
		sys.exit(1)
	return f.readlines()
	
def extract( lines ):
	protein = 0
	helices = []
	p1 = re.compile( r'^[\ 0-5][B].*' )
	p2 = re.compile( r'^[B].*' )
	aas = [ "GLY","ALA","VAL","LEU","ILE","THR","PHE","TYR","TRP","SER","CYS","MET","GLU","GLN","ASP","ASN","HIS","ARG","LYS","PRO"]
	chain = ' '
	for line in lines:
		if( (len( p1.findall( line[12:16] ) ) > 0 or len(p2.findall( line[12:16] )) > 0 ) and ( line[0:6] == "ATOM  " ) ):
			#print line
			if( protein == 0 or (protein == 1 and chain != line[21])):
				protein = 1
				helices.append( [] )
				chain = line[21]
			helices[-1].append( Atom( line ) )
		elif( line[17:20] not in aas):
			protein = 0
		elif ( line[0:6] != "ATOM  " and line[0:6] != "HETATM" ):
			protein = 0
	print len(helices)
	return helices
    
def connect_dppc( lines ):
	conn = ""
	for line in lines:
		if line[ 17:20 ] == "DPP" and line[ 12:16 ] == " NC3":
			i = int( line[7:11] )
			conn += ( "CONECT %4i %4i \n" %( i, i+1 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+1, i, i+2 ) )
			conn += ( "CONECT %4i %4i %4i %4i \n" %( i+2, i+1, i+3, i+4 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+3, i+2, i+8 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+4, i+2, i+5 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+5, i+4, i+6 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+6, i+5, i+7 ) )
			conn += ( "CONECT %4i %4i \n" %( i+7, i+6 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+8, i+3, i+9 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+9, i+8, i+10 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+10, i+9, i+11 ) )
			conn += ( "CONECT %4i %4i \n" %( i+11, i+10 ) )
	return conn        
    
def connect_dpc( lines ):
	conn = ""
	for line in lines:
		if line[ 17:20 ] == "DPC" and line[ 12:16 ] == " NC3":
			i = int( line[7:11] )
			conn += ( "CONECT %4i %4i \n" %( i, i+1 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+1, i, i+2 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+2, i+1, i+3 ) )
			conn += ( "CONECT %4i %4i %4i \n" %( i+3, i+2, i+4 ) )
			conn += ( "CONECT %4i %4i \n" %( i+4, i+3 ) )
	return conn

def make_map( helices ):
	contact_map = []
	for hx in helices:
		contact_map.append( [] )
		size = len(hx)
		for i in range( 0, size ):
			try:
				contact_map[ -1 ].append( [ hx[ i ].atomn, hx[ i-1 ].atomn, hx[ i+1 ].atomn ] )
			except IndexError:
				try:
					contact_map[ -1 ].append( [ hx[ i ].atomn, hx[ i-1 ].atomn ] )
				except IndexError:
					contact_map[ -1 ].append( [ hx[ i ].atomn, hx[ i+1 ].atomn ] )
		contact_map[-1][0].remove( contact_map[-1][0][1] )
	return contact_map

def connect_CA( map ):
	conect = ""
	for hx in map:
		for atom in hx:
			s = len(atom)
			if( s == 2 ):
				conect += ( "CONECT %4i %4i\n" %( atom[0], atom[1] ) )
			elif( s == 3 ):
				conect += ( "CONECT %4i %4i %4i\n" %( atom[0], atom[1], atom[2] ) )
	return conect
    
def write_it_all( fname, conect ):
	f = None
	try:
		f = open( fname, 'r' )
	except IOError:
		print "No such filename"
		sys.exit(1)
	
	lines = f.readlines()
	s = len(lines)
	towrite = lines
	for i in range( 0, s ):
		if( lines[ s - i - 1 ][0:3] == "END" ):
			towrite = lines[0:s-i-1]
			break
	f.close()
	f = open( fname[:-4]+'_CONECT.pdb', 'w' )
	for w in towrite:
		f.write( w )
	f.write( conect )
	f.write( "ENDMDL\n" )
	f.close()

def main():
	fname = None
	try:
		fname = sys.argv[1]
	except IndexError:
		print "Usage: "+sys.argv[0]+" <filename>\n"
		sys.exit(1)
	connstr = ""
 	lines = parsePDB( fname ) 
	connstr += connect_dppc( lines )	
	connstr += connect_dpc( lines )
	connstr += connect_CA( make_map( extract( lines ) ) )
	write_it_all( fname, connstr )
	
if( __name__ == "__main__" ):
	main()
		
