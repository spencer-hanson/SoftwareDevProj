# Installing Dependencies

You can install the dependencies with 
~~~~ 
sudo pip install -r requirements.txt
~~~~

You may need to install additional packages on Ubuntu
~~~~
sudo apt-get install libffi-dev libssl-dev
sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev
sudo apt-get install python-pip
~~~~

## Common Errors

If you are getting an error about python like so:
~~~~
  File "/usr/local/lib/python2.7/dist-packages/spotipy/util.py", line 56, in prompt_for_user_token
    token_info = sp_oauth.get_cached_token()
  File "/usr/local/lib/python2.7/dist-packages/spotipy/oauth2.py", line 135, in get_cached_token
    if 'scope' not in token_info or not self._is_scope_subset(self.scope, token_info['scope']):
  File "/usr/local/lib/python2.7/dist-packages/spotipy/oauth2.py", line 156, in _is_scope_subset
    needle_scope = set(needle_scope.split())
AttributeError: 'NoneType' object has no attribute 'split'
~~~~
To fix:
~~~~
./clean.sh
~~~~
That means you have a sneaky .cache file hidden in your directory. For some reason the spotipy library doesn't use the token in them, but recognizes that they exist, and lets you pass without getting a token.
Clean.sh just removes the cache files and compiled python code to make sure it's a clean enviornment.


## Running CadenceServer
CadenceServer needs to be started in the Cadence/backend folder context, since it will access other folders for libraries. 
Usage:
~~~~
python server/CadenceServer.py [-test]
~~~~
Or more easily, just run start.sh

The -test option runs the server with no output or input streams, so that it can be used for testcases.






# Cassandra Install information

To install CassandraDB:

You must have latest version of Java 8 and python 2.7 check to see using 
~~~~
java -version
python --version
~~~~
To update Java:
~~~~
sudo apt-add-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
~~~~

If you're running a current build of Ubuntu/Debian based Linux, you should have Python 2.7.x by default.

### Installing CassandraDB:
Current stable build is 3.10

Add the Apache repository of Cassandra to /etc/apt/sources.list.d/cassandra.sources.list
~~~~
echo "deb http://www.apache.org/dist/cassandra/debian 310x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
~~~~

Add the Apache Cassandra repo keys
~~~~
curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
~~~~

Update repos
~~~~	
sudo apt-get update
~~~~

Install Cassandra
~~~~
sudo apt-get install cassandra
~~~~
That should install it. It normally starts automatically, but you can use these commands to start/stop.
~~~~
sudo service cassandra start
sudo service cassandra stop
~~~~

Verify that Cassandra is running by using
~~~~
nodetool status
~~~~

* Default location of config files is /etc/cassandra
* Default loaction of log and data directories are /var/log/cassandra and /var/lib/cassandra
* More CassandraDB documentation is found at: http://cassandra.apache.org/doc/latest/
* There are some pages that have no information, but the "Getting Started" and "Configuring Cassandra" sections have some helpful info.

### Python Driver for Cassandra: 

https://github.com/datastax/python-driver

Easiest to install using pip:
~~~~
pip install cassandra-driver
~~~~

