#!/usr/bin/env python
import cli.app
import commands
import time
from time import gmtime, strftime

@cli.app.CommandLineApp
def commitsql(app):
	# don't execute this if committing sql-diff
	checkedin = commands.getoutput('git diff --cached --name-only --diff-filter=ACM')
	print "Is this sql-dff.sql itself being checked in?"
	print checkedin
	if ("sql-diff" in checkedin):
		print "Yep. Let it go. Bypass pre-commit for sql-diff.sql"
		exit(0)
	else:
		print "Nope. Let's do the drill.."

	# get diff
	tmp_file = "/tmp/sqldiff_%s.sql" % time.time()
	print "creating mysql diff..."
	if (app.params.password):
		print "I will need mysql password for user '%s'\n" % app.params.user
	min_p = ''
	if (app.params.password):
		min_p = '-p'

	#print '%s -u %s -h localhost %s test_%s %s > %s' % (app.params.mysqldiff, app.params.user, min_p, app.params.dbname, app.params.dbname, tmp_file)

	# be warned that AUTOINCREMENT is also considered schema change!!
	print '%s -u %s -h localhost %s db:test_%s db:%s > %s' % (app.params.mysqldiff, app.params.user, min_p, app.params.dbname, app.params.dbname, tmp_file)
	print commands.getoutput('%s -u %s -h localhost %s db:test_%s db:%s > %s' % (app.params.mysqldiff, app.params.user, min_p, app.params.dbname, app.params.dbname, tmp_file))

	print "sql diff:"
	print commands.getoutput('cat %s' % tmp_file)
	#print '%s -u %s -h localhost %s test_%s < %s' % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname, tmp_file)

	# apply to db
	successful = commands.getstatusoutput('%s -u %s -h localhost %s test_%s < %s' % (app.params.mysqlpath, app.params.user, min_p, app.params.dbname, tmp_file))

	if (successful[0] != 0):
		print "Unable to apply sql diff. Commit aborted!"
		return successful[0];

	# commit sql if successful
	print "sql diff applied to test_db. Committing changes to git.."
	commands.getoutput('cat %s > sql-diff.sql' % tmp_file)
	# add sql-diff.sql to git, just in case it's not added yet
	print "sql-diff.sql created"
	print commands.getoutput('git add sql-diff.sql')
	#print "git commit-ing sql-diff.sql"
	#print 'git commit sql-diff.sql --no-verify -m "sql diff %s"' % strftime("%a, %d %b %Y %H:%M:%S", gmtime())
	#print commands.getoutput('git commit sql-diff.sql --no-verify -m "sql diff %s"' % strftime("%a, %d %b %Y %H:%M:%S", gmtime()))

	# update version
	revision = commands.getoutput("git log --pretty=format:\"%h\" -n 1 sql-diff.sql")
	print "updating revision info table: %s" % revision
	print '%s -u %s -h localhost %s -e "truncate sqldiff; insert into sqldiff values(\'%s\')" test_%s' % (app.params.mysqlpath, app.params.user, min_p, revision, app.params.dbname)
	successful = commands.getstatusoutput('%s -u %s -h localhost %s -e "truncate sqldiff; insert into sqldiff values(\'%s\')" test_%s' % (app.params.mysqlpath, app.params.user, min_p, revision, app.params.dbname))
	
	if (successful[0] != 0):
		print "Unable to bump schema version. You need to manually update sqldiff table in test_%s with '%s'" % (app.params.dbname, revision)
		return exit(1);

	#cleaning up
	print commands.getoutput("rm %s" % tmp_file)

commitsql.add_param("-d", "--dbname", help="prepare a comparison db for internal sql diffing in each commit", default="test", action="store")
commitsql.add_param("-m", "--mysqldiff", help="mysqldiff executable path", default="mysqldiff", action="store")
commitsql.add_param("-u", "--user", help="mysql user", default="root", action="store")
commitsql.add_param("-p", "--password", help="enable ask password", default=False, action="store_true")
commitsql.add_param("-x", "--mysqlpath", help="mysql executable path", default="mysql", action="store")
#commitsql.add_param("revision", help="revision number for this commit", action="store")


if __name__ == "__main__":
    commitsql.run()
