
# Veriyi Anlama ve Hazırlama

# region import

"""
Adım1:

flo_data_20K.csv verisini okuyunuz.
Dataframe’in kopyasını oluşturunuz.

"""

import pandas as pd
import datetime as dt

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df_ = pd.read_csv("/Users/apple/PycharmProjects/miuul/CRM_Analytics/FLO_Customer_Segmentation/flo_data_20k.csv")

df = df_.copy()
df.head()

# endregion

# region Veri Seti İncelemesi

"""
Adım2 :    Veri setinde
           a. İlk 10 gözlem,
           b. Değişken isimleri,
           c. Betimsel istatistik,
           d. Boşdeğer,
           e. Değişken tipleri,incelemesi yapınız.
"""

df.head(10)
df.columns
df.shape
df.isnull().sum()
df["master_id"].dtype
df["order_channel"].dtype
df["last_order_channel"].dtype
df["first_order_date"].dtype
df["last_order_date"].dtype
df["last_order_date_online"].dtype
df["last_order_date_offline"].dtype
df["order_num_total_ever_online"].dtype
df["order_num_total_ever_offline"].dtype
df["customer_value_total_ever_offline"].dtype

# endregion

# region TotalOrder & TotalPrice Değerlerinin Oluşturulması

"""
Adım3 : 

Omnichannel müşterilerin hem online'dan hemde offline platformlardan 
alışveriş yaptığını ifade etmektedir. Her bir müşterinin toplam 
alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.

"""
df["TotalOrder"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["TotalPrice"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

# endregion

# region Değişkenlerin Tipini Date'e Çevirme

"""
Adım4 :  

Değişken tiplerini inceleyiniz. 
Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
"""

# region 1. yol (Loser Way)
df["first_order_date"] = pd.to_datetime(df["first_order_date"])
df["last_order_date"] = pd.to_datetime(df["last_order_date"])
df["last_order_date_online"] = pd.to_datetime(df["last_order_date_online"])
df["last_order_date_offline"] = pd.to_datetime(df["last_order_date_offline"])
df["first_order_date"].dtype
df["last_order_date"].dtype
df["last_order_date_online"].dtype
df["last_order_date_offline"].dtype
# endregion

# region 2. yol
to_date_format = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
df[to_date_format] = df[to_date_format].apply(pd.to_datetime)
# endregion

# 3. yol
# to_time_format = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
# df[to_time_format] = pd.to_datetime(df[to_time_format])

# 4. yol (if not string)
# df['first_order_date'] = df['first_order_date'].apply(lambda x: dt.datetime.strptime(x,'%d%b%Y:%H:%M:%S.%f'))

# endregion

# region Veriyi İnceleme
"""
Adım5:  

Alışveriş kanallarındaki müşteri sayısının, 
toplam alınan ürün sayısının ve toplam harcamaların dağılımına bakınız.

"""

df.groupby("order_channel").agg({"TotalOrder": "sum",
                                 "TotalPrice": "sum",
                                 "master_id": "nunique"})

"""
Adım6:  

En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.

"""

df = df.sort_values(by="TotalPrice", ascending=False)
# df.groupby("master_id")["TotalPrice"].head(10)

"""
Adım7 :  

En fazla siparişi veren ilk 10 müşteriyi sıralayınız.

"""

df = df.sort_values(by="TotalOrder", ascending=False)
# df.groupby("master_id")["TotalOrder"].head(10)

# endregion  #

# region Veri Ön Hazırlık Süreci Fonksiyonu

"""
Adım8 :  
Veri ön hazırlık sürecini fonksiyonlaştırınız.

"""


def Data_Preparing(df, csv=False):

    # importingz

    import pandas as pd
    import datetime as dt
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 500)
    df_ = pd.read_csv("/Users/apple/PycharmProjects/miuul/CRM_Analytics/FLO_Customer_Segmentation/flo_data_20k.csv")

    df = df_.copy()
    df.head()

    # Veri Seti İncelemesi

    df.head(10)
    df.columns
    df.shape
    df.isnull().sum()
    df["master_id"].dtype
    df["order_channel"].dtype
    df["last_order_channel"].dtype
    df["first_order_date"].dtype
    df["last_order_date"].dtype
    df["last_order_date_online"].dtype
    df["last_order_date_offline"].dtype
    df["order_num_total_ever_online"].dtype
    df["order_num_total_ever_offline"].dtype
    df["customer_value_total_ever_offline"].dtype

    # Total Order & Total Price for Each Customer

    df["TotalOrder"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["TotalPrice"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

    # to date type

    to_date_format = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
    df[to_date_format] = df[to_date_format].apply(pd.to_datetime)

    # TotalOrder, TotalPrice, num. of master_id according to order_channel

    df.groupby("order_channel").agg({"TotalOrder": "sum",
                                     "TotalPrice": "sum",
                                     "master_id": "nunique"})

    # top 10 Customers have max. TotalPrice

    df = df.sort_values(by="TotalPrice", ascending=False)
    df.groupby("master_id")["TotalPrice"].head(10)

    # top 10 Customers have max. TotalOrder

    df = df.sort_values(by="TotalOrder", ascending=False)
    df.groupby("master_id")["TotalOrder"].head(10)

    if csv:
        rfm.to_csv("rfm.csv")

    return df


df = df_.copy()
Data_Preparing(df)


# endregion

#  region RFM Metriklerinin Hesaplanması

df.head()

# Analiz Tarihi Oluşturma

df["last_order_date"].max()  # Timestamp('2021-05-30 00:00:00') Analiz için seçeceğimiz tarih : 2021-06-02
today_date = dt.datetime(2021,6,2)
type(today_date)  # Out[29]: datetime.datetime  : zaman formunda bir değişken tipi


# RFM Analizi

rfm = df.groupby("master_id").agg({'last_order_date': lambda last_order_date: (today_date - last_order_date.max()).days,
                                   'TotalOrder': lambda TotalOrder: TotalOrder.sum(),
                                   'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.head()
rfm.columns = ['recency', 'frequency', 'monetary']
rfm.describe().T

# endregion

# region RF Skorunun Hesaplanması

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method = "first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm["RF_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))

# endregion

# region RF Skorunun Segment Olarak Tanımlanması

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

# endregion

# Görev 5

rfm.groupby("segment").agg({"recency": "mean",
                            "frequency": "mean",
                            "monetary": "mean"})

# region segmentation part a

# champions|loyal_customers interested in Cat. Women
champs_royals_wom = rfm[rfm['segment'].str.contains('champions|loyal_customers')]
champs_royals_wom.reset_index(inplace=True)

champs_royals_wom = df[['master_id', 'interested_in_categories_12']].merge(right=champs_royals_wom, on='master_id', how='right')

champs_royals_wom = champs_royals_wom[champs_royals_wom['interested_in_categories_12'].str.contains('KADIN')]

# endregion

# region to csv.
df_MasterIDs = pd.DataFrame()
df_MasterIDs["MasterIDs"] = champs_royals_wom["master_id"].values

df_MasterIDs.to_csv("MasterIDs.csv")

# endregion

# region segmentation part b

# cant_loose|hibernating|new_customers interested in Cat. Man and Children

new_segments = rfm[rfm['segment'].str.contains('cant_loose|hibernating|new_customers')]
new_segments.reset_index(inplace=True)

new_segments = df[['master_id', 'interested_in_categories_12']].merge(right=new_segments, on='master_id', how='right')
new_segments = new_segments[new_segments['interested_in_categories_12'].str.contains('ERKEK|COCUK')]


# endregion

# region to csv.

discount_segmentation = pd.DataFrame()
discount_segmentation["CustomerIDs"] = new_segments["master_id"].values

discount_segmentation.to_csv("CustomerIDs.csv")

# endregion