#!/usr/bin/env python
# coding: utf-8

# In[128]:


import pandas as pd
import numpy as np

# Load data from Excel file
credit_data = pd.read_excel(r'C:\Users\eesha\Desktop\Edulty\CB_2.xls', sheet_name='Project_2')
customer_data = pd.read_excel(r'C:\Users\eesha\Desktop\Edulty\CB_2.xls', sheet_name='Customer_info')


# In[129]:


# Calculate the number of entries where Credit Card ID is blank
num_blank_cc_entries = credit_data['Credit_card'].isnull().sum()
print(num_blank_cc_entries)

# Provide a meaningful treatment where the Credit Card entries are blank
credit_data['Credit_card'].fillna('Unknown', inplace=True)

# Identity where Price is equal to Selling Price even after having a Coupon Code, apply an automatic discount of 5% for those entries
credit_data['Discounted_Selling_Price'] = np.where(credit_data['PRICE'] == credit_data['Selling_price'], credit_data['Selling_price'] * 0.95, credit_data['Selling_price'])

# Make sure that the return date is after the Purchase Date
credit_data['Return_Date'] = pd.to_datetime(credit_data['Return_date'])
credit_data['Purchase_Date'] = pd.to_datetime(credit_data['Date'])
credit_data = credit_data[credit_data['Return_Date'] >= credit_data['Purchase_Date']]

# If the Coupon ID is NULL, make sure that NO discount is given, the Selling Price should be equal to Price
credit_data['Selling_price'] = np.where(credit_data['Coupon_ID'].isnull(), credit_data['PRICE'], credit_data['Discounted_Selling_Price'])

# Age should be greater than 18 for all the CC holders
customer_data = customer_data[customer_data['Age'] > 18]

# Transaction ID should be unique for all
credit_data = credit_data.drop_duplicates(subset=['Transaction ID'], keep='first')


# In[130]:


# Combine data for segmentation
segmentation_data = pd.merge(credit_data, customer_data, left_on='Credit_card', right_on='C_ID', how='left')

# Create bins for customer age
age_bins = [0, 30, 50, 120]
age_labels = ['Young', 'Mid age', 'Old']
segmentation_data['Age_Group'] = pd.cut(segmentation_data['Age'], bins=age_bins, labels=age_labels)

# Convert 'Gender' and 'Age_Group' columns to strings
segmentation_data['Gender'] = segmentation_data['Gender'].astype(str)
segmentation_data['Age_Group'] = segmentation_data['Age_Group'].astype(str)
# Create segments based on gender and age group
segmentation_data['Segment'] = segmentation_data['Gender'] + ' ' + segmentation_data['Age_Group']

# Calculate the required statistics for each segment
segmentation_stats = segmentation_data.groupby(['Segment', 'Age_Group'])['Selling_price'].agg([('Sum_of_Selling_Price', 'sum'), ('No_of_Transactions', 'size')]).reset_index()

# Print the segmentation values
print("Segmentation\t\tAge Profile\t\tSum of Selling Price\tNo of Transactions")
for index, row in segmentation_stats.iterrows():
    print(f"{row['Segment']}\t\t{row['Age_Group']}\t\t{row['Sum_of_Selling_Price']:.2f}\t\t\t{row['No_of_Transactions']}")



# In[131]:


# Calculate spend in dollars based on Product, State, and Payment method
spend_by_product = segmentation_data.groupby('PID')['Selling_price'].sum()
spend_by_state = segmentation_data.groupby('State')['Selling_price'].sum()
spend_by_payment_method = segmentation_data.groupby('Payment Method')['Selling_price'].sum()


# In[132]:


# Highest 5 spenders based on Product
top_spenders_by_product = spend_by_product.nlargest(5)

# Highest 5 spenders based on State
top_spenders_by_state = spend_by_state.nlargest(5)

# Highest 5 spenders based on Payment method
top_spenders_by_payment_method = spend_by_payment_method.nlargest(5)


# In[133]:


# Custom function to extract hour from datetime.time object
def extract_hour(time_obj):
    return time_obj.hour

# Apply the custom function to extract the hour from 'Time' column
segmentation_data['Order_Hour'] = segmentation_data['Time'].apply(extract_hour)

# Create bins for order timing
time_bins = [0, 6, 12, 18, 24]
time_labels = ['Night', 'Morning', 'Afternoon', 'Evening']
segmentation_data['Order_Timing'] = pd.cut(segmentation_data['Order_Hour'], bins=time_bins, labels=time_labels)

# Calculate spend in dollars based on Order Timing
spend_by_timing = segmentation_data.groupby('Order_Timing')['Selling_price'].sum()


# In[134]:


# Calculate the average discount for each payment method
average_discount_by_payment_method = segmentation_data.groupby('Payment Method')['Discounted_Selling_Price'].mean()

# Identify the payment method with the highest average discount
payment_method_with_max_discount = average_discount_by_payment_method.idxmax()


# In[135]:


# Calculate the total discount
total_discount = (credit_data['PRICE'] - credit_data['Selling_price']).sum()
print(total_discount)


# In[136]:


# Places where return date is earlier than purchase date
invalid_return_dates = credit_data[credit_data['Return_Date'] < credit_data['Purchase_Date']]
print(invalid_return_dates[['Transaction ID', 'Return_Date', 'Purchase_Date']])


# In[137]:


# Calculate the total discount given where Coupon ID is null
total_discount_coupon_null = (credit_data.loc[credit_data['Coupon_ID'].isnull(), 'PRICE'] - credit_data.loc[credit_data['Coupon_ID'].isnull(), 'Selling_price']).sum()
print(total_discount_coupon_null)


# In[138]:


# Calculate the average age for missing values
average_age_missing_values = customer_data[customer_data['Age'].isnull()]['Age'].mean()
print(average_age_missing_values)


# In[139]:


print(segmentation_data['Segment'].value_counts())


# In[140]:


# Calculate the required statistics for each product category
product_stats = credit_data.groupby('P_CATEGORY')['Selling_price'].agg([('Sum_of_Selling_Price', 'sum'), ('No_of_Transactions', 'size')]).reset_index()

# Print the product category statistics
print("P_CATEGORY\tSum of Selling Price\tNo of Transactions")
for index, row in product_stats.iterrows():
    print(f"{row['P_CATEGORY']}\t\t{row['Sum_of_Selling_Price']:.2f}\t\t\t{row['No_of_Transactions']}")



# In[141]:


state_stats = segmentation_data.groupby('State')['Selling_price'].agg([('Sum_of_Selling_Price', 'sum'), ('No_of_Transactions', 'size')]).reset_index()

# Print the state statistics
print("State\t\tSum of Selling Price\tNo of Transactions")
for index, row in state_stats.iterrows():
    print(f"{row['State']}\t\t{row['Sum_of_Selling_Price']:.2f}\t\t\t{row['No_of_Transactions']}")


# In[142]:


# Calculate the sum of selling price and the number of transactions for each payment method
spend_by_payment_method = segmentation_data.groupby('Payment Method')['Selling_price'].agg([('Sum_of_Selling_Price', 'sum'), ('No_of_Transactions', 'size')]).reset_index()

# Print the payment method statistics
print("Payment Method\t\tSum of Selling Price\tNo of Transactions")
for index, row in spend_by_payment_method.iterrows():
    print(f"{row['Payment Method']}\t\t\t{row['Sum_of_Selling_Price']:.2f}\t\t\t{row['No_of_Transactions']}")


# In[143]:


# Calculate the total discount for each payment method
total_discount_by_payment_method = segmentation_data.groupby('Payment Method')['Discounted_Selling_Price'].sum()

# Print the total discount for each payment method
print("Payment Method\t\tTotal Discount")
for payment_method, total_discount in total_discount_by_payment_method.items():
    print(f"{payment_method}\t\t\t{total_discount:.2f}")


# In[ ]:





# In[ ]:





# In[ ]:




