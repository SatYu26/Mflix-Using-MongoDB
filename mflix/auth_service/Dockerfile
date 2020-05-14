FROM mflix_base

# Copy the current directory to "/auth_service/" directory in the container
COPY . /auth_service
# Specify the working directory as "/auth_service/"
WORKDIR /auth_service

# Set environment variables
ENV USER zianglu
ENV PASSWORD Zest2016!
ENV FLASK_SECRET_KEY auth-service-mongodb

ENTRYPOINT ["gunicorn", "-w", "9", "--worker-class", "gevent", "worker-connections", "1000", "-b", "0.0.0.0", "auth:app"]
