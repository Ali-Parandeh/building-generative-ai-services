python -m vllm.entrypoints.openai.api_server \
--model "TinyLlama/TinyLlama-1.1B-Chat-v1.0" \
--dtype float16 \
--tensor-parallel-size 4 \
--api-key "your_secret_token"