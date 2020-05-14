FROM mflix_base

# Copy the current directory to "/movie_service/" directory in the container
COPY . /movie_service
# Specify the working directory as "/movie_service/"
WORKDIR /movie_service

# Set environment variables
ENV USER zianglu
ENV PASSWORD Zest2016!
ENV FLASK_SECRET_KEY movie-service-mongodb

ENTRYPOINT ["gunicorn", "-w", "9", "--worker-class", "gevent", "worker-connections", "1000", "-b", "0.0.0.0", "movie_service:app"]
