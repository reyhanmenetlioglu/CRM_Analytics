# rfm["interested_Women_Cat"] = df["interested_in_categories_12"].values
# rfm = rfm[rfm["interested_Women_Cat"].str.contains("KADIN")]
# rfm = rfm[rfm["segment"].str.contains("champions|loyal_customers", case=False, na=False, regex=True)]
# rfm.reset_index(inplace=True)




# rfm["Male_Children"] = df["interested_in_categories_12"].values
# rfm = rfm[rfm["Male_Children"].str.contains("ERKEK|COCUK", case=False, na=False, regex=True)]
# rfm = rfm[rfm["segment"].str.contains("cant_loose|about_to_sleep|new_customers", case=False, na=False, regex=True)]
# rfm.reset_index(inplace=True)
# rfm["master_id"]