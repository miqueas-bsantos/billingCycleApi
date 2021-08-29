# deploy DEV
FROM python:3.7
MAINTAINER Miqueas Santos

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV STAGE='prod'
EXPOSE 80

COPY . /black-box-adyen-api-webhooks    
WORKDIR /black-box-adyen-api-webhooks
RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]