"""

--Müşteri Yaşam Boyu Değeri(Customer Lifetime Value) :

  Bir müşterinin  bir şirketle kurduğu ilişki-iletişim süresince,
  bu şirkete kazandıracağı parasal değerdir.

--Bu Neden Önemlidir ?

  Müşterilerimizin gelecekte bile bize sağlayacak olduğu faydayı,
  eğer belirleyebilirsek, buna göre hem onlarla olan ilişkimizi düzenleyebilir,
  hem de şirketimizde orta-uzun vadeli daha müşteri odaklı, katma değer odaklı bir
  yaklaşım sergileyebiliriz.
  Bu aynı zamanda, pazarlama faaliyetleri için ayrılacak bütçelerin belirlenmesinde
  bir rol oynayabilecektir.
  Bunun sebesi, elimizdeki mevcut müşterilerin lifetime value'larını hesaplayabilirsek,
  bu durumda bir diğer kaygımız olan yeni müşteri bulma çabasının da maliyetlerini
  birimleştirebilirsek, bu durumda var olanlar ile yenilerini bulmak arasındaki
  teoride sıkça duyduğumuz fakat pratikte uygulanması biraz daha problemli olabilen
  bu konuya dair de bir bilgi edinmiş oluruz.

  -- Nasıl Hesaplanır?

     Kafa karıştırıcı derecede fazla Customer Lifetime Value hesaplama yöntemi vardır.
     En başta ifade edilmesi gereken şey, CLTV değerini hesaplamak ve tahmin etmek farklı şeylerdir.

     Temel Fomül          : satın alma başına ortalama kazanç * satın alma sayısı
                            Customer Value = Average Order Value * Purchase Frequency


     CLTV                 = (Customer Value / Churn Rate) * Profit Margin

     Customer Value       = Average Order Value * Purchase Frequency

     Churn Rate           : Müşteri terk oranı sabiti
                            (1 - Repeat Rate) ile hesaplanır.

     Repeat Rate:         : Birden fazla alışveriş yapan müşteri sayısı / Tüm müşteriler
                            (Tekrar Oranı)
                            (Retention Rate)
                            (Elde Tutma Oranı)
                            (Retention Rate)


     Profit Margin        : Şirketin müşteriler ile yaptığı alışverişlerde varsayacağı kar miktarı.
                            Kişilerin şirkete bıraktığı gelir ile bu kar marjı çarpıldığında,
                            Profit Margin ortaya çıkar.

     Average Order Value  : Total Price / Total Transaction

     Pruechase Frequency  : Total Transaction per Customer / Total Number of Customers
                            Bu işlem tüm müşteriler için yapılacak olduğundan, aslında
                            bütün müşteriler çaısından Total Transaction değeri
                            ölçeklendirilmiş olur.
                            Bütün bir kitlenin etkisini, göz önünde bulundurmaya çalışmanın bir yoludur.
                            Basit bir bölme işlemi ile gerçekleştirilir.


    Profit Margin         : Total Price per Customer * kar miktarı
                            (Karlılık Oranı)

-- Sonuç olarak, her bir müşteri için hesaplanacak olan CLTV değerlerine göre bir sıralama yapıldığında
   ve CLTV değerlerine göre belirli noktalardan bölme işlemi yapılarak gruplar oluşturulduğunda
   müşterilerimiz segmentlere ayrılmış olacaktır.

# CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri)

# 1. Veri Hazırlama
# 2. Average Order Value (average_order_value = total_price / total_transaction)
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
# 5. Profit Margin (profit_margin =  total_price * 0.10)
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
# 8. Segmentlerin Oluşturulması
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması

"""

##################################################
# 1. Veri Hazırlama
##################################################

"""
Veri Seti Hikayesi : https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının,
01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

Değişkenler        

InvoiceNo       : Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
StockCode       : Ürün kodu. Her bir ürün için eşsiz numara.
Description     : Ürün ismi
Quantity        : Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
InvoiceDate     : Fatura tarihi ve zamanı.
UnitPrice       : Ürün fiyatı (Sterlin cinsinden)
CustomerID      : Eşsiz müşteri numarası
Country         : Ülke ismi. Müşterinin yaşadığı ülke.

Klasik bir transaction/ muhasebe datası. 
Bu, fatura kesme işlemine göre biçimlendirilmiş bir data olduğu anlamına gelir.
Bizim için önemli olan fatura/transaction'dur.

"""

# region import & read

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)  # float sayıların ondalık olarak 0'dan sonra kaç basamak gösterilmesi gerektiğini ayarlar.

df_ = pd.read_excel("/Users/apple/PycharmProjects/miuul/CRM_Analytics/Customer_Lifetime_Value/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()

# endregion

"""
-- Öncelikle analizi doğru bir şekilde gerçekleştirebilmek için, Invoice değişkeninin başında C olan değerleri, 
   yani iadeleri veri setinden çıkarmamız gerekmektedir çünkü iadeler quantity miktarında ve price miktarında 
   bazı yanlışlıklara sebep olmaktadır.
-- Bununla birlikte, veri setindeki bazı eksik değerleri gözlemleyip, veri ssetinin daha ölçülebilir olmasını 
   istediğimizden dolayı, veri setinden çıkarmamız gerekmektedir.

"""
df.head()

df = df[~df["Invoice"].str.contains("C", na=False)]

df.describe().T  # Quantity ve Price değişkenlerinde - değerler görüyoruz, bu mümkün olmadığından düzetme yapmalıyız.
df = df[(df["Quantity"] > 0)]

df.isnull().sum()
df.dropna(inplace=True)


df["TotalPrice"] = df["Quantity"] * df["Price"]

cltv_c = df.groupby("Customer ID").agg({"Invoice": lambda x: x.nunique(),
                                       "Quantity": lambda x: x.sum(),
                                       "TotalPrice": lambda x: x.sum()})

cltv_c.columns = ["total_transaction", "total_unit", "total_price"]


##################################################
# 2. Average Order Value (average_order_value = total_price / total_transaction)
##################################################

cltv_c.head()

cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

##################################################
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
##################################################

cltv_c.head()
cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]

cltv_c.shape[0]  # total num of customers

##################################################
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
##################################################

repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]

churn_rate = 1 - repeat_rate

##################################################
# 5. Profit Margin (profit_margin =  total_price * 0.10)
##################################################

cltv_c['profit_margin'] = cltv_c['total_price'] * 0.10

##################################################
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
##################################################

cltv_c['customer_value'] = cltv_c['average_order_value'] * cltv_c['purchase_frequency']

##################################################
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
##################################################

cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]

cltv_c.sort_values(by="cltv", ascending=False).head()
cltv_c.describe().T

##################################################
# 8. Segmentlerin Oluşturulması
##################################################

cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

cltv_c.sort_values(by="cltv", ascending=False).head()

cltv_c.groupby("segment").agg({"count", "mean", "sum"})

cltv_c.to_csv("cltv.csv")

##################################################
# 9. Tüm İşlemlerin Fonksiyonlaştırılması
##################################################

def create_cltv_c(dataframe, profit=0.10):

    # Veriyi hazırlama
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe['Quantity'] > 0)]
    dataframe.dropna(inplace=True)
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                                   'Quantity': lambda x: x.sum(),
                                                   'TotalPrice': lambda x: x.sum()})
    cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']
    # avg_order_value
    cltv_c['avg_order_value'] = cltv_c['total_price'] / cltv_c['total_transaction']
    # purchase_frequency
    cltv_c["purchase_frequency"] = cltv_c['total_transaction'] / cltv_c.shape[0]
    # repeat rate & churn rate
    repeat_rate = cltv_c[cltv_c.total_transaction > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate
    # profit_margin
    cltv_c['profit_margin'] = cltv_c['total_price'] * profit
    # Customer Value
    cltv_c['customer_value'] = (cltv_c['avg_order_value'] * cltv_c["purchase_frequency"])
    # Customer Lifetime Value
    cltv_c['cltv'] = (cltv_c['customer_value'] / churn_rate) * cltv_c['profit_margin']
    # Segment
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_c


df = df_.copy()

clv = create_cltv_c(df)

