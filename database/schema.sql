create table if not exists customers(
    customer_id text primary key,
    customer_unique_id text,
    customer_zip_code_prefix integer,
    customer_city text,
    customer_state text
);

create table if not exists orders(
    order_id text primary key,
    customer_id text,
    order_status text,
    order_purchase_timestamp text,
    order_approved_at text,
    order_delivered_carrier_date text,
    order_delivered_customer_date text,
    order_estimated_delivery_date text,

    foreign key(customer_id)
    references customers(customer_id)
);

create table if not exists products(
    product_id text primary key,
    product_category_name text,
    product_name_lenght integer,
    product_description_lenght integer,
    product_photos_qty integer,
    product_weight_g real,
    product_length_cm real,
    product_height_cm real,
    product_width_cm real
);

create table if not exists reviews(
    review_id text primary key,
    order_id text,
    review_score integer,
    review_comment_title text,
    review_comment_message text,
    review_creation_date text,
    review_answer_timestamp text,

    foreign key(order_id)
    references orders(order_id)
);

create table if not exists sellers(
    seller_id text primary key,
    seller_zip_code_prefix integer,
    seller_city text,
    seller_state text
);

create table if not exists payments(
    order_id text,
    payment_sequential integer,
    payment_type text,
    payment_installments integer,
    payment_value real,

    primary key(order_id,payment_sequential),

    foreign key(order_id)
    references orders(order_id)
);

create table if not exists order_items(
    order_id text,
    order_item_id integer,
    product_id text,
    seller_id text,
    shipping_limit_date text,
    price real,
    freight_value real,

    primary key(order_id,order_item_id),

    foreign key(order_id)
    references orders(order_id),

    foreign key(product_id)
    references products(product_id),

    foreign key(seller_id)
    references sellers(seller_id)
);

create table if not exists geolocation(
    geolocation_zip_code_prefix integer,
    geolocation_lat real,
    geolocation_lng real,
    geolocation_city text,
    geolocation_state  text
);