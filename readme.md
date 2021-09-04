# Carret Payments: A dummy assignment  

## How to run

**1. Environment set up**

Create virtual environment and activate it.

```bash
> python3 -m venv {environment_name}
> source env/bin/activate
> {environment_name}\Scripts\activate # Windows only! 
```

**2. Install dependencies**

```bash
> pip3 install -r requirements.txt
```

**3. Migrate changes to the database**

```bash
> python3 manage.py migrate
```

**4. Run the server**

```bash
> python3 manage.py runserver
```