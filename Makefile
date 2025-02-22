VERSION=1.0.1

build:
	docker build -t cuongnb14/web2md:$(VERSION) .

push:
	docker push cuongnb14/web2md:$(VERSION)
