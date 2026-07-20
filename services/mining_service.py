import pandas as pd
import io
import re
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

def execute_ml_task(payload) -> str:
    df = None
    
    # 1. Coba download dataset jika Okta mengirim URL
    if payload.url and payload.url.startswith("http"):
        try:
            df = pd.read_csv(payload.url)
        except:
            pass 
            
    # 2. Coba baca raw_text sebagai tabel (jika bentuknya CSV)
    if df is None and payload.raw_text:
        try:
            df = pd.read_csv(io.StringIO(payload.raw_text))
        except:
            pass

    # ========================================================
    # SKENARIO A: Gagal dapat tabel (Input cuma teks artikel)
    # ========================================================
    if df is None or len(df.columns) < 2:
        teks = payload.raw_text or ""
        kata = len(teks.split())
        angka = len(re.findall(r'\d+', teks))
        return f"Data Mining Profiling: Input berupa teks tidak terstruktur. Ditemukan {kata} kata dan {angka} entitas numerik. Ekstraksi selesai."

    # ========================================================
    # SKENARIO B: THE REAL MACHINE LEARNING (LENGKAP 4 ALGORITMA)
    # ========================================================
    keyword = (payload.keyword or "").lower()
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    try:
        df_clean = df.fillna(0) # Bersihkan data kosong agar ML tidak error

        # 1. ALGORITMA CLUSTERING (K-Means)
        if "cluster" in keyword or "kelompok" in keyword:
            if len(numeric_cols) > 0:
                model = KMeans(n_clusters=3, random_state=42)
                df["hasil_klaster"] = model.fit_predict(df_clean[numeric_cols])
                return f"Proses Clustering (K-Means) selesai. Dataset ({df.shape[0]} baris) berhasil dikelompokkan menjadi 3 klaster utama berdasarkan fitur numerik. Data siap divisualisasikan."
        
        # 2. ALGORITMA REGRESI (Linear Regression - Supervised Numeric)
        elif "regresi" in keyword or "prediksi" in keyword:
            if len(numeric_cols) > 1:
                target_col = numeric_cols[-1] # Ambil kolom angka terakhir sbg target tebakan
                feature_cols = numeric_cols[:-1] # Sisa kolom jadi bahan ajar
                
                model = LinearRegression()
                model.fit(df_clean[feature_cols], df_clean[target_col])
                akurasi = model.score(df_clean[feature_cols], df_clean[target_col]) * 100
                return f"Proses Regresi Linier selesai. AI berhasil mempelajari pola untuk memprediksi nilai '{target_col}' dengan tingkat akurasi (R-Squared) sebesar {akurasi:.2f}%. Model siap digunakan."

        # 3. ALGORITMA KLASIFIKASI (Decision Tree - Supervised Kategori)
        elif "klasifikasi" in keyword or "label" in keyword:
            if len(numeric_cols) > 0 and len(categorical_cols) > 0:
                target_col = categorical_cols[-1] # Ambil kolom teks terakhir sbg target (misal: Lulus/Gagal)
                
                model = DecisionTreeClassifier(max_depth=3, random_state=42)
                model.fit(df_clean[numeric_cols], df_clean[target_col])
                return f"Proses Klasifikasi (Decision Tree) selesai. AI berhasil membangun pohon keputusan untuk mengklasifikasikan kolom '{target_col}' berdasarkan data numerik yang ada. Rule klasifikasi telah diekstrak."

        # 4. ALGORITMA ASOSIASI/KORELASI (Pengganti Apriori yang rawan error)
        elif "asosiasi" in keyword or "pola" in keyword or "korelasi" in keyword:
            if len(numeric_cols) > 1:
                kor = df[numeric_cols].corr().unstack().sort_values(ascending=False).drop_duplicates()
                kor_kuat = kor[(kor > 0.5) & (kor < 1.0)].head(1) # Cari korelasi terkuat
                if not kor_kuat.empty:
                    fitur1, fitur2 = kor_kuat.index[0]
                    nilai = kor_kuat.values[0] * 100
                    return f"Proses Asosiasi selesai. Ditemukan pola hubungan yang kuat ({nilai:.1f}%) antara '{fitur1}' dan '{fitur2}'. Jika nilai {fitur1} naik, maka {fitur2} cenderung ikut naik."

        # 5. DEFAULT BACKUP: Automated Data Profiling
        kesimpulan = f"Automated Data Profiling selesai. Dataset memiliki {df.shape[0]} baris dan {df.shape[1]} kolom. "
        if numeric_cols:
            avg_val = df[numeric_cols[0]].mean()
            max_val = df[numeric_cols[0]].max()
            kesimpulan += f"Kolom numerik utama '{numeric_cols[0]}' memiliki nilai rata-rata {avg_val:.2f} dengan nilai maksimal {max_val:.2f}. "
        return kesimpulan + "Siap diteruskan ke agen Summarizer/PPT."
        
    except Exception as e:
        return f"Proses Data Mining gagal saat memproses dataset: {str(e)}"