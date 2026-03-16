import os
from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import psycopg2

app = Flask(__name__)

# Key Vault Bağlantısı (Kendi vault adınla kontrol et)
KV_URL = "https://kv-se4453-elif.vault.azure.net/" 
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KV_URL, credential=credential)

# Ana sayfa (Burası sadece karşılama ekranı)
@app.route('/')
def index():
    return """
    <body style='font-family:sans-serif; text-align:center; padding-top:50px;'>
        <h1>Grup 11 - Azure Projesine Hoş Geldiniz!</h1>
        <p>Veritabanı bağlantı testi ve gereksinimler için lütfen <a href='/hello' style='color:#0078d4; font-weight:bold;'>/hello</a> uç noktasına (endpoint) gidiniz.</p>
    </body>
    """

# Kılavuzun istediği zorunlu /hello uç noktası
@app.route('/hello')
def hello():
    try:
        # 1. Key Vault'tan Sırları Çekiyoruz
        db_host = client.get_secret("DB-HOST").value
        db_user = client.get_secret("DB-USER").value
        db_pass = client.get_secret("DB-PASS").value
        
        # 2. PostgreSQL Bağlantısı
        conn = psycopg2.connect(
            host=db_host,
            database="postgres",
            user=db_user,
            password=db_pass,
            port=5432
        )
        
        # Bağlantıyı test edip kapatıyoruz (Tablo oluşturma kısımları silindi)
        conn.close()

        return """
        <body style='font-family:sans-serif; text-align:center; padding-top:50px; background-color:#f9f9f9;'>
            <h1 style='color:#0078d4;'>Hello Azure! 🚀</h1>
            <p style='font-size:1.2em;'>Bu uç nokta (endpoint) kılavuz gereksinimlerine uygun olarak <b>Key Vault</b> üzerinden şifrelerini alarak<br>
            <b>VNET Integration</b> ile kapalı ağdaki veritabanına bağlanmıştır.</p>
            <div style='background:white; padding:20px; border-radius:10px; display:inline-block; border: 1px solid #ccc; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom:20px;'>
                <b>Sır Yönetimi:</b> ✅ Key Vault'tan şifreler başarıyla çekildi!<br>
                <b>Bağlantı Durumu:</b> ✅ Veritabanına Başarıyla Bağlanıldı!
            </div>
        </body>
        """

    except Exception as e:
        return f"<h1 style='color:red;'>Bağlantı Hatası! ❌</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run()
