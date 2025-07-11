DROP DATABASE IF EXISTS db_noted;
CREATE DATABASE db_noted;
USE db_noted;

-- ======================
-- Table: Categories
-- ======================
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

INSERT INTO categories (description) VALUES 
('note'), 
('write'), 
('type'), 
('essentials');

-- ======================
-- Table: Product Collections
-- ======================
CREATE TABLE product_collections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- ======================
-- Table: Products
-- ======================
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    image VARCHAR(200),
    category_id INT,
    collection_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (collection_id) REFERENCES product_collections(id) ON DELETE SET NULL
);

-- ======================
-- Table: Product Images
-- ======================
CREATE TABLE product_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    path VARCHAR(255) NOT NULL,
    caption VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- ======================
-- Table: Product Features
-- ======================
CREATE TABLE feature_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE product_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    feature_type_id INT NOT NULL,
    value VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (feature_type_id) REFERENCES feature_types(id) ON DELETE CASCADE
);

-- ======================
-- Table: Users
-- ======================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    address TEXT,
    noted_cash DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    role INT NOT NULL DEFAULT 2, -- 1 = admin, 2 = client
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

-- ======================
-- Table: Noted Cash Transactions
-- ======================
CREATE TABLE noted_cash_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    change_amount DECIMAL(10,2) NOT NULL,
    reason VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ======================
-- Table: Orders
-- ======================
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATETIME NOT NULL,
    total DECIMAL(10,2),
    shipping_method VARCHAR(100),
    payment_method VARCHAR(100),
    billing_same_as_shipping BOOLEAN DEFAULT TRUE,
    status VARCHAR(50) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tracking_number VARCHAR(100),
    admin_notes TEXT,
    invoice_number VARCHAR(50),
    invoice_generated BOOLEAN DEFAULT FALSE,
    invoice_sent BOOLEAN DEFAULT FALSE,
    invoice_sent_date DATETIME,
    tax_rate DECIMAL(5,2) DEFAULT 23.00, -- Default VAT rate for Portugal
    tax_amount DECIMAL(10,2),
    subtotal DECIMAL(10,2),
    shipping_cost DECIMAL(10,2) DEFAULT 0.00,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ======================
-- Table: Order Items
-- ======================
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ======================
-- Table: Product Stock
-- ======================
CREATE TABLE product_stock (
    product_id INT PRIMARY KEY,
    quantity INT NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ======================
-- Table: Cart
-- ======================
CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ======================
-- Table: Discounts
-- ======================
CREATE TABLE discounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    is_percentage BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- Table: Shipping Addresses
-- ======================
CREATE TABLE shipping_addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    street_address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- ======================
-- Table: Billing Addresses
-- ======================
CREATE TABLE billing_addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    street_address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- ======================
-- Table: Payment Info
-- ======================
CREATE TABLE payment_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    card_last4 VARCHAR(4),
    card_brand VARCHAR(50),
    paid BOOLEAN DEFAULT FALSE,
    payment_date DATETIME,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- ======================
-- Table: Invoices
-- ======================
CREATE TABLE invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    invoice_date DATETIME NOT NULL,
    pdf_path VARCHAR(255),
    company_name VARCHAR(100) DEFAULT 'Noted Stationery, Lda.',
    company_vat VARCHAR(20) DEFAULT 'PT123456789',
    company_address VARCHAR(255) DEFAULT 'Rua Principal 123, 1000-001 Lisboa, Portugal',
    company_phone VARCHAR(20) DEFAULT '+351 910 000 000',
    company_email VARCHAR(100) DEFAULT 'invoices@noted.pt',
    payment_terms VARCHAR(255) DEFAULT 'Payment due within 30 days',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- ======================
-- Table: Email Notifications
-- ======================
CREATE TABLE email_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    notification_type ENUM('order_confirmation', 'order_processing', 'order_shipped', 'invoice', 'payment_confirmation') NOT NULL,
    recipient_email VARCHAR(100) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    sent_at DATETIME,
    status VARCHAR(50) DEFAULT 'pending',
    error_message TEXT,
    attachments TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- ======================
-- Stored Procedures
-- ======================

DELIMITER //

-- Procedure to generate invoice number and create invoice record
CREATE PROCEDURE GenerateInvoice(IN order_id INT)
BEGIN
    DECLARE invoice_num VARCHAR(50);
    DECLARE order_exists INT;
    DECLARE invoice_exists INT;
    
    -- Check if order exists
    SELECT COUNT(*) INTO order_exists FROM orders WHERE id = order_id;
    
    IF order_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Order does not exist';
    ELSE
        -- Check if invoice already exists for this order
        SELECT COUNT(*) INTO invoice_exists FROM invoices WHERE order_id = order_id;
        
        IF invoice_exists = 0 THEN
            -- Generate invoice number: INV-YEAR-MONTH-OrderID
            SET invoice_num = CONCAT('INV-', 
                                     DATE_FORMAT(CURRENT_DATE(), '%Y'),
                                     DATE_FORMAT(CURRENT_DATE(), '%m'),
                                     '-',
                                     LPAD(order_id, 5, '0'));
            
            -- Update order with invoice number
            UPDATE orders SET 
                invoice_number = invoice_num,
                invoice_generated = TRUE
            WHERE id = order_id;
            
            -- Create invoice record
            INSERT INTO invoices (
                order_id,
                invoice_number,
                invoice_date,
                created_at
            ) VALUES (
                order_id,
                invoice_num,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP()
            );
        END IF;
    END IF;
END //

-- ======================
-- Invoice Auto Generation
-- ======================

-- Procedure to generate invoice number
CREATE PROCEDURE generate_invoice_number(IN p_order_id INT, OUT p_invoice_number VARCHAR(50))
BEGIN
    DECLARE v_year CHAR(4);
    DECLARE v_seq_num INT;
    
    -- Get current year
    SET v_year = DATE_FORMAT(NOW(), '%Y');
    
    -- Generate sequence number
    SELECT IFNULL(MAX(SUBSTRING_INDEX(invoice_number, '-', -1) + 0), 0) + 1 
    INTO v_seq_num 
    FROM invoices 
    WHERE invoice_number LIKE CONCAT('INV-', v_year, '-%');
    
    -- Format invoice number: INV-YYYY-00001
    SET p_invoice_number = CONCAT('INV-', v_year, '-', LPAD(v_seq_num, 5, '0'));
END //
