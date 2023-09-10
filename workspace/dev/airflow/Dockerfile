FROM phidata/airflow:2.7.1

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY workspace/dev/airflow/config/airflow_requirements.txt /
RUN pip install -r /airflow_requirements.txt

COPY workspace/dev/airflow/config/webserver_config.py ${AIRFLOW_HOME}/

# Install python3 kernel for jupyter
RUN ipython kernel install --name "python3"
