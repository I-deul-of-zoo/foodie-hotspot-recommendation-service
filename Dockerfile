# Use an official lightweight Python image based on Debian Slim
FROM python:3.11.6-slim

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1
# Set the working directory to /app
WORKDIR /app

# Install system dependencies
# pkg-config: mysqlclient 못찾아서 추가
# default-libmysqlclient-dev mysql연결 가능한 패키지 설치 추가
# python3 -m pip install --upgrade pip : pip 업그레이드
# 나머지는 기본적으로 있었습니다.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev libpq-dev default-libmysqlclient-dev pkg-config\
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install --upgrade pip \
    && pip install poetry

# Copy only the requirements file to optimize caching
COPY poetry.lock pyproject.toml /app/

# Copy the current directory contents into the container at /app
COPY . /app/
# COPY docker-entrypoint.sh /app/

# Install project dependencies
RUN poetry install --no-root

# Make port 8000 available to the world outside this container
EXPOSE 8000
# RUN chmod a+x /app/docker-entrypoint.sh
# Run app.py when the container launches
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# ENTRYPOINT [ "/app/docker-entrypoint.sh" ]