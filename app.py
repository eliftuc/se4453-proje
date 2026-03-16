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

@app.route('/')
def index():
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
        conn.autocommit = True # Otomatik kaydetmeyi açıyoruz
        cur = conn.cursor()

        # 3. Tablo Oluşturma (Eğer yoksa)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS proje_ekibi (
                id SERIAL PRIMARY KEY,
                isim VARCHAR(50),
                gorev VARCHAR(100)
            );
        """)

        # 4. Tablo boşsa örnek veri ekleme
        cur.execute("SELECT COUNT(*) FROM proje_ekibi;")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO proje_ekibi (isim, gorev) VALUES ('Elif', 'Bulut Mimarı - VNET & Key Vault');")
            cur.execute("INSERT INTO proje_ekibi (isim, gorev) VALUES ('Grup 11', 'Konfigürasyon 8 Dağıtımı');")

        # 5. Verileri Okuma
        cur.execute("SELECT isim, gorev FROM proje_ekibi;")
        kayitlar = cur.fetchall()
        
        # 6. HTML Çıktısı Hazırlama
        tablo_html = "<table style='margin: 0 auto; border-collapse: collapse; width: 60%;'>"
        tablo_html += "<tr style='background-color: #0078d4; color: white;'><th style='padding: 10px; border: 1px solid #ddd;'>İsim</th><th style='padding: 10px; border: 1px solid #ddd;'>Görev (Rol)</th></tr>"
        
        for satir in kayitlar:
            tablo_html += f"<tr><td style='padding: 10px; border: 1px solid #ddd;'>{satir[0]}</td><td style='padding: 10px; border: 1px solid #ddd;'>{satir[1]}</td></tr>"
        tablo_html += "</table>"

        return f"""
        <body style='font-family:sans-serif; text-align:center; padding-top:50px; background-color:#f9f9f9;'>
            <h1 style='color:#0078d4;'>Tebrikler Elif! 🚀</h1>
            <p style='font-size:1.2em;'>Uygulaman şu an <b>Key Vault</b> üzerinden şifrelerini alıyor<br>
            ve <b>VNET Integration</b> ile kapalı ağdaki veritabanında işlem yapıyor.</p>
            <div style='background:white; padding:20px; border-radius:10px; display:inline-block; border: 1px solid #ccc; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom:20px;'>
                <b>Bağlantı Durumu:</b> ✅ Veritabanına Başarıyla Bağlanıldı!<br>
                <b>Tablo Durumu:</b> ✅ Veri Okuma/Yazma Başarılı!
            </div>
            <br>
            {tablo_html}
        </body>
        """

    except Exception as e:
        return f"<h1 style='color:red;'>Bağlantı Hatası! ❌</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run()
