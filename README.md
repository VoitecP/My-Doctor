# My Doctor 


## Info
Aplication  for registered user's that allows to select one role (Patient or Doctor).
Patient's can create Visits with preffered Doctor, and upload images as attachement's to current visit. Different role have specific permission's. Director (singleton) have permissions to see summary and statistics.


#### Current Status:
- Major design of REST API are completed. 
- There is 2 version of api ModelViewsSets and GenericView's
- Data are generated by FactoryBoy and loaded as fixtures
- Both Api Views, using Dynamic serializer's and specific Permission classes.
- In next step Doctor's Votes and Opinion's compared with nested Router will be added
- I have idea's to implement new features like visit callendar, Visit Data export to PDF, OAuth features..
- A this moment im developing classic Django View's (with templates).


#### Login accounts:
Admin - login: **admin**  password: **admin**

Patient - login: **user-patient-00**  password: **password1234** 

Doctor - login: **user-doctor-00**  password: **password1234**

Director - login: **user-director-00**  password: **password1234**


### Live Server Links:
Admin Site:  
- https://voitecp.eu.pythonanywhere.com/admin/

User Register Link:
- https://voitecp.eu.pythonanywhere.com/api/user/register/

Api Schema:
- https://voitecp.eu.pythonanywhere.com/api/schema/-ui/#/

Api Generic View's
- https://voitecp.eu.pythonanywhere.com/api/user/

Api Generic Views Set
- https://voitecp.eu.pythonanywhere.com/api-viewset/


### Docker:

<a href="https://hub.docker.com/r/voitecp/my-doctor/"><img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>

Pull Docker Image:
```
docker pull voitecp/my-doctor:latest
```
Run Image:
```
docker run -it -p 8000:8000 voitecp/my-doctor:latest /bin/bash -c "sh /usr/src/app/init.sh"

```
Open web browser and navigate to localhost address:  http://127.0.0.1:8000/ 


### How to Set up

Clone repository to custom folder (My-Doctor):
```
git clone https://github.com/VoitecP/My-Doctor.git
```
Poetry package is required. If you don't have, please install using this command:
```
pip install poetry
```
Change directory to My-Doctor:
```
cd My-Doctor
```
Set poetry global option, to use project folder as place to hold Virtual environment (recommended):
```
poetry config virtualenvs.in-project true
```
Create virtual environment, and install requirements:
```
poetry install
```
Copy file env-template to .env file using command:
```
# linux/mac
cp env-template .env

# windows
copy env-template .env
```
Start poetry virtual environment
```
poetry shell
```

Load fixtures to prepopulate Database, and run server

```
# linux/mac
./manage.py makemigrations
./manage.py migrate 
./manage.py db_fixtures
./manage.py runserver


# windows
python manage.py makemigrations
python manage.py migrate
python manage.py db_fixtures
python manage.py runserver
```


Open web browser and navigate to localhost address:  http://127.0.0.1:8000/ 

