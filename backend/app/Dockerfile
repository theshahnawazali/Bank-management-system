FROM python:3.13.9

WORKDIR /backend/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD [ "fastapi", "run"]