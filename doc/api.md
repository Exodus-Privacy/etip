# REST API documentation

## API Endpoints

An API is available to help administrate the ETIP database.

### Authenticate

```sh
POST /api/get-auth-token/
```

Example:

```sh
curl -X POST http://localhost:8000/api/get-auth-token/ --data "username=admin&password=testtest"
```

You need to include your token as an `Authorization` header in all subsequent requests.

### Get the list of trackers

```sh
GET /api/trackers/
```

Example:

```sh
curl -X GET http://localhost:8000/api/trackers/ -H 'Authorization: Token <your-token>'
```

