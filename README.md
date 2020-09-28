# Lifestream

Lifestream is a Python library to make sense out of your transaction logs. Import a log of your transactional data and let's explore! 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install lifestream
```
## Transactional Data 
At a minimum, the transactional data you import should have the following: 

* OrderID assoiated with transaction
* Unique user id associated with transaction
* Date of transaction
* Monetary value of transaction


| order_id | user_id | date       | monetary_value |
|----------|---------|------------|----------------|
| 768      | 13      | 09/13/2020 | $15.12        |
| 769      | 13249   | 09/13/2020 | $240.00        |
| 770      | 11424   | 09/13/2020 | $194.34        |

*Is your transactional data in another kind of format? See the `create_transaction_log` function below.*

## Usage
Need to create a transaction log that meets the library's requirements? If your data is as raw as the individually purchased items, try this method.

```python

lifestream.create_transaction_log(df, invoicenum, date_col, quantity, unitprice, customerid)
```
* **df** is a dataframe of your  data.
* **date_col** represents the column of the dataframe which contains the datetime of the transaction.
* **user_id** represents the column of the dataframe which contains the unique user id associated with the transaction. 
* **quantity** represents the column of the dataframe which contains the quantity of an item purchased in the transaction.
* **unitprice** represents the column of the dataframe which contains the price of an item purchased in the transaction
* **customerid** is the unique id associated with the customer making the purchase.


Want to plot sales by month?
```python
import lifestream

lifestream.sales_chart(transaction_log, date_col, monetary_val, user_id)
```
* **transaction_log** is a dataframe of your transactional data.
* **date_col** represents the column of the transaction_log dataframe which contains the datetime of the transaction.
* **monetary_val** represents the column of the transaction_log dataframe which contains the monetary value of the transaction. 
* **user_id** represents the column of the transaction_log dataframe which contains the unique user id associated with the transaction. 

Want to dig into basic cohort analyses? Plot how many users from a cohort are still spending in subsequent months.
```python

lifestream.cohort_retention_chart(df, date_col, user_id, monetary_val, cohort1, cohort2, cohort3)
```
* **df** is a dataframe of your transactional data.
* **date_col** represents the column of the dataframe which contains the datetime of the transaction.
* **user_id** represents the column of the dataframe which contains the unique user id associated with the transaction. 
* **monetary_val** represents the column of the dataframe which contains the monetary value of the transaction. 
* **cohort1**, **cohort2**, **cohort3** are the three cohorts you are interested in, expressed as 'YYYY-MM' string.

Plot how many new users you are acquiring per month.

```python

lifestream.new_customers_chart(df, date_col, user_id)
```
* **df** is a dataframe of your transactional data.
* **date_col** represents the column of the dataframe which contains the datetime of the transaction.
* **user_id** represents the column of the dataframe which contains the unique user id associated with the transaction. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
