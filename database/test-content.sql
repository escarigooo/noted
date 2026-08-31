-- ============================
-- Tabela de Coleções de Produto
-- ============================
INSERT INTO product_collections (name, description) VALUES 
('Studio', 'A refined digital writing collection with the Slate tablet and accessories.'),
('Momentum', 'Organize thoughts, create goals, and capture life''s achievements with Momentum tools.'),
('Horizon', 'A collection of advanced digital writing tools designed for immersive experiences.');

-- ===========================
-- STUDIO COLLECTION PRODUCTS
-- ===========================

-- 1. Slate Tablet
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    1,
    'Slate',
    'The Slate tablet combines modern digital writing with elegant design, ideal for notes, sketches, and productivity.',
    479.00,
    'tablet.png',
    1,
    1
);


-- 2. Slate Sleeve
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    2,
    'Slate Sleeve',
    'Premium protective folio case for your Slate tablet, ensuring safety and elegance on the go.',
    69.00,
    'essentials.png',
    4,
    1
);

-- 3. Studio Stylus Pen
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    3,
    'Studio Stylus',
    'A smooth, digital ink pen designed for precision and comfort, tailored for the Studio experience.',
    49.00,
    'stylus.png',
    2,
    1
);

-- 4. Stylus Nibs
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    4,
    'Stylus Nibs',
    'High-quality refill tips for your Studio Stylus pen. Long-lasting and friction-optimized.',
    12.00,
    'essentials.png',
    4,
    1
);

-- ===========================
-- MOMENTUM COLLECTION PRODUCTS
-- ===========================

-- 5. Cable
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (5, 'Cable', 'High-quality USB-C cable for charging and data transfer.', 9.99, 'essentials.png', 4, 2);


-- 6. Marker Tips
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (6, 'Marker Tips', 'Set of replacement marker tips for your digital pen.', 7.99, 'stylus.png', 4, 2);

-- 7. Focus Planner
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (7, 'Focus Planner', 'Digital productivity planner with structured pages.', 14.99, 'essentials.png', 2, 2);


-- 8. Daybook Journal
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (8, 'Daybook', 'Notebook for recording milestones and memories.', 19.99, 'essentials.png', 1, 2);


-- 9. Type Folio
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (9, 'Folio Mini', 'Keyboard folio case for your tablet.', 89.00, 'folio.png', 3, 2);


-- ===========================
-- HORIZON COLLECTION PRODUCTS
-- ===========================

-- 10. Canvas Tablet
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    10,
    'Canvas',
    'A powerful and elegant digital notebook for immersive writing and sketching.',
    499.00,
    'tablet.png',
    1,
    3
);


-- 11. Precision Stylus
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    11,
    'Precision Stylus',
    'A sleek pen with high-precision digital ink for the Canvas tablet.',
    59.00,
    'stylus.png',
    2,
    3
);

-- 12. Folio Pro
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    12,
    'Folio Pro',
    'Ergonomic keyboard folio designed exclusively for Canvas tablets.',
    99.00,
    'folio.png',
    3,
    3
);




-- ===========================
-- FEATURE TYPES
-- ===========================
INSERT INTO feature_types (name) VALUES 
('Screen Size'),
('Storage'),
('Battery Life'),
('Connectivity'),
('Color'),
('Material'),
('Weight'),
('Compatibility');

-- ===========================
-- PRODUCT FEATURES
-- ===========================
-- Studio features
INSERT INTO product_features (product_id, feature_type_id, value) VALUES
(1, 1, '10.3 inches'),
(1, 2, '32 GB'),
(1, 3, 'Up to 14 days'),
(1, 4, 'Wi-Fi, Bluetooth 5.0'),
(1, 5, 'Black'),
(1, 7, '410g');

-- Slate Sleeve features
INSERT INTO product_features (product_id, feature_type_id, value) VALUES
(2, 5, 'Black, Brown, Navy'),
(2, 6, 'Premium synthetic leather'),
(2, 8, 'Slate tablet');

-- Studio Stylus Pen features
INSERT INTO product_features (product_id, feature_type_id, value) VALUES
(3, 5, 'Silver'),
(3, 6, 'Aluminum'),
(3, 8, 'Slate tablet');

-- Canvas tablet features
INSERT INTO product_features (product_id, feature_type_id, value) VALUES
(10, 1, '10.9 inches'),
(10, 2, '64 GB'),
(10, 3, 'Up to 12 hours'),
(10, 4, 'Wi-Fi 6, Bluetooth 5.2'),
(10, 5, 'Space Gray, Silver'),
(10, 7, '460g');

-- ===========================
-- PRODUCT STOCK
-- ===========================
INSERT INTO product_stock (product_id, quantity) VALUES
(1, 25),
(2, 42),
(3, 38),
(4, 15),
(5, 50),
(6, 8),  -- Low stock
(7, 0),  -- Out of stock
(8, 30),
(9, 12),
(10, 5), -- Low stock
(11, 0), -- Out of stock
(12, 3); -- Low stock

-- ===========================
-- USERS
-- ===========================
-- Synthetic demo identities. Password for all users: DemoOnly!2026 (Werkzeug PBKDF2 hash).
INSERT INTO users (id, name, email, password, email_verified, address, noted_cash, role, created_at, last_login) VALUES
(1, 'Demo Admin', 'admin@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Demo Office, Example City', 0.00, 1, '2024-12-01 09:00:00', '2025-06-28 14:30:00'),
(2, 'Demo User 01', 'demo01@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 1, Example City', 25.00, 2, '2025-01-15 14:22:00', '2025-06-29 08:45:00'),
(3, 'Demo User 02', 'demo02@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 2, Example City', 50.00, 2, '2025-02-02 10:10:00', '2025-06-30 12:15:00'),
(4, 'Demo User 03', 'demo03@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 3, Example City', 10.00, 2, '2025-02-15 16:45:00', '2025-06-25 18:20:00'),
(5, 'Demo User 04', 'demo04@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 4, Example City', 0.00, 2, '2025-03-01 09:30:00', '2025-06-27 20:10:00'),
(6, 'Demo User 05', 'demo05@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 5, Example City', 5.00, 2, '2025-03-10 11:20:00', '2025-06-24 15:30:00'),
(7, 'Demo User 06', 'demo06@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 6, Example City', 15.00, 2, '2025-04-05 13:15:00', '2025-06-28 09:45:00'),
(8, 'Demo User 07', 'demo07@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 7, Example City', 30.00, 2, '2025-04-20 15:40:00', '2025-06-26 14:20:00'),
(9, 'Demo User 08', 'demo08@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 8, Example City', 0.00, 2, '2025-05-10 10:30:00', '2025-06-23 11:15:00'),
(10, 'Demo User 09', 'demo09@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 9, Example City', 20.00, 2, '2025-05-25 12:50:00', '2025-06-29 17:25:00'),
(11, 'Demo User 10', 'demo10@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 10, Example City', 0.00, 2, '2025-06-01 14:10:00', '2025-06-30 10:05:00'),
(12, 'Demo User 11', 'demo11@example.com', 'pbkdf2:sha256:260000$noteddemo$5b58a34f0ea45e7bf9b4f754ef348b0f8f158c45460b1a665e1ff62285d93276', 1, 'Example Street 11, Example City', 0.00, 2, '2025-06-15 09:20:00', '2025-06-29 16:40:00');

-- ===========================
-- NOTED CASH TRANSACTIONS
-- ===========================
INSERT INTO noted_cash_transactions (user_id, change_amount, reason, created_at) VALUES
(2, 25.00, 'Welcome bonus', '2025-01-15 14:30:00'),
(3, 50.00, 'Referral reward', '2025-02-02 10:20:00'),
(4, 10.00, 'Newsletter signup', '2025-02-15 17:00:00'),
(6, 5.00, 'Survey completion', '2025-03-10 11:45:00'),
(7, 15.00, 'Product review reward', '2025-04-05 13:30:00'),
(8, 30.00, 'Contest winner', '2025-04-20 16:00:00'),
(10, 20.00, 'Customer loyalty bonus', '2025-05-25 13:10:00');

-- ===========================
-- ORDERS
-- ===========================
INSERT INTO orders (id, user_id, order_date, total, shipping_method, payment_method, status, created_at) VALUES
(1, 3, '2025-01-05 10:30:00', 479.00, 'Standard', 'Credit Card', 'completed', '2025-01-05 10:30:00'),
(2, 2, '2025-01-15 14:45:00', 69.00, 'Express', 'Demo Wallet', 'completed', '2025-01-15 14:45:00'),
(3, 5, '2025-02-01 09:20:00', 548.00, 'Standard', 'Credit Card', 'completed', '2025-02-01 09:20:00'),
(4, 8, '2025-02-10 16:15:00', 119.98, 'Standard', 'Credit Card', 'completed', '2025-02-10 16:15:00'),
(5, 4, '2025-02-20 11:40:00', 89.00, 'Express', 'Demo Wallet', 'completed', '2025-02-20 11:40:00'),
(6, 3, '2025-03-05 13:25:00', 9.99, 'Standard', 'Credit Card', 'completed', '2025-03-05 13:25:00'),
(7, 6, '2025-03-15 15:10:00', 499.00, 'Express', 'Credit Card', 'completed', '2025-03-15 15:10:00'),
(8, 7, '2025-03-25 10:45:00', 49.00, 'Standard', 'Demo Wallet', 'completed', '2025-03-25 10:45:00'),
(9, 2, '2025-04-05 12:30:00', 7.99, 'Standard', 'Credit Card', 'completed', '2025-04-05 12:30:00'),
(10, 9, '2025-04-15 14:20:00', 479.00, 'Express', 'Credit Card', 'completed', '2025-04-15 14:20:00'),
(11, 10, '2025-04-25 16:05:00', 99.00, 'Standard', 'Demo Wallet', 'completed', '2025-04-25 16:05:00'),
(12, 5, '2025-05-05 09:50:00', 59.00, 'Express', 'Credit Card', 'completed', '2025-05-05 09:50:00'),
(13, 4, '2025-05-15 11:35:00', 14.99, 'Standard', 'Demo Wallet', 'completed', '2025-05-15 11:35:00'),
(14, 8, '2025-05-25 13:15:00', 19.99, 'Standard', 'Credit Card', 'completed', '2025-05-25 13:15:00'),
(15, 3, '2025-06-05 15:00:00', 499.00, 'Express', 'Credit Card', 'completed', '2025-06-05 15:00:00'),
(16, 7, '2025-06-15 16:45:00', 12.00, 'Standard', 'Demo Wallet', 'completed', '2025-06-15 16:45:00'),
(17, 2, '2025-06-25 10:20:00', 158.00, 'Express', 'Credit Card', 'completed', '2025-06-25 10:20:00'),
(18, 11, '2025-06-28 12:10:00', 537.99, 'Standard', 'Credit Card', 'processing', '2025-06-28 12:10:00'),
(19, 6, '2025-06-29 14:30:00', 59.00, 'Express', 'Demo Wallet', 'processing', '2025-06-29 14:30:00'),
(20, 12, '2025-06-30 09:40:00', 19.99, 'Standard', 'Credit Card', 'pending', '2025-06-30 09:40:00'),
(21, 10, '2025-06-30 11:25:00', 69.00, 'Standard', 'Credit Card', 'pending', '2025-06-30 11:25:00');

-- ===========================
-- ORDER ITEMS
-- ===========================
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 479.00),
(2, 2, 1, 69.00),
(3, 1, 1, 479.00),
(3, 3, 1, 49.00),
(3, 4, 2, 10.00),
(4, 3, 1, 49.00),
(4, 6, 1, 7.99),
(4, 7, 1, 14.99),
(4, 5, 3, 9.99),
(4, 4, 2, 10.00),
(5, 9, 1, 89.00),
(6, 5, 1, 9.99),
(7, 10, 1, 499.00),
(8, 3, 1, 49.00),
(9, 6, 1, 7.99),
(10, 1, 1, 479.00),
(11, 12, 1, 99.00),
(12, 11, 1, 59.00),
(13, 7, 1, 14.99),
(14, 8, 1, 19.99),
(15, 10, 1, 499.00),
(16, 4, 1, 12.00),
(17, 3, 1, 49.00),
(17, 2, 1, 69.00),
(17, 4, 2, 12.00),
(17, 5, 1, 9.99),
(17, 6, 1, 7.99),
(18, 1, 1, 479.00),
(18, 11, 1, 59.00),
(19, 11, 1, 59.00),
(20, 8, 1, 19.99),
(21, 2, 1, 69.00);

-- ===========================
-- PAYMENT INFO
-- ===========================
INSERT INTO payment_info (order_id, card_last4, card_brand, paid, payment_date) VALUES
(1, NULL, 'Demo Card', TRUE, '2025-01-05 10:35:00'),
(2, NULL, 'Demo Wallet', TRUE, '2025-01-15 14:50:00'),
(3, NULL, 'Demo Card', TRUE, '2025-02-01 09:25:00'),
(4, NULL, 'Demo Card', TRUE, '2025-02-10 16:20:00'),
(5, NULL, 'Demo Wallet', TRUE, '2025-02-20 11:45:00'),
(6, NULL, 'Demo Card', TRUE, '2025-03-05 13:30:00'),
(7, NULL, 'Demo Card', TRUE, '2025-03-15 15:15:00'),
(8, NULL, 'Demo Wallet', TRUE, '2025-03-25 10:50:00'),
(9, NULL, 'Demo Card', TRUE, '2025-04-05 12:35:00'),
(10, NULL, 'Demo Card', TRUE, '2025-04-15 14:25:00'),
(11, NULL, 'Demo Wallet', TRUE, '2025-04-25 16:10:00'),
(12, NULL, 'Demo Card', TRUE, '2025-05-05 09:55:00'),
(13, NULL, 'Demo Wallet', TRUE, '2025-05-15 11:40:00'),
(14, NULL, 'Demo Card', TRUE, '2025-05-25 13:20:00'),
(15, NULL, 'Demo Card', TRUE, '2025-06-05 15:05:00'),
(16, NULL, 'Demo Wallet', TRUE, '2025-06-15 16:50:00'),
(17, NULL, 'Demo Card', TRUE, '2025-06-25 10:25:00'),
(18, NULL, 'Demo Card', FALSE, NULL),
(19, NULL, 'Demo Wallet', FALSE, NULL),
(20, NULL, 'Demo Card', FALSE, NULL),
(21, NULL, 'Demo Card', FALSE, NULL);

-- ===========================
-- SHIPPING ADDRESSES
-- ===========================
INSERT INTO shipping_addresses (order_id, first_name, last_name, street_address, city, state, zip_code, country, phone, email) VALUES
(1, 'Demo', 'User 02', 'Example Street 2', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo02@example.com'),
(2, 'Demo', 'User 01', 'Example Street 1', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo01@example.com'),
(3, 'Demo', 'User 04', 'Example Street 4', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo04@example.com'),
(4, 'Demo', 'User 07', 'Example Street 7', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo07@example.com'),
(5, 'Demo', 'User 03', 'Example Street 3', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo03@example.com'),
(6, 'Demo', 'User 02', 'Example Street 2', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo02@example.com'),
(7, 'Demo', 'User 05', 'Example Street 5', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo05@example.com'),
(8, 'Demo', 'User 06', 'Example Street 6', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo06@example.com'),
(9, 'Demo', 'User 01', 'Example Street 1', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo01@example.com'),
(10, 'Demo', 'User 08', 'Example Street 8', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo08@example.com'),
(11, 'Demo', 'User 09', 'Example Street 9', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo09@example.com'),
(12, 'Demo', 'User 04', 'Example Street 4', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo04@example.com'),
(13, 'Demo', 'User 03', 'Example Street 3', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo03@example.com'),
(14, 'Demo', 'User 07', 'Example Street 7', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo07@example.com'),
(15, 'Demo', 'User 02', 'Example Street 2', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo02@example.com'),
(16, 'Demo', 'User 06', 'Example Street 6', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo06@example.com'),
(17, 'Demo', 'User 01', 'Example Street 1', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo01@example.com'),
(18, 'Demo', 'User 10', 'Example Street 10', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo10@example.com'),
(19, 'Demo', 'User 05', 'Example Street 5', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo05@example.com'),
(20, 'Demo', 'User 02', 'Example Street 11', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo11@example.com'),
(21, 'Demo', 'User 09', 'Example Street 9', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo09@example.com');

-- ===========================
-- BILLING ADDRESSES (same as shipping for simplicity)
-- ===========================
INSERT INTO billing_addresses (order_id, first_name, last_name, street_address, city, state, zip_code, country, phone, email) VALUES
(1, 'Demo', 'User 02', 'Example Street 2', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo02@example.com'),
(2, 'Demo', 'User 01', 'Example Street 1', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo01@example.com'),
(3, 'Demo', 'User 04', 'Example Street 4', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo04@example.com'),
(4, 'Demo', 'User 07', 'Example Street 7', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo07@example.com'),
(5, 'Demo', 'User 03', 'Example Street 3', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo03@example.com'),
(6, 'Demo', 'User 02', 'Example Street 2', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo02@example.com'),
(7, 'Demo', 'User 05', 'Example Street 5', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo05@example.com'),
(8, 'Demo', 'User 06', 'Example Street 6', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo06@example.com'),
(9, 'Demo', 'User 01', 'Example Street 1', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo01@example.com'),
(10, 'Demo', 'User 08', 'Example Street 8', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo08@example.com'),
(11, 'Demo', 'User 09', 'Example Street 9', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo09@example.com'),
(12, 'Demo', 'User 04', 'Example Street 4', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo04@example.com'),
(13, 'Demo', 'User 03', 'Example Street 3', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo03@example.com'),
(14, 'Demo', 'User 07', 'Example Street 7', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo07@example.com'),
(15, 'Demo', 'User 02', 'Example Street 2', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo02@example.com'),
(16, 'Demo', 'User 06', 'Example Street 6', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo06@example.com'),
(17, 'Demo', 'User 01', 'Example Street 1', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo01@example.com'),
(18, 'Demo', 'User 10', 'Example Street 10', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo10@example.com'),
(19, 'Demo', 'User 05', 'Example Street 5', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo05@example.com'),
(20, 'Demo', 'User 02', 'Example Street 11', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo11@example.com'),
(21, 'Demo', 'User 09', 'Example Street 9', 'Example City', 'Example City', '0000-000', 'Portugal', '+351000000000', 'demo09@example.com');

-- ===========================
-- CART (current active carts)
-- ===========================
INSERT INTO cart (user_id, product_id, quantity, added_at) VALUES
(2, 10, 1, '2025-06-28 15:30:00'),
(3, 12, 1, '2025-06-29 10:45:00'),
(4, 3, 1, '2025-06-27 14:20:00'),
(4, 2, 1, '2025-06-27 14:22:00'),
(5, 8, 2, '2025-06-30 09:15:00'),
(7, 1, 1, '2025-06-29 16:40:00'),
(8, 11, 1, '2025-06-28 11:25:00'),
(9, 4, 2, '2025-06-30 13:10:00'),
(11, 7, 1, '2025-06-30 10:05:00');

-- ===========================
-- DISCOUNTS
-- ===========================
INSERT INTO discounts (code, amount, is_percentage, is_active, created_at) VALUES
('WELCOME10', 10.00, TRUE, TRUE, '2025-01-01 00:00:00'),
('SUMMER25', 25.00, TRUE, TRUE, '2025-06-01 00:00:00'),
('NOTED5', 5.00, FALSE, TRUE, '2025-02-15 00:00:00'),
('FLASH20', 20.00, TRUE, FALSE, '2025-03-10 00:00:00'),
('FREEDEL', 4.99, FALSE, TRUE, '2025-04-01 00:00:00');