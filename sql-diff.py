#!/usr/bin/env python
import cli.app
import commands

@cli.app.CommandLineApp
def sqldiff(app):
	# log up to this commit
	# git log --format=oneline 545784c010e1400e9b05d737877d3c223de6065d sql-diff.sql

	# log after this, up to this
	# git log --format=oneline ba4c9c3dcf53ef7df5ae2ccecdc228170c0d949c~1..545784c010e1400e9b05d737877d3c223de6065d sql-diff.sql
	diff = commands.getoutput('git log --reverse --pretty=format:"%h" sql-diff.sql').splitlines()
	for x in diff:
		print commands.getoutput("git show %s:sql-diff.sql" % x)

sqldiff.add_param("-p", "--prefix", help="prepare a comparison db for internal sql diffing in each commit", default="test", action="store")


if __name__ == "__main__":
    sqldiff.run()
