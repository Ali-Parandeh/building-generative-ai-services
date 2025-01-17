export model=google/gemma-2b
export volume=$PWD/data

docker run --gpus all --shm-size 1g -p 8080:80 -v "$volume":/data \
ghcr.io/huggingface/text-generation-inference:2.0.4 \
--model-id $model