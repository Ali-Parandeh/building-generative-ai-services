@app.post("/generate/text")
@limiter.limit("10/minute", key_func=get_current_user)
def serve_text_to_text_controller(request: Request):
    return {"message": f"Hello User"}
