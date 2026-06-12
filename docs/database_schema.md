# ExecuMind AI Database Schema

## Overview

This document defines the SQLite database schema used in the ExecuMind AI Executive Intelligence Platform. The schema is based on the Olist Brazilian E-Commerce Dataset and serves as the structured analytics layer for KPI monitoring, business intelligence, forecasting, and executive decision support.

---

# customers

## Description

Stores customer information.

## Primary Key

customer_id

| Column Name              | Data Type | Description                            |
| ------------------------ | --------- | -------------------------------------- |
| customer_id              | TEXT      | Unique customer identifier             |
| customer_unique_id       | TEXT      | Unique customer across multiple orders |
| customer_zip_code_prefix | INTEGER   | ZIP code prefix                        |
| customer_city            | TEXT      | Customer city                          |
| customer_state           | TEXT      | Customer state                         |

---

# orders

## Description

Stores order lifecycle information.

## Primary Key

order_id

## Foreign Keys

customer_id → customers.customer_id

| Column Name                   | Data Type | Description                |
| ----------------------------- | --------- | -------------------------- |
| order_id                      | TEXT      | Unique order identifier    |
| customer_id                   | TEXT      | Customer placing the order |
| order_status                  | TEXT      | Order status               |
| order_purchase_timestamp      | TEXT      | Purchase timestamp         |
| order_approved_at             | TEXT      | Payment approval timestamp |
| order_delivered_carrier_date  | TEXT      | Carrier pickup date        |
| order_delivered_customer_date | TEXT      | Customer delivery date     |
| order_estimated_delivery_date | TEXT      | Estimated delivery date    |

---

# products

## Description

Stores product information.

## Primary Key

product_id

| Column Name           | Data Type | Description        |
| --------------------- | --------- | ------------------ |
| product_id            | TEXT      | Product identifier |
| product_category_name | TEXT      | Product category   |
| product_name_lenght   | REAL        | Product name length|
| product_description_lenght| REAL  | Product description length|   |
| product_photos_qtY    | REAL      | Productphoto quality   |
| product_weight_g      | REAL      | Product weight     |
| product_length_cm     | REAL      | Product length     |
| product_height_cm     | REAL      | Product height     |
| product_width_cm      | REAL      | Product width      |

---

# sellers

## Description

Stores seller information.

## Primary Key

seller_id

| Column Name            | Data Type | Description       |
| ---------------------- | --------- | ----------------- |
| seller_id              | TEXT      | Seller identifier |
| seller_zip_code_prefix | INTEGER   | ZIP code prefix   |
| seller_city            | TEXT      | Seller city       |
| seller_state           | TEXT      | Seller state      |

---

# payments

## Description

Stores payment transactions.

## Primary Key

Composite Key:
(order_id, payment_sequential)

## Foreign Keys

order_id → orders.order_id

| Column Name          | Data Type | Description       |
| -------------------- | --------- | ----------------- |
| order_id             | TEXT      | Order identifier  |
| payment_sequential   | INTEGER   | Payment sequence  |
| payment_type         | TEXT      | Payment method    |
| payment_installments | INTEGER   | Installment count |
| payment_value        | REAL      | Payment amount    |

---

# reviews

## Description

Stores customer review information.

## Primary Key

review_id

## Foreign Keys

order_id → orders.order_id

| Column Name            | Data Type | Description       |
| ---------------------- | --------- | ----------------- |
| review_id              | TEXT      | Review identifier |
| order_id               | TEXT      | Related order     |
| review_score           | INTEGER   | Rating score      |
| review_comment_title   | TEXT      | Review title      |
| review_comment_message | TEXT      | Review text       |
| review_creation_date   | TEXT      | Review date       |
| review_answer_timestamp| TEXT      | Review answer time|

---

# order_items

## Description

Stores products purchased within each order.

## Composite Primary Key

(order_id, order_item_id)

## Foreign Keys

order_id → orders.order_id

product_id → products.product_id

seller_id → sellers.seller_id

| Column Name         | Data Type | Description       |
| ------------------- | --------- | ----------------- |
| order_id            | TEXT      | Order identifier  |
| order_item_id       | INTEGER   | Item sequence     |
| product_id          | TEXT      | Purchased product |
| seller_id           | TEXT      | Seller identifier |
| shipping_limit_date | TEXT      | Shipping deadline |
| price               | REAL      | Product price     |
| freight_value       | REAL      | Shipping charge   |

---

# Geolocation

## Description

Stores ZIP-code-level geographic information.

## Note

This table is used for analytics but not heavily used in Week 2 joins.

| Column Name                 | Data Type | Description |
| --------------------------- | --------- | ----------- |
| geolocation_zip_code_prefix | INTEGER   | ZIP prefix  |
| geolocation_lat             | REAL      | Latitude    |
| geolocation_lng             | REAL      | Longitude   |
| geolocation_city            | TEXT      | City        |
| geolocation_state           | TEXT      | State       |
