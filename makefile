# A template makefile that works for static websites.
# Need to export as ENV var
export TEMPLATE_DIR = templates
PTML_DIR = html_src
UTILS_DIR = utils
DOCKER_DIR = docker
REPO = coursebuilder

INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/logo.txt $(TEMPLATE_DIR)/menu.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $< 
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

local: $(HTMLFILES)

prod: $(INCS) $(HTMLFILES)
	-git commit -a 
	git pull origin master
	git push origin master

# real tests need to be written!
tests: FORCE
	ls

submods:
	git submodule foreach 'git pull origin master'

# dev container has dev tools
dev_container: $(DOCKER_DIR)/Dockerfile $(DOCKER_DIR)/requirements.txt $(DOCKER_DIR)/requirements-dev.txt
	docker build -t gcallah/$(REPO)-dev docker


# prod container has only what's needed to run
prod_container: $(DOCKER_DIR)/Deployable $(DOCKER_DIR)/requirements.txt
	docker system prune -f
	docker build -t gcallah/$(REPO) docker --no-cache --build-arg repo=$(REPO) -f $(DOCKER_DIR)/Deployable

deploy_container:
	docker push gcallah/$(REPO):latest
	
nocrud:
	rm *~
	rm .*swp
	rm $(PTML_DIR)/*~
	rm $(PTML_DIR)/.*swp

clean:
	touch $(PTML_DIR)/*.ptml; make local

