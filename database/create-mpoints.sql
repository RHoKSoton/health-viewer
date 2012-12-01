CREATE TABLE IF NOT EXISTS mpoints (
  id int(11) NOT NULL AUTO_INCREMENT,
  medicalfacilityid int(11) NOT NULL,
  lon double NOT NULL,
  lat double NOT NULL,
  PRIMARY KEY (id),
  KEY medicalfacilityid (medicalfacilityid)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 ;
