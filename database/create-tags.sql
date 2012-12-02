CREATE TABLE IF NOT EXISTS tags (
  id int(11) NOT NULL AUTO_INCREMENT,
  medicalfacilityid int(11) NOT NULL,
  okey varchar(255) NOT NULL,
  oval varchar(255) NOT NULL,
  PRIMARY KEY (id),
  KEY medicalfacilityid (medicalfacilityid)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 ;
