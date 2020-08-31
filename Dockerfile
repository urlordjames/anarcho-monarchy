FROM python:3.7-slim

EXPOSE 8000

WORKDIR /root
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY static static
COPY anarchonet anarchonet
WORKDIR /root/anarchonet
COPY install.sh .
RUN chmod +x install.sh && ./install.sh
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "anarchonet.wsgi"]
