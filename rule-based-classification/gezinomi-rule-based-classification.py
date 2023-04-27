import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', None)

# Görev 1: Aşağıdaki soruları yanıtlayın
print("hello")
# Soru 1 :  miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz..
df = pd.read_excel("miuul_gezinomi.xlsx")
df.head()
df.shape
df.info()
df.isnull().sum()
df.describe().T

# Soru 2: Kaç unique şehir vardır? Frekansları nedir?
df["SaleCityName"].unique()
df["SaleCityName"].value_counts()
# Soru 3: Kaç unique Concept vardır?
df["ConceptName"].unique()
# Soru 4: Hangi Concept’den kaçar tane satışgerçekleşmiş?
df.groupby("ConceptName").agg({"SaleId": "count"}) # İkinci yol
df["ConceptName"].value_counts() # Birinci yol
# Soru 5: Şehirlere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("SaleCityName").agg({"Price": "sum"})
# Soru 6: Concept türlerine göre göre ne kadar kazanılmış?
df.groupby("ConceptName").agg({"Price": "sum"}) # Konsepte göre toplam kazanç
# Soru 7: Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName").agg({"Price": "mean"})
# Soru 8: Conceptlere  göre PRICE ortalamaları nedir?
df.groupby(['ConceptName']).agg({"Price": "mean"})
# Soru 9: Şehir konsept kırılımında price ortalamaları nedir
df.groupby(["SaleCityName", "ConceptName"]).agg({"Price": "mean"})

# GÖREV 2: SaleCheckInDayDiff değişkenini EB_Score adında yeni bir kategorik değişkene çeviriniz.

df["SaleCheckInDayDiff"].max()

bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = ["Last Minuters", "Potential Planners", "Planner", "Early Bookers"]


df["EB_score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)
df.head()

# Şehir-Concept-EB Score, Şehir-Concept- Sezon, Şehir-Concept-CInDay kırılımında
# ortalama ödenen ücret ve yapılan işlem sayısı cinsinden 
# inceleyiniz ?

df.groupby(["SaleCityName", "ConceptName", "EB_score"]).agg({"Price": ["mean", "count"]})
df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]})
df.groupby(["SaleCityName", "ConceptName", "CheckInDate"]).agg({"Price": ["mean", "count"]})

# Görev 4:  City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.

agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]}).sort_values(("Price", "mean"), ascending=False)

# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.

agg_df.reset_index(inplace=True)

# Görev 5:  Yeni seviye tabanlı müşterileri (persona) tanımlayınız.

# Basit 1. yol:
agg_df["sale_level_based"] = agg_df["SaleCityName"] + '_' + agg_df["ConceptName"] + '_' + ["Seasons"]

# Daha fonksiyonel olan ikinci yol:
agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis=1)

# Görev 6:  Yeni müşterileri (personaları) segmentlere ayırınız.
# •Yeni personaları PRICE’a göre 4 segmente ayırınız.
# •Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})

# Görev 7: Oluşan son df'i price değişkenine göre sıralayınız.
agg_df.sort_values(by="Price")

# Modele Soru: "ANTALYA_HERŞEY DAHIL_HIGH" hangi segmenttedir ve ne kadar ücret beklenmektedir?

new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new_user]



