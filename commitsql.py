#!/usr/bin/env python
import cli.app
import commands
import time
from time import gmtime, strftime

@cli.app.CommandLineApp
def commitsql(app):
	# get diff
	tmp_file = "/tmp/sqldiff_%s.sql" % time.time()
	print "creating mysql diff..."
	if (app.params.password):
		print "I will need mysql password for user '%s'\n" % app.params.user
	min_p = ''
	if (app.params.password):
		min_p = '-p'

	print commands.getoutput('%s -u %s -h localhost %s test_%s %s > %s' % (app.params.mysqldiff, app.params.user, min_p, app.params.dbname, app.params.dbname, tmp_file))

	print "sql diff:"
	print commands.getoutput('cat %s' % tmp_file)

	# apply to db
	successful = commands.getstatusoutput('%s -u %s -h localhost %s test_%s < %s' % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname, tmp_file))
	
	if (successful[0] != 0):
		print "Unable to apply sql diff. Commit aborted!"
		return successful[0];

	# commit sql if successful
	print "sql diff applied to test_db. Committing changes to git.."
	commands.getoutput('cat %s > sql-diff.sql' % tmp_file)
	print commands.getoutput('git commit sql-diff.sql -m "sql diff %s"' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

commitsql.add_param("-d", "--dbname", help="prepare a comparison db for internal sql diffing in each commit", default="test", action="store")
commitsql.add_param("-m", "--mysqldiff", help="mysqldiff executable path", default="mysqldiff", action="store")
commitsql.add_param("-u", "--user", help="mysql user", default="root", action="store")
commitsql.add_param("-p", "--password", help="enable ask password", default=False, action="store_true")
commitsql.add_param("-x", "--mysqlpath", help="mysql executable path", default="/Applications/XAMPP/xamppfiles/bin/mysql", action="store")


if __name__ == "__main__":
    commitsql.run()
