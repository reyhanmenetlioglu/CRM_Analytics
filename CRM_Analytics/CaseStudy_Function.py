def data_preparing(csv=False):

    # importingz

    import pandas as pd
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
        df.to_csv("df.csv")

    return df

data_preparing()