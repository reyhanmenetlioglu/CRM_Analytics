"""
RFM Nedir?

Çok uzun süredir iş dünyasında oldukça yaygın bir şekilde kullanılan, CRM, Müşteri Analitiği, Veri Bilimi, Segmentasyon dendiğinde akla gelen ilk uygulamalardandır.
RFM Analizi basit, kural tabanlı, müşteri segmentasyonu için kullanılan bir tekniktir.
Müşterilerin satın alma alışkanlıkları üzerinden gruplara ayrılması ve bu gruplar özelinde stratejiler geliştirebilmesini sağlar.
CRM çalışmları için birçok başlıkta veriye dayalı aksiyon alma imkanı sağlar.

-- RFM : Recency
         Frequency
         Monetary
   ifadelerinin baş harflerinden meydana gelen bir isimlendirmedir. Recency, Frequency ve Monetary RFM metrikleridir.

   RFM metriklerinin detayları:

   Recency(Yenilik) : Müşterinin yenilik, ya da bizden en son ne zaman alışveriş yaptığının durumunu ifade eder.
   -- Örneğin, bir müşterinin rececncy değeri 1, diğer bir müşterinin recency değeri 10 ise, 1 olan bizim için daha iyidir.
      Çünkü, günlük cinsten konuşuyor olursak, henüz 1 gün önce alışveriş yapmış olduğunu gösterir.
      Müşterinin sıcaklığını, yeniliğini ifade etmektedir.

   Frequency(Sıklık) : İşlem sayısıdır.
   -- Örneğin, müşterinin toplam yaptığı alışveriş sayısını ifade eder. Her bir müşterinin satın alma sıklığı,
      ya da diğer ifadesi ile işlem sıklığı hesaplanarak, frequency isimlendirmesi ile temsil edilmiş olur.

   Monetary(Parasal Değer) : Müşterilerin bize bıraktığı parasal değeri ifade eder.


   Recency, Frequency ve Monetary RFM metriklerine dayalı olarak bazı skorlar oluşturacağız, ve bu skorlar üzerinden de segmentasyon gerçekleştireceğiz.

   RFM metriklerini hem birbirleri içerisinde, hem de birbirleri arasında "kıyaslanabilir" yapmak gerekmektedir.
   Bunun için, bu RFM metriklerini, RFM skorlarına çevirmemiz gerekmektedir.

   RFM metriklerini, RFM skorlarına çevirmek ne demektir?
   Elimizde Recency, Frequency ve Monetary değerleri var ve bunlar farklı ölçektedirler.
   Bunları skorlara çevirmek demek, hepsini aynı cinsten ifade etmek demektir.
   Yani aslında bir çeşit standartlaştırma işlemi yapacağız.
   Ve hepsini hem kendi içinde, hem de birbirleri arasında kıyaslanabilir bir formata getirmiş olacağız.

   RFM değerleri içerisinde, Recency'nin küçük olması bizim için iyiyken, Frequency ve Monetary'nin büyük olması bizim için iyidir.
   Bu yüzden bunun skoru oluşturulurken en yüksek skoru Recency'de en küçük değer alırken, Frequency ve Monetary'de en büyük değerler en yüksek skoru alırlar.

   Bu oluşturmuş olduğumuz RFM skorlarını daha sonra bir araya getirerek, yani hepsini string değerler olarak bir araya getirerek, RFM skorunu oluştururuz.

   Örneğin:   R    F    M    RFM

   Müşteri1   1    4    5    145
              5    5    5    555  en değerli müşteridir
              1    1    1    111  bizim  için çok da iyi olmayan müşteri

   Burada, RFM değerlerine 1 ve 5  arasında sayılar verdiğimiz için, ortaya çıkacak çok fazla sayıda RFM skorları kombinasyonu olacaktır.
   Bütün bu kombinasyonlar ile uğraşmak demek, aslında yine müşterileri tam olarak segmentlere ayıramamak anlamına gelmektedir.
   Dolayısıyla öyle bir işlem yapılmalı ki, RFM skorlarından daha az sayıda bir skor, bize ayrımları, mantıksal ve iş bilgisine uygun, gruplar, segmentler oluştursun. Bizim için bir değer ifade ediyor olsun.
   Bunun için sektörde yaygın kullanılan bir yöntem vardır. Buna göre segmentleri oluşturacağız.

   Özetle, iki boyut üzerinden, yani Recency, Frequency değerinden bir sınıflandırma yapılacaktır.
   X ekseninde recency değeri, Y ekseninde Frequency değeri vardır.
   CRM analitiği çalışmaları kapsamında, müşterilerin bizimle kurduğu ilişkilerde, frekans(Transactions), yani işlem daha önemlidir.
   Çünkü zaten bizimle işlem halinde, etkileşim halinde olan bir müşteriye daha fazla satış gerçekleştirebiliriz.
   Fakat bizimle bir frekansı, etkileşimi olmayan müşteri için Monetary değerine bakarak yorum yapmanın bir anlamı olmayacaktır. Ya da daha az anlamlı olacaktır.
   Özetle, iki boyut üzerinden, yani Recency, Frequency değerinden bir sınıflandırma yapılacaktır.
   RFM üzerinden oluşacak bu sabit segmentler ile, müşterilerimizi bu gruplara ayırıp, bu grupların özelinde yaklaşımlar gerçekleştirebiliriz.
   Bu grupların özelinde, çeşitli pazarlama yaklaşımları, satış yaklaşımları, iletişim yaklaşımları sergilenebilir.
"""

"""
RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)

1. İş problemi (Business Problem)
2. Veriyi anlama (Data Understanding)
3. Veriyi Hazırlama(Data Preparation)
4. RFM Metriklerinin Hesaplanması(Calculating RFM Metrics)
5. RFM Skorlarının Hesaplanması(Calculating RFM Scores)
6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi(Creating & Analysing RFM Segments)
7. Tüm sürecin Fonksiyonlaştırılması
"""


############################################################################################
# 1. İş problemi (Business Problem)
############################################################################################

""" 
Veri Seti Hikayesi :

https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının, 
01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

Değişkenler :

InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
Description: Ürün ismi
Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
InvoiceDate: Fatura tarihi ve zamanı.
UnitPrice: Ürün fiyatı (Sterlin cinsinden)
CustomerID: Eşsiz müşteri numarası
Country: Ülke ismi. Müşterinin yaşadığı ülke.

Bu e-ticaret şirketi müşterilerini segmentlere ayırıp,
bu segmentlere göre pazarlama stratejileri vermek istiyor.
"""

############################################################################################
# 2. Veriyi anlama (Data Understanding)
############################################################################################

# region import

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)  # tüm sütunların görünmesi için
# pd.set_option('display.max_rows', None)  # tüm satırların görünmesi için
pd.set_option('display.float_format', lambda x: '%3f' % x)  # sayısal değişkenlerin virgülden sonra kaç basamağının gösterileceğini ifade eder.
df_ = pd.read_excel("/Users/apple/PycharmProjects/miuul/CRM_Analytics/Analysis_of_RFM/online_retail_II.xlsx", sheet_name = "Year 2009-2010")

# endregion

# region df = fd_.copy()
"""verinin okunması zaman aldığı için, 
   daha sonra tekrar çalıştırma ihtiyacımıza karşın,
   öncelikle df_ isimlendirmesi yapıp, daha sonra kopyasını oluşturup 
   df e atayarak üzerinde çalışmaya devam edeceğiz. 
   Eğer ileride ters bir şey gerçekleşirse, tekrar veri okutma işlemi yerine df = df_.copy()
   çalıştırıldığında, uzun verime okuma işlemini beklememiş olacağız."""

df = df_.copy()

# endregion

df.head()
df.shape

# region eksik degerler

df.isnull().sum()
"""
Customer_ID eksikliği varsa veri setinden sileceğiz.
Müşteri özelinde segmentasyon çalışması yapacağımızdan dolayı,
ölçülebilirlik değeri taşımıyor olacak.
"""
# endregion

# region veriyi anlama

df["Description"].nunique()
df["Description"].value_counts().head()
df.groupby("Description").agg({"Quantity": "sum"})
df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending = False).head()
df["Invoice"].nunique()

# endregion

# region toplam kazanç / fatura başına kazanç

# Ürünlerin toplam kazancı ?
df["TotalPrice"] = df["Quantity"] * df["Price"]

# Fatura başına toplam ne kadar kazanılmıştır ?
df.groupby("Invoice").agg({"TotalPrice": "sum"}).head()

# endregion

############################################################################################
# 3. Veriyi Hazırlama(Data Preparation)
############################################################################################

df.shape

# region eksik değerleri silme

df.isnull().sum()
"""
Burada ilk yapılacak şey, eksik olan Customer ID lerin veri setinden silinmesi olmalıdır.
Description'daki eksik değerler az, veri setindeki gözlemler yeterince fazla olduğundan, 
bu değerlerin de silinmesi sorun yaratmaz."""

df.dropna(inplace=True)  # dropna ifadesi eksik değerleri silmek için kullanılır.

"""
RFM'de outliers temizliği yapmalı mıyız? Yapabilir miyiz?
Dilenirse yapılabilir, fakat burada zaten outlier'lar bizim için 
5 skoruna denk geleceğinden dolayı, eğer zaten aykırı değer çözümü olarak
bir baskılama yapacak olsaydık bile aynı değere denk geleceğinden dolayı
aykırı değer incelemesini, analizini ya da düzeltmesini yapmamak tercih edilebilir.
"""

# endregion

df.describe().T

# region Invoice değişkeninden C'leri temizleme
"""
Veri seti hikayesinde, Invoice değişkeninde C olan değerler olduğunu öğrenmiştik.
Bu C'ler iadeleri ifade etmektedir. Bu iadelerin de sonucu, veriyi anlama bölümünde fark ettiğimiz,
bazı eksi değerlerin gelmesine sebep olmuştur. 
Yani iadelerin veri setinin yapısını bozması söz konusudur. Bu sebeple bu ifadeleri veri setinden dışarıda bırakmalıyız.
"""
# "C" yi barındıranların dışındaki değerleri getirmek için
df = df[~df["Invoice"].str.contains("C", na=False)]

# endregion

############################################################################################
# 4. RFM Metriklerinin Hesaplanması(Calculating RFM Metrics)
############################################################################################

"""
RFM Metrikleri : Recency, Frequency, Monetary

   Recency : 
   -- Müşterinin yeniliği, sıcaklığı.
   -- Matematiksel karşılığı : (analizin yapıldığı tarih) - (ilgili müşterinin son satın alma yaptığı tarih)
   
   Frequency :
   -- Müşterinin yaptığı tplam satın almadır.
   
   Monetary :
   -- Müşterinin yaptığı satın almalar neticesinde, bıraktığı toplam parasal değerdir.
"""

df.head()

# region Analiz Tarihi Oluşturma

"""
-- Burada öncelikle analizi yaptığımız günü belirlememiz gerekmektedir.
-- Bu veri seti 2009-2010 yılları arasını kapsayan bir veri setidir.
-- O tarihlerde olmadığımız için izleyeceğimiz yol, ilgili hesaplamaların yapılabilmesi için,
   analizin yapıldığı günü tanımlamamız gerekmektedir. 
-- Yani örneğin, bu veri seti içerisindeki en son tarih hangisi ise, 
   bu tarihin üzerine 2 gün koyarsak ve analiz yapılan tarih gibi kabul edersek,
   bu tarih üzerinden Recency'i hesapalrız.
"""

df["InvoiceDate"].max()  # Timestamp('2010-12-09 20:01:00') : Analiz için seçeceğimiz tarih : 2010-12-11

today_date = dt.datetime(2010, 12, 11)
type(today_date)  # Out[29]: datetime.datetime  : zaman formunda bir değişken tipi

"""
-- Bunun anlamı, datetime() içine girdiğimiz tarihi,
   today_date değişkeni içerinde tutacağız ve zaman değişkeni
   formunda (datetime.datetime) oluşturulmasını istiyoruz.
-- Bu zaman formu bize, yapacacağımız işlemlerde zaman açısından 
   fark alabilme imkanı sağlayacaktır.
"""

# endregion

"""
-- Aslında, RFM analizinin temeli, basit bir pandas operasyonudur.
-- Buradaki bütün müşterilere göre groupby' a alacağız.
-- Böylece, Recency, Frequency ve Monetary'i kolay bir şekilde hesaplayacağız.

Bunun için Recency için yapmamız gerekir?

-- CustomerID'ye göre groupby'a aldıktan sonra, her bir müşterinin
   max tarihini bulmamız gerekmekterdir.
-- Daha sonra today_date'ten çıkardığımızda recency'i bulmuş olacağız.

Bunun için Frequency için yapmamız gerekir?

-- Ve yine benzer bir şekilde CustomerID'ye göre groupby'a aldıktan sonra,
   her bir müşterinin eşsiz fatura sayısına gidersek, böylece müşterinin 
   kaç tane işlem yaptığını, satın alma yaptığını buluruz.
   
Bunun için Monetary için yapmamız gerekir?

-- Eğer yine CustomerID'ye göre groupby'a aldıktan sonra, TotalPrice'ların 
   sum'ını alırsak, bu durumda her bir müşterinin toplam kaç para değer 
   bıraktığını hesaplamış oluruz.
"""

# region RFM Analizi
rfm = df.groupby("Customer ID").agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice: Invoice.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

"""
'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days

-- Kullanıcıya göre groupby'a aldıktan sonra:
-- Burada her bir kullanıcı özelinde InvoiceDate'leri temsil eder.
-- Bugünün tarihinden (today_date) ilgili müşetirin en son satın alma tarihi (InvoiceDate.max()) çıkarılır.
-- Bu tarih, tarihsel bir değişken olduğu için, bunu gün cinsinden ifade ederiz (.days). 
-- Böylece her bir müşterinin Recency değerini elde etmiş oluruz.

'Invoice': lambda Invoice: Invoice.nunique()

-- Kullanıcıya göre groupby'a aldıktan sonra:
-- Invoice'ların eşsiz değerlerini alıyoruz ve kaç tane fatura olduğuna bakıyoruz.
-- Yani frequency değerini hesaplamış oluyoruz.

'TotalPrice': lambda Invoice: TotalPrice.sum()

-- TotalPrice'ların sum'ını alıyoruz.
-- Böylece Monetary değerini elde etmiş oluruz.

"""
rfm.head()
rfm.columns = ['recency', 'frequency', 'monetary']  # liste aracılığı ile column isimlerini(değişkenleri) değiştirebiliriz.
rfm.describe().T

"""
rfm.describe().T gözlemi sonucu:
Monetary değişkeninin min değerinin 0 olduğunu inceledik.
Bu istediğimiz bir değer olmadığı için, 0 dan büyük değerleri seçeceğiz.
"""

rfm = rfm[rfm["monetary"] > 0]

rfm.shape

# endregion

############################################################################################
# 5. RFM Skorlarının Hesaplanması(Calculating RFM Scores)
############################################################################################

# region R, F, M için skorların oluşturulması

"""
-- Burada dikkat edilmesi gereken ilk şey,
   Recency'nin ters, Frequency ve Monetary'nin düz bir 
   büyüklük, küçüklük algısı olması.
-- Yani Frequency ve Monetary'de büyük olan değerlere 
   skor olarak da büyük olan verilirken,
   Recency'de küçük olan değere büyük skor değeri verilir.
"""

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels = [5, 4, 3, 2, 1])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels = [1, 2, 3, 4, 5])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method = "first"), 5, labels = [1, 2, 3, 4, 5])

"""
quantile'ın asıl yaptığı: 

-- Bir değişkeni küçükten büyüğe sıralar.
-- Belirli parçalara göre bunu böler.
-- Recency için Küçükten büyüğe doğru, 5-1 aralığında girdiğimiz skorlara atama yapar.
-- Frequency ve Monetary için küüçkten büyüğe doğru 1-5 aralığında girdiğimiz skorlara atama yapar.

"""

# endregion

# region RFM_SCORE Değişkeninin Oluşturulması

# Şimdi bu değerler üzerinden skor değişkeni oluşturmamız gerekmektedir.
# R ve F değerlerini bir araya getirmemiz gerekmektedir.
# Monetary'i hesaplama sebebimiz yalnızca gözlem yapmaktır.

rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) +
                    rfm["frequency_score"].astype(str))

rfm.describe().T # RFM_SCORE string tipte olduğu için burada gözlemleyemeyiz.

rfm[rfm["RFM_SCORE"] == "55"]  # en değerli müşteriler
rfm[rfm["RFM_SCORE"] == "11"]  # bizim için değersiz müşteriler.

# endregion

############################################################################################
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi(Creating & Analysing RFM Segments)
############################################################################################

# region RFM isimlendirmesi

# regex ?

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

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

# endregion

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# need_attention sınıfına erişmek istiyorsak:

rfm[rfm["segment"] == "need_attention"].head()

# cant_loose sınıfına erişmek istiyorsak:

rfm[rfm["segment"] == "cant_loose"].head()

# sadece new_customers 'ın ID'lerine erişmek istersek:

rfm[rfm["segment"] == "new_customers"].index

# Bu işlemlerin sonucunu dışarı aktarmak için:

new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index
new_df["new_customer_id"].astype(int) # astype(int) ondalıklardan kurtulmak için

# region excel veya csv formunda dışarı aştarma

new_df.to_csv("new_customers.csv")
rfm.to_csv("rfm.csv")

"""
Bu sonuçlar daha sonra bir database'e basılır,
yani tablo haline gelir, o tabloda oluşturduğumuz
bütün segmentler yer alır, yine o tablo ile konuşan tableau,
powerbi gibi iş zakası aracı seçimler yaparak kolayca 
ilgili arayüzlerden bu bilgilere erişebilir.
"""

# endregion

# BI aracı ?

############################################################################################
# 7. Tüm sürecin Fonksiyonlaştırılması
############################################################################################

def create_rfm(dataframe, csv=False):

    # VERIYI HAZIRLAMA
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    # RFM METRIKLERININ HESAPLANMASI
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]

    # RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    # cltv_df skorları kategorik değere dönüştürülüp df'e eklendi
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))


    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm

df = df_.copy()

rfm_new = create_rfm(df, csv=True)