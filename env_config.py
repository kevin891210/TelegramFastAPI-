import os

API_ID = int(os.getenv("TG_API_ID", "27129567"))
API_HASH = os.getenv("TG_API_HASH", "843b2878d3d02fad55de7043516d3e56")
TG_SESSION = os.getenv("TG_SESSION", "1BVtsOL8Bu0otQr5YJksb_3Y3-TvrWpuYsJ26m-e_qn1heUHNphguoIrMyRS2YJ1BmblSj1rLo_Om5-B4jF2vImpMuXJctTSf-aKIMmaYxqQ7OQLOTmHS3xX5n0eLDZDDz0RXKwjs8p02eMMt4Fy3jtGlR84HPUqNPUq4hH4ValLrNIybFFN1m4KgOZM6Cvevi-dpqBdRhw1y4J_v0EsHvPxV55_HmB23m9jZ267H9D6Rqxhp4_VFPPc2MxhBXp63EWzcwQJjfEnk11uTfatGLrFm9H9j4IOy6SIbvGhb8PB5Uun0B7tByGJkeYdyVzpL42E8KhGg6m1-zj8tyqGUKJfZk7qFeQA=")  # leave empty for first run
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://yhchen.zeabur.app/webhook/f18d6766-9d10-4c79-90a0-41123cb9f7f5")
API_AUTH_TOKEN = os.getenv("API_AUTH_TOKEN", "CHANGE_ME")

LISTEN_HOST = os.getenv("HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("PORT", "8000"))
