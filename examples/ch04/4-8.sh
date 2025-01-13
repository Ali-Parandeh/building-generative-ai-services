$ curl -X 'POST' \
  'http://127.0.0.1:8000/validation/failure' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "string",
  "model": "gpt-4o",
  "temperature": 0
}'

#{
#  "detail": [
#    {
#      "type": "literal_error",
#      "loc": [
#        "body",
#        "model"
#      ],
#      "msg": "Input should be 'tinyllama' or 'gemma2b'",
#      "input": "gpt-4o",
#      "ctx": {
#        "expected": "'tinyllama' or 'gemma2b'"
#      }
#    }
#  ]
#}