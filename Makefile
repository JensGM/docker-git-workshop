shell:
	docker run \
		-it --privileged --pid=host \
		--mount type=bind,source=`pwd`/out,target=/out
		debian

run: all
	docker run \
		--mount type=bind,source=`pwd`/model,target=/model,readonly \
		--mount type=bind,source=`pwd`/out,target=/out \
		sima
