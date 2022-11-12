"""
FLO satış v epazarlama faaliyetleri için roadmap belirlemekistemektedir.
Şirketin orta uzun vadeli plan yapabilmesi için var olan müşterilerin
gelecekte şirkete sağlayacakları potansiyel değerin tahmin edilmesi gerekmektedir.

"""

##############################################################
# Verinin Hazırlanması (Data Preperation)
##############################################################

# region install, import & read

# !pip install lifetimes
import datetime as dt
import pandas as pd
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

pd.set_option('display.max_column', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

df_ = pd.read_csv("/Users/apple/PycharmProjects/miuul/CRM_Analytics/FLO_CLTV_Prediction/flo_data_20k.csv")
df = df_.copy()
df.head()

# endregion

# region outlier_thresholds & replace_with_thresholds functions


def outlier_thresholds(dataframe, variable):
    quartile_1 = dataframe[variable].quantile(0.01)
    quartile_3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile_3 - quartile_1
    up_limit = round(quartile_3 + 1.5 * interquantile_range)
    low_limit = round(quartile_1 - 1.5 * interquantile_range)
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

# endregion

# region aykırı değerlerin baskılanması


df.describe().T

cols = ["order_num_total_ever_online", "order_num_total_ever_offline", "customer_value_total_ever_offline", "customer_value_total_ever_online"]
outliers = []
for col in cols:
    outliers.append(outlier_thresholds(df, col))

outliers

for col in cols:
    replace_with_thresholds(df, col)

df.describe().T

# [col.replace_with_thresholds() for col in df.columns if col == cols] olmadı tabiki

# endregion

# region TotalOrder & TotalPrice

df['TotalOrder'] = df['order_num_total_ever_online'] + df['order_num_total_ever_offline']
df['TotalPrice'] = df['customer_value_total_ever_online'] + df['customer_value_total_ever_offline']
df.columns

# endregion

# region to_datetime

df.info
# [pd.to_datetime(df[col]) for col in df.columns if 'date' in col]

for col in df.columns:
    if 'date' in col:
        df[col] = pd.to_datetime(df[col])
df.dtypes

# endregion

##############################################################
# CLTV Veri Yapısının Oluşturulması
##############################################################

#region analysis date

df['last_order_date'].max()
today_date = dt.datetime(2021, 6, 1)

# today_date =dt.datetime(df['last_order_date'].max()) neden olmuyor bu

# endregion

# region New DataFrame including customer_id, recency_cltv_weekly, T_we ekly, frequency and monetary_cltv_avg

cltv_df = pd.DataFrame()

df['recency'] = (df['last_order_date'] - df['first_order_date']).astype('timedelta64[D]')
df.head()

cltv_df = df.groupby('master_id').agg({'recency': lambda recency: int(recency),
                                       'first_order_date': lambda first_order_date: (today_date - first_order_date.min()).days,
                                       'TotalOrder': lambda TotalOrder: int(TotalOrder),
                                       'TotalPrice': lambda TotalPrice: TotalPrice})
cltv_df.head()
cltv_df.reset_index(inplace=True)

cltv_df.columns = ['customer_id', 'recency_cltv_weekly', 'T_weekly', 'frequency', 'monetary_cltv_avg']
cltv_df.head()

cltv_df['monetary_cltv_avg'] = cltv_df['monetary_cltv_avg'] / cltv_df['frequency']
cltv_df['recency_cltv_weekly'] = cltv_df['recency_cltv_weekly'] / 7
cltv_df['T_weekly'] = cltv_df['T_weekly'] / 7
cltv_df.head()
cltv_df.describe().T

# endregion

##############################################################
# BG/NBD, Gamma-Gamma Modellerinin Kurulması ve CLTV’nin Hesaplanması
##############################################################

# region Fitting BG/NBD model, Predicting exp_sales_3_month & exp_sales_6_month

bgf = BetaGeoFitter(penalizer_coef=0.001)

bgf.fit(cltv_df['frequency'],
        cltv_df['recency_cltv_weekly'],
        cltv_df['T_weekly'])

cltv_df["exp_sales_3_month"] = bgf.conditional_expected_number_of_purchases_up_to_time(4 * 3,
                                                                                    cltv_df['frequency'],
                                                                                    cltv_df['recency_cltv_weekly'],
                                                                                    cltv_df['T_weekly'])

cltv_df["exp_sales_6_month"] = bgf.conditional_expected_number_of_purchases_up_to_time(4 * 6,
                                                                                    cltv_df['frequency'],
                                                                                    cltv_df['recency_cltv_weekly'],
                                                                                    cltv_df['T_weekly'])

cltv_df.head()

# endregion

# region Fitting Gamma-Gamma model & Creating df['exp_average_value']

ggf = GammaGammaFitter(penalizer_coef=0.01)

ggf.fit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])

cltv_df['exp_average_value'] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                       cltv_df['monetary_cltv_avg'])
cltv_df.head()

# endregion

# region 6-month CLTV Prediction & Top 20 Customer

cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency_cltv_weekly'],
                                   cltv_df['T_weekly'],
                                   cltv_df['monetary_cltv_avg'],
                                   time=6,
                                   freq="W",
                                   discount_rate=0.01)

cltv.index = cltv_df["customer_id"]

cltv_final = cltv_df.merge(cltv, on="customer_id", how="left")
cltv_final.sort_values(by="clv", ascending=False).head(20)

# endregion

# region Segmentation Customers by 6-Month CLTV


cltv_final['segment'] = pd.qcut(cltv_final['clv'], 4, labels=["D", "C", "B", "A"])
cltv_final.sort_values(by="clv", ascending=False).head(10)

cltv_final.groupby('segment').agg({"count", "mean", "sum"})

# endregion

# region 6 aylık aksiyon önerileri

cltv_final.head()

cltv_final.sort_values(by="clv", ascending=False).head(50)

cltv_final.groupby("segment").agg(
    {"count", "mean", "sum"})

""" kısa yazmaya çalıştım bu yüzden analiz etmeye çalıştığım değerleri buraya detaylı eklemiyorum.

Segmentlere göre 6 aylık değerlere bakıldığında, en yüksek beklentinin(segment A) 1.5 birim olduğunu gözlemleriz.
Toplam kazanç açısından inceleyecek olursak CLV' nun 0.004' üne karşılık gelmektedir. Bu istenen bir sonuç gibi görünmüyor. En değerli ve ilgilenilmesi gereken
grubun daha yüksek getirileri olması beklenir 
Satış değerlerindeki ivmenin yükselmesi için ne tür çalışmalar yapılacağına karar vermek adına recency, monetary ve frequency
değerlerinin incelenmesi ve buna göre bir yol haritası belirlenmesi gerekiyor. Örneğin, satın alma sıklığı ile ilgili beklentinin
karşılanmadığı bir durum varsa bu konuda bir çalışma yapılması beklenirken, satışlardan beklenen karın elde edilmediği durumlarda ise farklı bir 
çalışma geliştirilmesi söz konusu olmalı.

A segmenti dışında, exp_average_value, exp_sales_3_month, exp_sales_6_month ve aslında diğer gözlemlerin de incelenmesi üzerine B ve C segmentlerinin
değerlerinin birbirlerine yakınlık gösterdiği düşünülebilir. Ayrı ayrı efor harcamaktansa bu iki segmenti birleştirerek bir politika uygulanması
daha karlı olmalı. 

A segmentinin davranışsal segmentasyona(yeni öğrendim) odaklanarak, sık görülen eğilimlerine ve davranışlarına, kullanılan ürünlerine, 
alışkanlıklarına eğilerek ve (BC) segmentinin değersel segmentasyonu(bunu da research ederken öğrendim ve yanlış kullanıyor olabilirim şu an) doğrultusunda, segmentlerine özgü ekonomik değerleri
göz önünde bulundurularak çeşitli teşfik araçlarının ve yöntemlerinin kullanılması tavsiyesini verebilirim. Aynı zamanda kısa anketler kullanılarak müşteri beklentileri
ve belki daha fazlası doğrudan müşterilerden gelen bilgi ile edinilebilir.


"""
