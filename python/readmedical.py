#!/usr/bin/env python

# process an OSM file to extract roads 

# Licence: DWYWT v 1.0 See LICENCE file

import sys
import os.path
import argparse
import codecs
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import MySQLdb as mdb

from osm import *
from hupd import *

__version__='0.1'
__progdesc__='Extract road details from OSM data'

def main():
	#sort out the command line stuff
	parser = argparse.ArgumentParser(description=__progdesc__)
	arga=get_args(parser)
	results = parser.parse_args()
	if arga.inosm=='':
		print '{0} version {1}'.format(__progdesc__,__version__) 
		print 'OSM file name is required (-i)'
		sys.exit(4)
	if not os.path.exists(arga.inosm):
		print '{0} version {1}'.format(__progdesc__,__version__) 
		print 'OSM file {0} cannot be found'.format(arga.inosm)
		sys.exit(5)
	if arga.verbose:
		arga.quiet=False
	if not arga.quiet:
		print '{0} version {1}'.format(__progdesc__,__version__) 
	if arga.verbose:
		print 'Input OSM file: {0}'.format(arga.inosm)
		print 'Text ouput file: {0}'.format(arga.outtxt)
		print 'Quiet mode: {0}'.format(arga.quiet)
		print 'Verbose: {0}'.format(arga.verbose)
	
	# parse the osm file
	OSM = OSMHandler()
	saxparser = make_parser()
	saxparser.setContentHandler(OSM)

	datasource = open(arga.inosm,"r")
	saxparser.parse(datasource)
	datasource.close
		
	print 'Nodes {0}'.format(len(OSM.Nodes))
	print 'Ways {0}'.format(len(OSM.Ways))
	print 'Relations {0}'.format(len(OSM.Relations))
	
	# open the database ready for updates
	h,u,p,d = hupd() # get the host, username password and database from an import file so it's not hardcoded here
	conn = mdb.connect(h,u,p,d)
	croad = conn.cursor()

	# this is a set of hoghway types I'm interested in
	amenities=('hospital','doctors','dentist')

	# find the ways that are highways
	for wid in OSM.Ways.keys():
		way = OSM.Ways[wid]
		if 'amenity' in way.Tags and way.Tags['amenity'] in amenities:
			# get north, south east & west max
			n=int(way.Nds[0])
			north = OSM.Nodes[n].Lat
			south = OSM.Nodes[n].Lat
			east = OSM.Nodes[n].Lon
			west = OSM.Nodes[n].Lon
			for n in way.Nds:
				if north < OSM.Nodes[int(n)].Lat:
					north = OSM.Nodes[int(n)].Lat
				if south > OSM.Nodes[int(n)].Lat:
					south = OSM.Nodes[int(n)].Lat
				if east < OSM.Nodes[int(n)].Lon:
					east = OSM.Nodes[int(n)].Lon
				if west > OSM.Nodes[int(n)].Lon:
					west = OSM.Nodes[int(n)].Lon
			if 'name' in way.Tags:
				name = way.Tags['name']
			else:
				name=''
			amenity=way.Tags['amenity']
			croad.execute("INSERT INTO medicalfacility (osmid,north,south,east,west,amenity,name) VALUES(%s,%s,%s,%s,%s,%s,%s)",\
                    (way.WayID,north,south,east,west,amenity,name))
			wayid=croad.lastrowid
			for n in way.Nds:
				lon=OSM.Nodes[int(n)].Lon
				lat=OSM.Nodes[int(n)].Lat
				croad.execute("INSERT INTO mpoints (medicalfacilityid,lon,lat) VALUES(%s,%s,%s)",(wayid,lon,lat))

    for nid in OSM.Nodes.keys():
        node = OSM.nodes[nid]
        if 'amenity' in node.Tags and node.Tags['amenity'] in amenities:
            lat = node.Lat
            lon = node.Lon
            amenity = node.Tags['amenity']
            name = node.Tags['name']
            croad.execute("INSERT INTO medicalfacility (osmid,north,south,east,west,amenity,name) VALUES(%s,%s,%s,%s,%s,%s,%s)",\
                    (node.NodeID,lat,lat,lon,lon,amenity,name))
            mfid = croad.lastrowid
            croad.execute("INSERT INTO mpoints (medicalfacilityid,lon,lat) VALUES(%s,%s,%s)",\
                    (mfid,lat,lon))

	conn.close()


def get_args(parser):
	'''parse the command line'''
	parser.add_argument('-i', action='store', default='', dest='inosm', help='Input OSM file')
	parser.add_argument('-o', action='store', default='out.txt', dest='outtxt', help='Output text file')
	parser.add_argument('-q', action='store_true', default=False, dest='quiet', help='Process quietly')
	parser.add_argument('-v', action='store_true', default=False, dest='verbose', help='Verbose, overrides quiet (-q)')
	
	results = parser.parse_args()
	return results

if __name__ == '__main__':
	
	main()
