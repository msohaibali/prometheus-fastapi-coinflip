FROM python:3.9.18-slim-bullseye

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 1010

ENTRYPOINT [ "python", "app.py" ]