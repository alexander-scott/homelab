# url_shortener

### Core components

- [ ] A REST API (or web portal) allowing anyone to:
  - [x] Create a user-specified short link from a long one
  - [ ] Create a generated short link from a long one
- [x] A persistent database storing this information
- [x] A http redirect service that is applied when someone goes to a valid short link

### Deployment

- [ ] Dockerimage
- [ ] Docker-compose with nginx reverse proxy
- [ ] K8s with traefik reverse proxy

### Advanced components

- [ ] Short URL Collision avoidance
- [ ] Analytics for the number of visits
- [ ] Unit Tests
- [ ] Load/performance tests
- [ ] Scaling or sharding/partitioning
