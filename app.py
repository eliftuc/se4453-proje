import os
from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import psycopg2

app = Flask(__name__)

# 1. Key Vault Bağlantısı
KV_URL = "https://kv-se4453-elif.vault.azure.net/" 
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KV_URL, credential=credential)

@app.route('/')
def index():
    try:
        # 2. Key Vault'tan Sırları Çekiyoruz
        db_host = client.get_secret("DB-HOST").value
        db_user = client.get_secret("DB-USER").value
        db_pass = client.get_secret("DB-PASS").value
        
        # 3. PostgreSQL Bağlantısı
        conn = psycopg2.connect(
            host=db_host,
            database="postgres",
            user=db_user,
            password=db_pass,
            port=5432
        )
        
        return """
        <body style='font-family:sans-serif; text-align:center; padding-top:50px;'>
            <h1 style='color:#0078d4;'>Tebrikler! 🚀</h1>
            <p style='font-size:1.2em;'>Uygulaman şu an <b>Key Vault</b> üzerinden şifrelerini alıyor<br>
            ve <b>VNET Integration</b> ile veritabanına kapalı ağdan bağlanıyor.</p>
            <div style='background:#e1f5fe; padding:20px; border-radius:10px; display:inline-block; border: 1px solid #0078d4;'>
                <b>Bağlantı Durumu:</b> ✅ Veritabanına Başarıyla Bağlanıldı!
            </div>
        </body>
        """
    except Exception as e:
        return f"<h1 style='color:red;'>Bağlantı Hatası! ❌</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run()
