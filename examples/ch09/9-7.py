@app.post("/generate/text")
@limiter.limit("5/minute")
def serve_text_to_text_controller(request: Request, ...):
    return ...


@app.post("/generate/image")
@limiter.limit("1/minute")
def serve_text_to_image_controller(request: Request, ...):
    return ...


@app.get("/health")
@limiter.exempt
def check_health_controller(request: Request, ...):
    return {"status": "healthy"}
