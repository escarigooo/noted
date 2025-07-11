-- ============================
-- Tabela de Coleções de Produto
-- ============================
INSERT INTO product_collections (name, description) VALUES 
('Supernote', 'A refined digital writing collection with the Supernote tablet and accessories.'),
('Milestones', 'Organize thoughts, create goals, and capture life''s achievements with Milestones tools.'),
('Vision', 'A collection of advanced digital writing tools designed for immersive experiences.');

-- ===========================
-- SUPERNOTE COLLECTION PRODUCTS
-- ===========================

-- 1. Supernote Tablet
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    1,
    'Supernote',
    'The Supernote tablet combines modern digital writing with elegant design, ideal for notes, sketches, and productivity.',
    479.00,
    'supernote.png',
    1,
    1
);

INSERT INTO product_images (product_id, path, caption) VALUES
(1, 'supernote1.png', 'Front view'),
(1, 'supernote2.png', 'Back view'),
(1, 'supernote3.png', 'Side profile'),
(1, 'supernote4.png', 'Top angle'),
(1, 'supernote5.png', 'With accessories');

-- 2. Supernote Case
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    2,
    'Supernote Case',
    'Premium protective folio case for your Supernote tablet, ensuring safety and elegance on the go.',
    69.00,
    'supernote_case.png',
    4,
    1
);

-- 3. Supernote Flow Pen
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    3,
    'Supernote Flow',
    'A smooth, digital ink pen designed for precision and comfort, tailored for the Supernote experience.',
    49.00,
    'supernote_flow.png',
    2,
    1
);

-- 4. Supernote Flow Refill
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    4,
    'Supernote Flow Refill',
    'High-quality refill tips for your Supernote Flow pen. Long-lasting and friction-optimized.',
    12.00,
    'supernote_flow_refill.png',
    4,
    1
);

-- ===========================
-- MILESTONES COLLECTION PRODUCTS
-- ===========================

-- 5. Cable
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (5, 'Cable', 'High-quality USB-C cable for charging and data transfer.', 9.99, 'cable.png', 4, 2);

INSERT INTO product_images (product_id, path, caption) VALUES
(5, 'cable1.png', 'Folded cable');

-- 6. Marker Tips
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (6, 'Marker Tips', 'Set of replacement marker tips for your digital pen.', 7.99, 'markertips.png', 4, 2);

-- 7. Milemarker
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (7, 'Milemarker', 'Digital productivity planner with structured pages.', 14.99, 'milemarker.png', 2, 2);

INSERT INTO product_images (product_id, path, caption) VALUES
(7, 'milemarker1.png', 'Cover detail');

-- 8. Milestones Journal
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (8, 'Milestones', 'Notebook for recording milestones and memories.', 19.99, 'milestones.png', 1, 2);

INSERT INTO product_images (product_id, path, caption) VALUES
(8, 'milestones1.png', 'Writing inside');

-- 9. Type Folio
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (9, 'Type Mile', 'Keyboard folio case for your tablet.', 89.00, 'type_mile.png', 3, 2);

INSERT INTO product_images (product_id, path, caption) VALUES
(9, 'type_mile1.png', 'Front fold'),
(9, 'type_mile2.png', 'Side profile'),
(9, 'type_mile3.png', 'Keyboard in the back'),
(9, 'type_mile4.png', 'Disconnected keyboard'),
(9, 'type_mile5.png', 'Front view'),
(9, 'type_mile6.png', 'Back view');

-- ===========================
-- VISION COLLECTION PRODUCTS
-- ===========================

-- 10. Vision Tablet
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    10,
    'Vision',
    'A powerful and elegant digital notebook for immersive writing and sketching.',
    499.00,
    'vision.png',
    1,
    3
);

INSERT INTO product_images (product_id, path, caption) VALUES
(10, 'vision1.png', 'Back view');

-- 11. Vision Marker
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    11,
    'Vision Marker',
    'A sleek pen with high-precision digital ink for the Vision tablet.',
    59.00,
    'vision_marker.png',
    2,
    3
);

-- 12. Type Vision
INSERT INTO products (id, name, description, price, image, category_id, collection_id)
VALUES (
    12,
    'Type Vision',
    'Ergonomic keyboard folio designed exclusively for Vision tablets.',
    99.00,
    'type_vision.png',
    3,
    3
);

INSERT INTO product_images (product_id, path, caption) VALUES
(11, 'vision_marker1.png', 'Tablet with marker in use'),
(11, 'vision_marker2.png', 'Tablet and marker ');


INSERT INTO product_images (product_id, path, caption) VALUES
(12, 'type_vision1.png', 'Front fold'),
(12, 'type_vision2.png', 'Open with keyboard'),
(12, 'type_vision3.png', 'Side profile'),
(12, 'type_vision4.png', 'Back closed'),
(12, 'type_vision5.png', 'Tablet standing');

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
-- Supernote features
INSERT INTO product_features (product_id, feature_type_id, value) VALUES
(1, 1, '10.3 inches'),
(1, 2, '32 GB'),
(1, 3, 'Up to 14 days'),
(1, 4, 'Wi-Fi, Bluetooth 5.0'),
(1, 5, 'Black'),
(1, 7, '410g');

-- Supernote Case features
INSERT INTO product_features (product_id, feature_type_id, value) VALUES
(2, 5, 'Black, Brown, Navy'),
(2, 6, 'Premium synthetic leather'),
(2, 8, 'Supernote tablet');

-- Supernote Flow Pen features
INSERT INTO product_features (product_id, feature_type_id, value) VALUES
(3, 5, 'Silver'),
(3, 6, 'Aluminum'),
(3, 8, 'Supernote tablet');

-- Vision tablet features
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
-- Password for all users is 'password123' - hashed with bcrypt
INSERT INTO users (id, name, email, password, address, noted_cash, role, created_at, last_login) VALUES
(1, 'Admin User', 'admin@noted.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Noted HQ, Lisboa, Portugal', 0.00, 1, '2024-12-01 09:00:00', '2025-06-28 14:30:00'),
(2, 'João Silva', 'joao@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Rua das Flores 123, Lisboa', 25.00, 2, '2025-01-15 14:22:00', '2025-06-29 08:45:00'),
(3, 'Maria Santos', 'maria@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Avenida da República 45, Porto', 50.00, 2, '2025-02-02 10:10:00', '2025-06-30 12:15:00'),
(4, 'Carlos Mendes', 'carlos@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Rua do Comércio 78, Faro', 10.00, 2, '2025-02-15 16:45:00', '2025-06-25 18:20:00'),
(5, 'Ana Costa', 'ana@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Avenida Central 22, Braga', 0.00, 2, '2025-03-01 09:30:00', '2025-06-27 20:10:00'),
(6, 'Pedro Oliveira', 'pedro@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Rua da Liberdade 56, Coimbra', 5.00, 2, '2025-03-10 11:20:00', '2025-06-24 15:30:00'),
(7, 'Sofia Rodrigues', 'sofia@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Largo do Rossio 9, Lisboa', 15.00, 2, '2025-04-05 13:15:00', '2025-06-28 09:45:00'),
(8, 'Miguel Fernandes', 'miguel@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Avenida do Mar 33, Setúbal', 30.00, 2, '2025-04-20 15:40:00', '2025-06-26 14:20:00'),
(9, 'Inês Martins', 'ines@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Rua das Oliveiras 17, Évora', 0.00, 2, '2025-05-10 10:30:00', '2025-06-23 11:15:00'),
(10, 'Tiago Pereira', 'tiago@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Praça Central 4, Aveiro', 20.00, 2, '2025-05-25 12:50:00', '2025-06-29 17:25:00'),
(11, 'Marta Almeida', 'marta@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Rua dos Clérigos 27, Porto', 0.00, 2, '2025-06-01 14:10:00', '2025-06-30 10:05:00'),
(12, 'Ricardo Santos', 'ricardo@email.com', '$2y$10$MUJ5kzRnNxk3JJL60dZ6N.m.9vUhJGLqiG5vSWqU9XP9xUuvr/b9G', 'Avenida da Praia 11, Faro', 0.00, 2, '2025-06-15 09:20:00', '2025-06-29 16:40:00');

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
(2, 2, '2025-01-15 14:45:00', 69.00, 'Express', 'PayPal', 'completed', '2025-01-15 14:45:00'),
(3, 5, '2025-02-01 09:20:00', 548.00, 'Standard', 'Credit Card', 'completed', '2025-02-01 09:20:00'),
(4, 8, '2025-02-10 16:15:00', 119.98, 'Standard', 'Credit Card', 'completed', '2025-02-10 16:15:00'),
(5, 4, '2025-02-20 11:40:00', 89.00, 'Express', 'PayPal', 'completed', '2025-02-20 11:40:00'),
(6, 3, '2025-03-05 13:25:00', 9.99, 'Standard', 'Credit Card', 'completed', '2025-03-05 13:25:00'),
(7, 6, '2025-03-15 15:10:00', 499.00, 'Express', 'Credit Card', 'completed', '2025-03-15 15:10:00'),
(8, 7, '2025-03-25 10:45:00', 49.00, 'Standard', 'PayPal', 'completed', '2025-03-25 10:45:00'),
(9, 2, '2025-04-05 12:30:00', 7.99, 'Standard', 'Credit Card', 'completed', '2025-04-05 12:30:00'),
(10, 9, '2025-04-15 14:20:00', 479.00, 'Express', 'Credit Card', 'completed', '2025-04-15 14:20:00'),
(11, 10, '2025-04-25 16:05:00', 99.00, 'Standard', 'PayPal', 'completed', '2025-04-25 16:05:00'),
(12, 5, '2025-05-05 09:50:00', 59.00, 'Express', 'Credit Card', 'completed', '2025-05-05 09:50:00'),
(13, 4, '2025-05-15 11:35:00', 14.99, 'Standard', 'PayPal', 'completed', '2025-05-15 11:35:00'),
(14, 8, '2025-05-25 13:15:00', 19.99, 'Standard', 'Credit Card', 'completed', '2025-05-25 13:15:00'),
(15, 3, '2025-06-05 15:00:00', 499.00, 'Express', 'Credit Card', 'completed', '2025-06-05 15:00:00'),
(16, 7, '2025-06-15 16:45:00', 12.00, 'Standard', 'PayPal', 'completed', '2025-06-15 16:45:00'),
(17, 2, '2025-06-25 10:20:00', 158.00, 'Express', 'Credit Card', 'completed', '2025-06-25 10:20:00'),
(18, 11, '2025-06-28 12:10:00', 537.99, 'Standard', 'Credit Card', 'processing', '2025-06-28 12:10:00'),
(19, 6, '2025-06-29 14:30:00', 59.00, 'Express', 'PayPal', 'processing', '2025-06-29 14:30:00'),
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
(1, '4242', 'Visa', TRUE, '2025-01-05 10:35:00'),
(2, NULL, 'PayPal', TRUE, '2025-01-15 14:50:00'),
(3, '5678', 'Mastercard', TRUE, '2025-02-01 09:25:00'),
(4, '9012', 'Visa', TRUE, '2025-02-10 16:20:00'),
(5, NULL, 'PayPal', TRUE, '2025-02-20 11:45:00'),
(6, '3456', 'Mastercard', TRUE, '2025-03-05 13:30:00'),
(7, '7890', 'Visa', TRUE, '2025-03-15 15:15:00'),
(8, NULL, 'PayPal', TRUE, '2025-03-25 10:50:00'),
(9, '1234', 'Visa', TRUE, '2025-04-05 12:35:00'),
(10, '5678', 'Mastercard', TRUE, '2025-04-15 14:25:00'),
(11, NULL, 'PayPal', TRUE, '2025-04-25 16:10:00'),
(12, '9012', 'Visa', TRUE, '2025-05-05 09:55:00'),
(13, NULL, 'PayPal', TRUE, '2025-05-15 11:40:00'),
(14, '3456', 'Mastercard', TRUE, '2025-05-25 13:20:00'),
(15, '7890', 'Visa', TRUE, '2025-06-05 15:05:00'),
(16, NULL, 'PayPal', TRUE, '2025-06-15 16:50:00'),
(17, '1234', 'Visa', TRUE, '2025-06-25 10:25:00'),
(18, '5678', 'Mastercard', FALSE, NULL),
(19, NULL, 'PayPal', FALSE, NULL),
(20, '9012', 'Visa', FALSE, NULL),
(21, '3456', 'Mastercard', FALSE, NULL);

-- ===========================
-- SHIPPING ADDRESSES
-- ===========================
INSERT INTO shipping_addresses (order_id, first_name, last_name, street_address, city, state, zip_code, country, phone, email) VALUES
(1, 'Maria', 'Santos', 'Avenida da República 45', 'Porto', 'Porto', '4000-123', 'Portugal', '+351912345678', 'maria@email.com'),
(2, 'João', 'Silva', 'Rua das Flores 123', 'Lisboa', 'Lisboa', '1000-123', 'Portugal', '+351923456789', 'joao@email.com'),
(3, 'Ana', 'Costa', 'Avenida Central 22', 'Braga', 'Braga', '4700-123', 'Portugal', '+351934567890', 'ana@email.com'),
(4, 'Miguel', 'Fernandes', 'Avenida do Mar 33', 'Setúbal', 'Setúbal', '2900-123', 'Portugal', '+351945678901', 'miguel@email.com'),
(5, 'Carlos', 'Mendes', 'Rua do Comércio 78', 'Faro', 'Faro', '8000-123', 'Portugal', '+351956789012', 'carlos@email.com'),
(6, 'Maria', 'Santos', 'Avenida da República 45', 'Porto', 'Porto', '4000-123', 'Portugal', '+351912345678', 'maria@email.com'),
(7, 'Pedro', 'Oliveira', 'Rua da Liberdade 56', 'Coimbra', 'Coimbra', '3000-123', 'Portugal', '+351967890123', 'pedro@email.com'),
(8, 'Sofia', 'Rodrigues', 'Largo do Rossio 9', 'Lisboa', 'Lisboa', '1100-123', 'Portugal', '+351978901234', 'sofia@email.com'),
(9, 'João', 'Silva', 'Rua das Flores 123', 'Lisboa', 'Lisboa', '1000-123', 'Portugal', '+351923456789', 'joao@email.com'),
(10, 'Inês', 'Martins', 'Rua das Oliveiras 17', 'Évora', 'Évora', '7000-123', 'Portugal', '+351989012345', 'ines@email.com'),
(11, 'Tiago', 'Pereira', 'Praça Central 4', 'Aveiro', 'Aveiro', '3800-123', 'Portugal', '+351990123456', 'tiago@email.com'),
(12, 'Ana', 'Costa', 'Avenida Central 22', 'Braga', 'Braga', '4700-123', 'Portugal', '+351934567890', 'ana@email.com'),
(13, 'Carlos', 'Mendes', 'Rua do Comércio 78', 'Faro', 'Faro', '8000-123', 'Portugal', '+351956789012', 'carlos@email.com'),
(14, 'Miguel', 'Fernandes', 'Avenida do Mar 33', 'Setúbal', 'Setúbal', '2900-123', 'Portugal', '+351945678901', 'miguel@email.com'),
(15, 'Maria', 'Santos', 'Avenida da República 45', 'Porto', 'Porto', '4000-123', 'Portugal', '+351912345678', 'maria@email.com'),
(16, 'Sofia', 'Rodrigues', 'Largo do Rossio 9', 'Lisboa', 'Lisboa', '1100-123', 'Portugal', '+351978901234', 'sofia@email.com'),
(17, 'João', 'Silva', 'Rua das Flores 123', 'Lisboa', 'Lisboa', '1000-123', 'Portugal', '+351923456789', 'joao@email.com'),
(18, 'Marta', 'Almeida', 'Rua dos Clérigos 27', 'Porto', 'Porto', '4000-456', 'Portugal', '+351901234567', 'marta@email.com'),
(19, 'Pedro', 'Oliveira', 'Rua da Liberdade 56', 'Coimbra', 'Coimbra', '3000-123', 'Portugal', '+351967890123', 'pedro@email.com'),
(20, 'Ricardo', 'Santos', 'Avenida da Praia 11', 'Faro', 'Faro', '8000-456', 'Portugal', '+351912345678', 'ricardo@email.com'),
(21, 'Tiago', 'Pereira', 'Praça Central 4', 'Aveiro', 'Aveiro', '3800-123', 'Portugal', '+351990123456', 'tiago@email.com');

-- ===========================
-- BILLING ADDRESSES (same as shipping for simplicity)
-- ===========================
INSERT INTO billing_addresses (order_id, first_name, last_name, street_address, city, state, zip_code, country, phone, email) VALUES
(1, 'Maria', 'Santos', 'Avenida da República 45', 'Porto', 'Porto', '4000-123', 'Portugal', '+351912345678', 'maria@email.com'),
(2, 'João', 'Silva', 'Rua das Flores 123', 'Lisboa', 'Lisboa', '1000-123', 'Portugal', '+351923456789', 'joao@email.com'),
(3, 'Ana', 'Costa', 'Avenida Central 22', 'Braga', 'Braga', '4700-123', 'Portugal', '+351934567890', 'ana@email.com'),
(4, 'Miguel', 'Fernandes', 'Avenida do Mar 33', 'Setúbal', 'Setúbal', '2900-123', 'Portugal', '+351945678901', 'miguel@email.com'),
(5, 'Carlos', 'Mendes', 'Rua do Comércio 78', 'Faro', 'Faro', '8000-123', 'Portugal', '+351956789012', 'carlos@email.com'),
(6, 'Maria', 'Santos', 'Avenida da República 45', 'Porto', 'Porto', '4000-123', 'Portugal', '+351912345678', 'maria@email.com'),
(7, 'Pedro', 'Oliveira', 'Rua da Liberdade 56', 'Coimbra', 'Coimbra', '3000-123', 'Portugal', '+351967890123', 'pedro@email.com'),
(8, 'Sofia', 'Rodrigues', 'Largo do Rossio 9', 'Lisboa', 'Lisboa', '1100-123', 'Portugal', '+351978901234', 'sofia@email.com'),
(9, 'João', 'Silva', 'Rua das Flores 123', 'Lisboa', 'Lisboa', '1000-123', 'Portugal', '+351923456789', 'joao@email.com'),
(10, 'Inês', 'Martins', 'Rua das Oliveiras 17', 'Évora', 'Évora', '7000-123', 'Portugal', '+351989012345', 'ines@email.com'),
(11, 'Tiago', 'Pereira', 'Praça Central 4', 'Aveiro', 'Aveiro', '3800-123', 'Portugal', '+351990123456', 'tiago@email.com'),
(12, 'Ana', 'Costa', 'Avenida Central 22', 'Braga', 'Braga', '4700-123', 'Portugal', '+351934567890', 'ana@email.com'),
(13, 'Carlos', 'Mendes', 'Rua do Comércio 78', 'Faro', 'Faro', '8000-123', 'Portugal', '+351956789012', 'carlos@email.com'),
(14, 'Miguel', 'Fernandes', 'Avenida do Mar 33', 'Setúbal', 'Setúbal', '2900-123', 'Portugal', '+351945678901', 'miguel@email.com'),
(15, 'Maria', 'Santos', 'Avenida da República 45', 'Porto', 'Porto', '4000-123', 'Portugal', '+351912345678', 'maria@email.com'),
(16, 'Sofia', 'Rodrigues', 'Largo do Rossio 9', 'Lisboa', 'Lisboa', '1100-123', 'Portugal', '+351978901234', 'sofia@email.com'),
(17, 'João', 'Silva', 'Rua das Flores 123', 'Lisboa', 'Lisboa', '1000-123', 'Portugal', '+351923456789', 'joao@email.com'),
(18, 'Marta', 'Almeida', 'Rua dos Clérigos 27', 'Porto', 'Porto', '4000-456', 'Portugal', '+351901234567', 'marta@email.com'),
(19, 'Pedro', 'Oliveira', 'Rua da Liberdade 56', 'Coimbra', 'Coimbra', '3000-123', 'Portugal', '+351967890123', 'pedro@email.com'),
(20, 'Ricardo', 'Santos', 'Avenida da Praia 11', 'Faro', 'Faro', '8000-456', 'Portugal', '+351912345678', 'ricardo@email.com'),
(21, 'Tiago', 'Pereira', 'Praça Central 4', 'Aveiro', 'Aveiro', '3800-123', 'Portugal', '+351990123456', 'tiago@email.com');

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