import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from fastapi import HTTPException

def execute_ml_task(request, df: pd.DataFrame):
    """
    Fungsi ini khusus untuk memproses rumus Machine Learning,
    tanpa perlu mengurus format API (API dipisah ke file router).
    """
    kesimpulan = ""
    model_yang_dipakai = ""
    hasil_output = None

    if request.task_type == "clustering":
        features = request.params.features
        n_clusters = request.params.n_clusters
        if not n_clusters: n_clusters = 3
            
        X = df[features]
        model = KMeans(n_clusters=n_clusters, random_state=42)
        df["hasil_klaster"] = model.fit_predict(X)
        kesimpulan = f"Memproses Clustering. Data berhasil dikelompokkan menjadi {n_clusters} klaster berdasarkan pola kemiripan."
        model_yang_dipakai = "Scikit-Learn K-Means"

    elif request.task_type == "association":
        min_support = request.params.min_support
        if not min_support: min_support = 0.2
            
        kolom_item = request.params.features[0]
        data_transaksi = df[kolom_item].tolist()

        te = TransactionEncoder()
        te_ary = te.fit(data_transaksi).transform(data_transaksi)
        df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

        frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)

        if frequent_itemsets.empty:
            aturan_final = []
            kesimpulan = f"Memproses Asosiasi. Tidak ditemukan pola keterkaitan dengan min_support {min_support}."
        else:
            rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
            aturan_final = []
            for _, row in rules.iterrows():
                sebab = ", ".join(list(row['antecedents']))
                akibat = ", ".join(list(row['consequents']))
                aturan_final.append({
                    "rule": f"{sebab} -> {akibat}",
                    "support": round(row['support'], 2),
                    "confidence": round(row['confidence'], 2)
                })
            kesimpulan = f"Memproses Asosiasi. Berhasil menemukan {len(aturan_final)} pola keterkaitan item."
        
        hasil_output = aturan_final
        model_yang_dipakai = "MLxtend Apriori"

    elif request.task_type == "classification":
        target = request.params.target_column
        features = request.params.features
        X = df[features]
        y = df[target]
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X, y)
        df[f"prediksi_{target}"] = model.predict(X)
        akurasi = model.score(X, y)
        kesimpulan = f"Memproses Klasifikasi. Model berhasil memprediksi kategori di kolom '{target}' dengan tingkat akurasi {akurasi:.2f}."
        model_yang_dipakai = "Scikit-Learn Decision Tree"

    elif request.task_type == "regression":
        target = request.params.target_column
        features = request.params.features
        X = df[features]
        y = df[target]
        model = LinearRegression()
        model.fit(X, y)
        df[f"prediksi_{target}"] = model.predict(X)
        akurasi = model.score(X, y)
        kesimpulan = f"Memproses Regresi. Model berhasil menemukan pola dengan tingkat akurasi {akurasi:.2f} (Skala 0-1)."
        model_yang_dipakai = "Scikit-Learn Linear Regression"

    else:
        raise HTTPException(status_code=400, detail="task_type tidak dikenali oleh sistem!")

    # Siapkan data kembalian
    data_untuk_dikembalikan = hasil_output if request.task_type == "association" else df.to_dict(orient="records")
    return data_untuk_dikembalikan, kesimpulan, model_yang_dipakai