# aws-demo


### Create key pair. Save private key somewhere safe.
	$ chmod 400 /path/to/keypair.pem

### Choose an Amazon Machine Image (AMI)
I like this one:
	Red Hat Enterprise Linux 7.4 (HVM), SSD Volume Type - ami-26ebbc5c

	$ ssh -i /path/to/keypair.pem ubuntu@instance-public-dns.amazonaws.com

### Initialize instance
	$ sudo apt-get update
	$ sudo apt-get install git

#### Initialize git
If you do not do this you will get the following error: 

	Permission denied (publickey). fatal: Could not read from remote repository. Please make sure you have the correct access rights and the repository exists.

`$ git config --global user.name "Mona Lisa"`

`$ sudo vi ~/.ssh/id_rsa [copy contents from existing private key]`

`$ sudo vi ~/.ssh/id_rsa.pub [copy contents from existing public key]`

`$ git config --global push.default simple`

### Clone Git Repository

	$ git clone https://github.com/carolgrrr/dh-demo.git

### Install dependencies
* Mongodb: install according to [this tutorial](https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/)
* Python

`$ sudo apt install python3-pip`

`$ pip install --upgrade pip`

* Other Python libraries - installed with pip

`$ sudo pip3 install boto3`

`$ sudo pip3 install pymongo`

`$ sudo pip3 install flask`

* Flask

`$ sudo pip3 install Flask-PyMongo`

`$ iptables -I INPUT -p tcp --dport 5000 -j ACCEPT`

* Other

`youtubedl: $ sudo -H pip install --upgrade youtube-dl`

[wordpress](https://www.tecmint.com/install-wordpress-on-ubuntu-16-04-with-lamp/)
