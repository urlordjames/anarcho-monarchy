FROM python:3.7-slim

EXPOSE 8000

WORKDIR /root
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY static static
COPY anarchonet anarchonet
WORKDIR /root/anarchonet
COPY start.sh .
RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
