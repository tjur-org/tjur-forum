# tjur-forum
Forum software for tjur.org

## Instructions

### Running the forum

Run locally with `docker-compose run -p 8000:8000 --workdir /app/src app uvicorn --host 0.0.0.0 app:app`

### Adding a dependency

* Add the dependency to `reqs/requirements.in`
* Run `pip-compile --generate-hashes --strip-extras reqs/requirements.in > reqs/requirements.txt`
* Rebuild the image with `docker buildx bake runtime-test`

## Todo

- [ ] Implement all basic routes

Registering user, viewing list of threads, creating thread, replying...

- [ ] Set up Docker

- [ ] Set up nginx

- [ ] Set up postgres

- [ ] Design db schemas

- [ ] Create simple style.css
