FROM python:3.7-slim

EXPOSE 8000

WORKDIR /root
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
