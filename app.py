import os
from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import psycopg2

app = Flask(__name__)

# Key Vault Connection (Azure SDK configuration)
KV_URL = "https://kv-se4453-elif.vault.azure.net/" 
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KV_URL, credential=credential)

@app.route('/')
def index():
    return """
    <body style='font-family:sans-serif; text-align:center; padding-top:50px; background-color:#fafafa;'>
        <h1 style='color:#252525;'>Grup 11 - Azure Projesi</h1>
        <h3 style='color:#757e8a;'>Sıla Barışık | Elif Tuc</h3>
        <p>Sistem doğrulama testi için lütfen <a href='/hello' style='color:#0078d4; font-weight:bold;'>/hello</a> uç noktasına gidiniz.</p>
    </body>
    """

@app.route('/hello')
def hello():
    try:
        # 1. Fetching Secrets from Key Vault (Secret Management Requirement)
        db_host = client.get_secret("DB-HOST").value
        db_user = client.get_secret("DB-USER").value
        db_pass = client.get_secret("DB-PASS").value
        
        # 2. Establishing PostgreSQL Connection (Private Network)
        conn = psycopg2.connect(
            host=db_host,
            database="postgres",
            user=db_user,
            password=db_pass,
            port=5432
        )
        
        # 3. Active Health Check: Querying Database Version
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()[0]
        cur.close()
        conn.close()

        return f"""
        <body style='font-family:sans-serif; text-align:center; padding-top:50px; background-color:#fafafa;'>
            <h1 style='color:#0078d4;'>Sistem Sağlık Kontrolü 🚀</h1>
            <div style='background:white; padding:30px; border-radius:15px; display:inline-block; border: 1px solid #e0e0e0; box-shadow: 0 10px 20px rgba(0,0,0,0.05);'>
                <p style='color:#2ecc71; font-weight:bold; font-size:1.2em;'>✅ Bağlantı Doğrulandı</p>
                <hr style='border:0; border-top:1px solid #eee; margin:20px 0;'>
                <div style='text-align:left; font-size:0.9em;'>
                    <p><b>Sır Yönetimi:</b> Key Vault Verileri Başarıyla Alındı</p>
                    <p><b>Veritabanı Durumu:</b> Özel Ağ (VNET) Üzerinden Bağlanıldı</p>
                    <p><b>Veritabanı Versiyonu:</b></p>
                    <code style='background:#f8f9fa; padding:10px; display:block; border-radius:5px; border:1px solid #eee;'>{db_version}</code>
                </div>
            </div>
            <p style='margin-top:20px; color:#666;'>Grup 11 - Güvenli Bulut Altyapısı v2.0</p>
        </body>
        """

    except Exception as e:
        # Error handling for unauthorized or external access (Professional message)
        return f"""
        <body style='font-family:sans-serif; text-align:center; padding-top:50px;'>
            <h1 style='color:#e74c3c;'>Erişim Engellendi! ❌</h1>
            <div style='background:#fdf2f2; border:1px solid #f5c6cb; padding:20px; display:inline-block; border-radius:10px;'>
                <p><b>Teknik Detay:</b> Bu uç noktaya sadece yetkili VNET üzerinden erişilebilir.</p>
                <p style='color:#721c24; font-size:0.8em;'>Hata Detayı: {str(e)}</p>
            </div>
        </body>
        """

if __name__ == "__main__":
    app.run()