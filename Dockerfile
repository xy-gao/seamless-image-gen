FROM python:3.8
EXPOSE 8080
RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev
COPY seamless_image_gen ./seamless_image_gen
COPY checkpoints ./checkpoints
COPY requirements.txt ./requirements.txt
COPY app.py ./app.py
RUN pip install -r requirements.txt
ENV CHECKPOINTS_PATH=./checkpoints
CMD streamlit run app.py --server.port 8080