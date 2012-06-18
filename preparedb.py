#!/usr/bin/env python
import cli.app
import commands

@cli.app.CommandLineApp
def preparedb(app):
	print "Preparing comparison db: test_%s\n" % app.params.dbname
	if (app.params.password):
		print "I will need mysql password for user '%s'\n" % app.params.user
	min_p = ''
	if (app.params.password):
		min_p = '-p'

	if (app.params.revision == False):
		rev = commands.getoutput("git log --pretty=format:\"%h\" -n 1")
		if (rev and not ("fatal" in rev)):
			app.params.revision = rev
		else:
			print "You need at least 1 commit before preparing the db"
			exit(1)
	
	#print "%s -u %s %s -e 'create database %s'" % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname)
	
	# if not exist, create one and sync from origin
	db_exists = commands.getstatusoutput("%s -u %s %s -e 'use test_%s'" % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname))

	if (db_exists[0] != 0):
		print "Creating database.."
		print commands.getoutput("%s -u %s %s -e 'create database test_%s'" % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname))
		#sync from origin
		tmp_schema = "/tmp/%s-schema.sql" % app.params.dbname
		print "Copying schema.."
		mdump = commands.getoutput("mysqldump -n -d -u %s %s > %s" % (app.params.user, app.params.dbname, tmp_schema))
		if ("ERROR" in mdump):
			print "Unable to dump database %s" % app.params.dbname
			exit(1)
		print "importing initial schema.."
		print commands.getoutput("mysql -u %s -e 'source %s;' %s" % (app.params.user, tmp_schema, app.params.dbname))

		# create version table (sqldiff) on subject db
		print "creating revision table sqldiff on subject db: %s .." % app.params.dbname
		print commands.getoutput("mysql -u %s -e  'CREATE TABLE `sqldiff` ( `version` varchar(100) NOT NULL, PRIMARY KEY (`version`)) ENGINE=MyISAM DEFAULT CHARSET=latin1; INSERT INTO sqldiff values(\"%s\")' %s" % (app.params.user, app.params.revision, app.params.dbname))

		# create version table (sqldiff) on test_db
		print "creating revision table sqldiff on test_%s" % app.params.dbname
		print "mysql -u %s -e  'CREATE TABLE `sqldiff` ( `version` varchar(100) NOT NULL, PRIMARY KEY (`version`)) ENGINE=MyISAM DEFAULT CHARSET=latin1; INSERT INTO sqldiff values(\"%s\")' test_%s" % (app.params.user, app.params.revision, app.params.dbname)
		print commands.getoutput("mysql -u %s -e  'CREATE TABLE `sqldiff` ( `version` varchar(100) NOT NULL, PRIMARY KEY (`version`)) ENGINE=MyISAM DEFAULT CHARSET=latin1; INSERT INTO sqldiff values(\"%s\")' test_%s" % (app.params.user, app.params.revision, app.params.dbname))
		
		# cleaning up
		print commands.getoutput("rm %s" % tmp_schema)
	
	print "Done"

preparedb.add_param("-d", "--dbname", help="prepare a comparison db for internal sql diffing in each commit. Will be created as test_dname", default="test", action="store")
preparedb.add_param("-m", "--mysqlpath", help="mysql executable path", default="/Applications/XAMPP/xamppfiles/bin/mysql", action="store")
preparedb.add_param("-u", "--user", help="mysql user", default="root", action="store")
preparedb.add_param("-p", "--password", help="enable ask password", default=False, action="store_true")

preparedb.add_param("-r", "--revision", help="revision number for this commit", default=False, action="store")

if __name__ == "__main__":
    preparedb.run()