<h1>
	Welcome to Project Colaborar
</h1>
<hr>
<p>
Project Colaborar is the project mamagement web application for your organization. This web application will help the project managers to manage the engineers for the project. The project manager can create as many projects as he wants and invite as many engineers, same engineer can also work in different projects. The engineer or project manager can make queues(task to be done) which can be picked by any other engineer or by themselves. Stay Tuned for more info..... 
</p>
<br>
<h3> Project Setup </h3>
<ol>
<li>Setup the virtual environment for the project (Make sure that the python path is set for Python3).</li>
<li>Install the requirements <b>pip install -r requirements.txt</b></li>
<li>Setup the database (PostgreSQL) with <b>database name="django_todo", user="django_todo_user" and password="demo1234"</b></li>
<li>Generate the migrations <b> python manage.py makemigrations todo</b></li>
<li>Run the migrations <b> python manage.py migrate </b> </li>
<li>Create SuperUser <b>python manage.py createsuperuser </b> </li>
<li>Run the server <b>python manage.py runserver </b> </li>
</ol>
<h4>Note</h4>If you any problem in running the project, feel free to drop a mail at pranav@codingmart.com
