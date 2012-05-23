## mysqldiff 0.43
## 
## Run on Wed May 23 21:45:15 2012
## Options: user=root, debug=0, host=localhost
##
## ---   db: test2 (host=localhost user=root)
## +++   db: test (host=localhost user=root)

ALTER TABLE new_table ADD COLUMN b varchar(45) DEFAULT NULL;
