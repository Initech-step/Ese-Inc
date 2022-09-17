## Task

I was given a task by my school teacher to develop a website to help him effectively manage a writing blog and also serve as a brand website for his Writing agency. 
This website serves two main purposes which include;
1. To promote his writing agency.
2. To serve as a blog for him to publish his creative works.

**Project status: In Progress**
**This project is still in the test stage so using envs are avoided for now**

### Local machine Requirements

Python >= 3.5
Flask==2.1.2
Flask-SQLAlchemy==2.5.1
Flask migrate


**This project uses the bootstrap CDN for its styling, Javascript and Icons which means you will need to have an active internet connection as it connects to bootstrap CDN**

# This is still under active development so it uses SQLite, it doesnt use blueprints for now.
## Steps to get the Project Up and running

1. Fork and Clone this repository
2. In the directory **Ese** start a virtual environment and install requiremens.txt
3. navigate with the terminal into the **Ese/eseinc/** folder
4. in the cmd run `set FLASK_APP=eseweb` to point at the `__init__.py` in eseweb
5. In the terminal run `flask db init` : This is to initialize the database
6. In the terminal run `flask db migrate`
7. In the terminal run `flask db upgrade`
8. navigate with the terminal into the **Ese/eseinc/** folder, this is where this `run.py` is located
9. in the terminal run `python run.py`

**This will expose a localhost Port which you can visit to view the application**
**Enjoy viewing the application and making your own changes**

## Happy Coding