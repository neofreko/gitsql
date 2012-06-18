Dependencies:

1. [MySQL::Diff] [1] from CPAN 
2. mysql and its utilities should be on $PATH. Pay attention if you are on Mac OSX and using MAMP or whatnot ;)
3. [PyCLI] [2]

  $ pip install pyCLI

Steps:

1. Prepare DBs. Prepare DB will require you to have at least one prior commit.

  python ~/Documents/SOURCES/sql-sync/preparedb.py -d &lt;database name&gt;

2. place the pre-commit and post-pull hook

  ###pre-commit
  python ./commitsql.py -d &lt;database name&gt;

  ###post-merge
  tbd
 
3. start committing

  [1]: http://search.cpan.org/~aspiers/MySQL-Diff-0.43/lib/MySQL/Diff.pm
  [2]: http://packages.python.org/pyCLI/
