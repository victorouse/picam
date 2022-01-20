
.PHONY: push
push:
	@echo "Pushing to target"
	./scripts/run.sh copy_to_pi

.PHONY: pull
pull:
	@echo "Pulling from target"
	./scripts/run.sh copy_from_pi

.PHONY: run
run:
	@echo "Running"
	./scripts/run.sh run

.PHONY: shell
shell:
	@echo "Running"
	./scripts/run.sh shell
