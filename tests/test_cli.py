import asyncio
import httpx

API_URL = "http://localhost:8000/api/query"


async def test_connection():
    """Test if server is running"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:8000/api/health", timeout=5.0)
            if resp.status_code == 200:
                print("✅ Server is running!")
                return True
    except Exception as e:
        print(f"❌ Server not running: {e}")
        print("\nPlease start the server first:")
        print("uvicorn app.main:app --reload --port 8000")
        return False


async def main():
    # Check if server is running
    if not await test_connection():
        return

    print("\n🔍 Perplexity MVP - Ask anything!")
    print("-" * 50)

    while True:
        try:
            query = input("\n💭 Enter your query (or 'quit' to exit): ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            if not query:
                print("Please enter a valid query.")
                continue

            print(f"\n🔎 Searching for: '{query}'...")
            print("⏳ Please wait...")

            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(API_URL, json={"query": query})
                resp.raise_for_status()
                data = resp.json()

                print("\n" + "=" * 60)
                print("📝 ANSWER:")
                print("=" * 60)
                print(data["answer"])

                print("\n" + "=" * 60)
                print("📚 SOURCES:")
                print("=" * 60)
                for citation in data["citations"]:
                    print(f"  {citation}")
                print("=" * 60)

        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"❌ Request Error: {e}")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
