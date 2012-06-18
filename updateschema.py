#!/usr/bin/env python
import cli.app
import commands
import time

@cli.app.CommandLineApp
def updateschema(app):
	if (app.params.revision == False):
		rev = commands.getoutput("git log --pretty=format:\"%h\" -n 1")
		if (rev and not ("fatal" in rev)):
			app.params.revision = rev
		else:
			print "Cannot get revision number!"
			exit(1)

	if (app.params.password):
		print "I will need mysql password for user '%s'\n" % app.params.user
	min_p = ''
	if (app.params.password):
		min_p = '-p'

	# get current db schema
	# version: a978f3cbe549ca3342fb9fa589ba7837ac3cbd5f
	current_version = commands.getoutput("%s -u %s %s -e 'select version from sqldiff limit 1' --silent --skip-column-name %s" % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname))
	
	# generate sql diff
	tmp_file = "/tmp/sqldiff_%s.sql" % time.time()
	print commands.getoutput('./sqldiff.py %s..%s > %s' % (current_version, app.params.revision, tmp_file))

	print "Applying schema update to current database"
	# apply diff (on db)
	print commands.getoutput("mysql -u %s -e 'source %s;' %s" % (app.params.user, tmp_file, app.params.dbname))

	# bump version (on db)
	print commands.getoutput("mysql -u %s -e  'TRUNCATE sqldiff; INSERT INTO sqldiff values(\"%s\")' %s" % (app.params.user, app.params.revision, app.params.dbname))

	print "Applying schema update to version database"
	# apply diff (on test db)
	print commands.getoutput("mysql -u %s -e 'source %s;' test_%s" % (app.params.user, tmp_file, app.params.dbname))

	# bump version (on test db)
	print commands.getoutput("mysql -u %s -e  'TRUNCATE sqldiff; INSERT INTO sqldiff values(\"%s\")' test_%s" % (app.params.user, app.params.revision, app.params.dbname))

	#cleaning up
	print commands.getoutput("rm %s" % tmp_file)

updateschema.add_param("-d", "--dbname", help="prepare a comparison db for internal sql diffing in each commit. Will be created as test_dname", default="test", action="store")
updateschema.add_param("-m", "--mysqlpath", help="mysql executable path", default="/Applications/XAMPP/xamppfiles/bin/mysql", action="store")
updateschema.add_param("-u", "--user", help="mysql user", default="root", action="store")
updateschema.add_param("-p", "--password", help="enable ask password", default=False, action="store_true")

updateschema.add_param("-r", "--revision", help="revision number for this commit", default=False, action="store")

if __name__ == "__main__":
    updateschema.run()