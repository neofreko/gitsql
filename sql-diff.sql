## mysqldiff 0.43
## 
## Run on Thu May 24 12:57:19 2012
## Options: user=root, debug=0, host=localhost
##
## ---   db: test_test (host=localhost user=root)
## +++   db: test (host=localhost user=root)

CREATE TABLE new_table (
  a int(11) NOT NULL,
  b varchar(45) DEFAULT NULL,
  c varchar(45) DEFAULT NULL,
  PRIMARY KEY (a),
  KEY idx_b (b)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



