CREATE TABLE IF NOT EXISTS medicalfacility (
  id int(11) NOT NULL AUTO_INCREMENT,
  osmid int(11) NOT NULL,
  north double NOT NULL,
  south double NOT NULL,
  east double NOT NULL,
  west double NOT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 ;
