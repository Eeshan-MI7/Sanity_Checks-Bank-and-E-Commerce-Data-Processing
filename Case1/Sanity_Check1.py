#!/usr/bin/env python
# coding: utf-8

# In[30]:


import pandas as pd

# Step 1: Load the data
df_customers = pd.read_excel(r'C:\Users\eesha\Desktop\Edulty\Credit Banking_Project1.xls',sheet_name='Customer Acqusition')
df_spending = pd.read_excel(r'C:\Users\eesha\Desktop\Edulty\Credit Banking_Project1.xls',sheet_name='Spend')
df_repayment = pd.read_excel(r'C:\Users\eesha\Desktop\Edulty\Credit Banking_Project1.xls',sheet_name='Repayment')

# Step 2a: Treat values where age is less than 18
df_customers.loc[df_customers['Age'] < 18, 'Age'] = 'Underage'


# In[31]:


# Step 2b: Identify cases where repayment is more than spend and calculate credit
df_merged = pd.merge(df_spending, df_repayment, on=['Sno', 'Customer', 'Month'], how='left')
df_merged['surplus'] = df_merged['AmountR'] - df_merged['AmountS']
df_merged['credit'] = 0
df_merged.loc[df_merged['surplus'] > 0, 'credit'] = df_merged['surplus'] * 0.02


# In[32]:


# Step 3: Monthly spend of each customer
monthly_spend = df_spending.groupby('Customer')['AmountS'].sum()


# In[33]:


# Step 4: Monthly repayment of each customer
monthly_repayment = df_repayment.groupby('Customer')['AmountR'].sum()


# In[34]:


# Step 5: Highest paying 10 customers
top_10_customers = monthly_repayment.nlargest(10)


# In[35]:


# Step 6: Segment with highest spending
segment_spending = df_customers.merge(df_spending, on='Customer')['Segment']
segment_with_highest_spending = segment_spending.value_counts().idxmax()


# In[36]:


# Step 7: Age group with highest spending
age_group_spending = df_customers.merge(df_spending, on='Customer')['Age']
age_group_with_highest_spending = age_group_spending.value_counts().idxmax()


# In[37]:


# Step 8: Most profitable segment
segment_profitability = df_customers.merge(df_spending, on='Customer').merge(df_repayment, on=['Customer', 'Month'])
segment_profitability['profitability'] = segment_profitability['AmountS'] - segment_profitability['AmountR']
most_profitable_segment = segment_profitability.groupby('Segment')['profitability'].sum().idxmax()


# In[38]:


# Step 9: Category with highest spending
category_spending = df_spending.groupby('Type')['AmountS'].sum()
category_with_highest_spending = category_spending.idxmax()


# In[39]:


# Step 10: Monthly profit for the bank
monthly_profit = monthly_spend.sum() - monthly_repayment.sum()


# In[40]:


# Step 11: Impose an interest rate of 2.9% for each customer for any due amount
df_merged['due_interest'] = df_merged['AmountR'] * 0.029


# In[41]:


# Print the results
print("Monthly spend of each customer:")
print(monthly_spend)
print("\nMonthly repayment of each customer:")
print(monthly_repayment)
print("\nHighest paying 10 customers:")
print(top_10_customers)
print("\nSegment with highest spending:")
print(segment_with_highest_spending)
print("\nAge group with highest spending:")
print(age_group_with_highest_spending)
print("\nMost profitable segment:")
print(most_profitable_segment)
print("\nCategory with highest spending:")
print(category_with_highest_spending)
print("\nMonthly profit for the bank:")
print(monthly_profit)


k=input("\npress close to exit") 




