#!/usr/bin/env python
import cli.app
import commands

@cli.app.CommandLineApp
def preparedb(app):
	print "Preparing comparison db: %s\n" % app.params.dbname
	if (app.params.password):
		print "I will need mysql password for user '%s'\n" % app.params.user
	min_p = ''
	if (app.params.password):
		min_p = '-p'
	
	#print "%s -u %s %s -e 'create database %s'" % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname)
	
	# if not exist, create one and sync from origin
	db_exists = commands.getstatusoutput("%s -u %s %s -e 'use test_%s'" % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname))

	if (db_exists[0] != 0):
		print "Creating database.."
		print commands.getoutput("%s -u %s %s -e 'create database test_%s'" % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname))
		#sync from origin
		tmp_schema = "/tmp/%s-schema.sql" % app.params.dbname
		print "Copying schema.."
		print commands.getoutput("mysqldump -n -d -u %s %s > %s" % (app.params.user, app.params.dbname, tmp_schema))
		print commands.getoutput("mysql -u %s -e 'source %s;' %s" % (app.params.user, tmp_schema, app.params.dbname))
		
		# cleaning up
		print commands.getoutput("rm %s" % tmp_file)
	
	print "Done"

preparedb.add_param("-d", "--dbname", help="prepare a comparison db for internal sql diffing in each commit. Will be created as test_dname", default="test", action="store")
preparedb.add_param("-m", "--mysqlpath", help="mysql executable path", default="/Applications/XAMPP/xamppfiles/bin/mysql", action="store")
preparedb.add_param("-u", "--user", help="mysql user", default="root", action="store")
preparedb.add_param("-p", "--password", help="enable ask password", default=False, action="store_true")

if __name__ == "__main__":
    preparedb.run()