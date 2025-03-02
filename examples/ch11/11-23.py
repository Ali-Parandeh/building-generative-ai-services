import pytest


@pytest.mark.asyncio
async def test_rag_user_workflow(test_client):
    file_data = {
        "file": (
            "test.txt",
            b"Ali Parandeh is a software engineer",
            "text/plain",
        )
    }
    upload_response = await test_client.post("/upload", files=file_data)

    assert upload_response.status_code == 200

    generate_response = await test_client.post(
        "/generate", json={"query": "Who is Ali Parandeh?"}
    )

    assert generate_response.status_code == 200
    assert "software engineer" in generate_response.json()
