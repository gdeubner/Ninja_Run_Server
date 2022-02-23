INSTALLATION GUIDE:

DEPENDENCIES: (Install these before running the program)

pip install httptools==0.1.0
sudo apt-get update -y
sudo apt-get install -y libmariadb-dev
pip3 install mariadb
pip install "fastapi[all]"
pip install "uvicorn[standard]"

STARTING THE SERVER:

uvicorn ninjaApp:app --host cs431-08.cs.rutgers.edu --port 3000 --reload

ACCESSING SERVER:

Use Cisco VPN or be connected to RUWireless Secure, then go to the following link:
	cs431-08.cs.rutgers.edu:3000
