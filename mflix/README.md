# Mflix Project

## Project Environment Setup

Follow the course environment setup in `../README.md`

In `env.sh`, we defined the necessary environmental variables for this project. Make sure to replace the `MFLIX_DB_URI` environmental variable with your own MongoDB Atlas connection URI.

<br>

## Importing Project Data to MongoDB Atlas

1. Make sure your MongoDB Atlas cluster is up and running

2. Download the data from Amazon S3 `mflix-data` bucket, and put it under the root directory of the project

   *i.e., All the data compression files should be under `data/dump/data/`*

3. Then, simply do

   ```bash
   $ ./init.sh
   ```

   which will restore the dumped data back into the DB cluster.

<br>

## Tech Stack (Implementation Notes)

#### Implementation with RESTful Architecture (Microservices)

<img src="https://github.com/Ziang-Lu/Intro-to-MongoDB/blob/master/mflix/Mflix%20RESTful%20Architecture.png?raw=true">

We separate `auth_service` and `movie_service` out as Flask-based web services:

* `auth_service` is responsible for user registeration and user authentication issues, and talks to `MongoDB` directly.

  Defined resources:

  * `UserList`

    Route: `/users`

    | Method | Description                                                | Request Form Schema                               | Reponse Status Code                                          |
    | ------ | ---------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------ |
    | GET    | Returns the user with a specified email                    | <u>Query</u>:<br>`email`: string                  | 200 on success, 400 on no email provided, 404 on user not found |
    | POST   | Adds a user with the given name, email and hashed password | `name`: string<br>`email`: string<br>`pw`: string | 201 on success, 400 on invalid data provided                 |

  * `UserAuth`

    Route: `/user-auth`
    
    | Method | Description                 | Request Form Data                                         | Response Status Code                                         |
    | ------ | --------------------------- | --------------------------------------------------------- | ------------------------------------------------------------ |
    | GET    | Handles user authentication | <u>Query:</u><br>`email`: string<br>JSON:<br>`pw`: string | 200 on success, 400 on no email provided, 404 on user not found, 401 on authentication failed |

* `movie_service` is responsible for all the information related to movies and movie comments, and talks to `MongoDB` directly.

  Defined resources:

  * `MovieList`

    Route: `/movies`

    | Method | Description            | Request Form Schema | Reponse Status Code |
    | ------ | ---------------------- | ------------------- | ------------------- |
    | GET    | Returns all the movies |                     | 200 on success      |

  * `MovieItem`

    Route: `/movie/<id>`

    | Method | Description                         | Request Form Schema | Reponse Status Code                                          |
    | ------ | ----------------------------------- | ------------------- | ------------------------------------------------------------ |
    | GET    | Returns the movie with the given ID |                     | 200 on success, 400 on invalid movie ID, 404 on movie not found |

  * `MovieGenreList`

    Route: `/movie-genres`

    | Method | Description                  | Request Form Schema | Reponse Status Code |
    | ------ | ---------------------------- | ------------------- | ------------------- |
    | GET    | Returns all the movie genres |                     | 200 on success      |

  * `MovieComments`

    Route: `/movie/<movie_id>/comments`

    | Method | Description                                                  | Request Form Schema                                          | Reponse Status Code                                          |
    | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | GET    | Returns all the comment of the given movie, from most-recent to least-recent |                                                              | 200 on success, 400 on invalid movie ID                      |
    | POST   | Adds a comment to the given movie                            | `movie_id`: string<br>`user`: dict<br>`text`: string<br>`date`: string | 201 on success, 404 on movie not found, 400 on invalid data provided |

  * `MovieComment`

    Route: `/movie/<movie_id>/comments/<comment_id>`

    | Method | Description                                    | Request Form Schema | Reponse Status Code |
    | ------ | ---------------------------------------------- | ------------------- | ------------------- |
    | DELETE | Deletes the given comment from the given movie |                     | 204 on success      |

***

**RESTful Web Service Implementation Details**

* `Marshmallow/Flask-Marshmallow` is used for schema definition & deserialization (including validation) / serialization.

***

The communication between the main Mflix app and the web services is through RESTful API, via `JSON`.

<br>

In this way, the original Mflix app now becomes a "skeleton" or a "gateway", which talks to `auth_service` and `movie_service`, uses the fetched data to render HTML templates.

***

*REST架构中要求client-server的communication应该是"无状态"的, 即一个request中必须包含server (service)处理该request的全部信息, 而在server-side不应保存任何与client-side有关的信息, 即server-side不应保存任何与某个client-side关联的session.*

*=> 然而, 我们应该区分"resource state"和"application state": REST要求的无状态应该是对resource的处理无状态, 然而在main application本身里面我们需要保存应用状态, 即user的login和session等.*

***

Thus, in the original Mflix app, we still use `Flask-Login` to handle user log-in/log-out and authentication issues, as well as session management.

<br>

**Run the application**

```bash
# Build the base image
$ docker build -t mflix_base ./

# Build all the images (main application and web services)
$ docker-compose build

$ docker-compose up
```

Then simply go to http://localhost:8000

