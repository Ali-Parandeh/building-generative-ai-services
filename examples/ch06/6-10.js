async function stream(message, maxRetries = 3, initialDelay = 1000, backoffFactor = 2) {
    let delay = initialDelay;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            // Establish SSE connection here
            return
        } catch (error) {
            console.warn(`Failed to establish SSE connection: ${error}`);
            console.log(`Re-establishing connection - attempt number ${attempt + 1}`);
            if (attempt < maxRetries - 1) {
                await new Promise(resolve => setTimeout(resolve, delay));
                delay *= backoffFactor;
            } else {
                throw error
            }
        }
    }
}