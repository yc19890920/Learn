	export GCLOUD_PROJECT = brickly-dev
	export GCLOUD_ZONE ?= us-west1-b
	export CONFIG_HOME ?= ${HOME}/cfg/dev/secret
	export CDB_CONFIG = "Replicas=3,Cpu=100m,Memory=500Mi,Storage=1Gi,StorageClass=pd-ssd"
	export K8S_CLUSTER := dev

	export MYSQL_STORAGE := 2Gi
	export MYSQL_MEMORY := 256Mi
	export MYSQL_CPU := 100m

	export MONGODB_STORAGE := 2Gi
	export MONGODB_MEMORY_REQUESTS := 256Mi
	export MONGODB_CPU_REQUESTS := 100m
	export MONGODB_MEMORY_LIMITS := 1024Mi
	export MONGODB_CPU_LIMITS := 500m

.PHONY: home
home:
	@echo ${HOME}
	 @echo $$HOME

.PHONY: clean
clean:
	rm -rf *.o

.PHONY: python-test
python-test:
	# python test.py
	@python test.py

.PHONY: env
env:
	@export foo=bar; echo "foo=[$$foo]"

.PHONY: a.txt
a.txt:b.txt c.txt
	cat b.txt c.txt > a.txt

source: file1 file2 file3
