response = TextModelResponse(content="FastAPI Generative AI Service", ip=None)
response.model_dump(exclude_none=True)

# {'content': 'FastAPI Generative AI Service',
#  'cost': 0.06,
#  'created_at': datetime.datetime(2024, 3, 7, 20, 42, 38, 729410),
#  'price': 0.01,
#  'request_id': 'a3f18d85dcb442baa887a505ae8d2cd7',
#  'tokens': 6}

response.model_dump_json(exclude_unset=True)
# '{"ip":null,"content":"FastAPI Generative AI Service","tokens":6,"cost":0.06}'
