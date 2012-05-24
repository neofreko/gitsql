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
	print commands.getoutput("%s -u %s %s -e 'create database %s'" % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname))
	pass

preparedb.add_param("-d", "--dbname", help="prepare a comparison db for internal sql diffing in each commit", default="test_test", action="store")
preparedb.add_param("-m", "--mysqlpath", help="mysql executable path", default="/Applications/XAMPP/xamppfiles/bin/mysql", action="store")
preparedb.add_param("-u", "--user", help="mysql user", default="root", action="store")
preparedb.add_param("-p", "--password", help="enable ask password", default=False, action="store_true")

if __name__ == "__main__":
    preparedb.run()