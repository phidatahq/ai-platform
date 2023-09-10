FROM phidata/superset:2.1.1

RUN pip install --upgrade pip

COPY workspace/prd/superset/config/superset_requirements.txt /
RUN pip install -r /superset_requirements.txt

COPY workspace/prd/superset/config/pythonpath /app/pythonpath/
