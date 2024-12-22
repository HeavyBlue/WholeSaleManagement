-------------------------------------- TABLE CREATING --------------------------------

-- Customer table
CREATE TABLE Customer
(
    Customer_ID  SERIAL PRIMARY KEY,
    First_Name   VARCHAR(100) NOT NULL,
    Second_Name  VARCHAR(100) NOT NULL,
    Address      VARCHAR(200) NOT NULL,
    Phone_Number VARCHAR(50)  NOT NULL,
    Email        VARCHAR(50)  NOT NULL,
    Image        BYTEA        NOT NULL
);

-- Item table
CREATE TABLE Item
(
    Item_ID  SERIAL PRIMARY KEY,
    Name     VARCHAR(100) NOT NULL,
    Quantity INTEGER      NOT NULL CHECK (Quantity >= 0),
    Price    DECIMAL      NOT NULL CHECK (Price > 0),
    Image    BYTEA        NOT NULL
);

-- Supplier table
CREATE TABLE Supplier
(
    Supplier_ID  SERIAL PRIMARY KEY,
    First_Name   VARCHAR(100) NOT NULL,
    Second_Name  VARCHAR(100) NOT NULL,
    Address      VARCHAR(200) NOT NULL,
    Phone_Number VARCHAR(50)  NOT NULL,
    Email        VARCHAR(50)  NOT NULL
);

-- Suppliers_Item table
CREATE TABLE Suppliers_Item
(
    Supp_Item_ID SERIAL PRIMARY KEY,
    Supplier_ID  INTEGER REFERENCES Supplier (Supplier_ID),
    Item_ID      INTEGER REFERENCES Item (Item_ID),
    Price        INTEGER NOT NULL
);


-- Order table
CREATE TABLE Orders
(
    Order_ID    SERIAL PRIMARY KEY,
    Item_ID     INTEGER REFERENCES Item (Item_ID),
    Customer_ID INTEGER REFERENCES Customer (Customer_ID),
    Quantity    INTEGER NOT NULL CHECK (Quantity > 0)
);

-- Payment table
CREATE TYPE payment_status AS ENUM ('Paid', 'Pending');
CREATE TABLE Payment
(
    Payment_ID     SERIAL PRIMARY KEY,
    Orders_ID      INTEGER REFERENCES Orders (Order_ID),
    Paid_Amount    DECIMAL NOT NULL CHECK (Paid_Amount >= 0),
    Pending_Amount DECIMAL CHECK (Pending_Amount >= 0),
    Payment_Status payment_status,
    Date           DATE    NOT NULL
);

-- Defaulter table
CREATE TABLE Defaulter
(
    Defaulter_ID SERIAL PRIMARY KEY,
    Payment_ID   INTEGER REFERENCES Payment (Payment_ID),
    Due_Date     DATE NOT NULL,
    Is_Paid      BOOLEAN DEFAULT FALSE
);

-- Inbound_Items table
CREATE TABLE Inbound_Items
(
    In_ID        SERIAL PRIMARY KEY,
    Supp_Item_ID INTEGER REFERENCES Suppliers_Item (Supp_Item_ID),
    Quantity     INTEGER NOT NULL CHECK (Quantity > 0),
    In_Date      DATE    NOT NULL
);

ALTER TABLE Orders
    ADD COLUMN Payment_ID INTEGER REFERENCES Payment (Payment_ID);


------------------------------ TRIGGER FUNCTIONS --------------------------------------

-- Tetikleyici Fonksiyonu: update_item_quantities()
CREATE OR REPLACE FUNCTION update_item_quantities()
    RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.quantity <= (SELECT quantity FROM Item WHERE NEW.Item_ID = Item_ID) THEN
        UPDATE Item
        SET quantity = quantity - NEW.quantity
        WHERE Item_ID = NEW.Item_ID;
    ELSE
        RAISE EXCEPTION 'Orders quantity must be lower than stock quantity. Orders not be created.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER update_item_quantities
    BEFORE INSERT
    ON Orders
    FOR EACH ROW
EXECUTE FUNCTION update_item_quantities();

-- Function: create_payment_entries()
CREATE OR REPLACE FUNCTION create_payment_entries()
    RETURNS TRIGGER AS
$$
DECLARE
    new_payment_id INTEGER;
BEGIN
    INSERT INTO Payment(Orders_ID, Paid_Amount, Pending_Amount, Date)
    VALUES (NEW.Order_ID, 0, (NEW.quantity * (SELECT price FROM Item WHERE Item_ID = NEW.Item_ID)), CURRENT_DATE)
    RETURNING Payment_ID INTO new_payment_id;
    UPDATE Orders
    SET Payment_ID = new_payment_id
    WHERE Order_ID = NEW.Order_ID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER create_payment_entries
    AFTER INSERT
    ON Orders
    FOR EACH ROW
EXECUTE FUNCTION create_payment_entries();

-- Function: set_payment_status()
CREATE OR REPLACE FUNCTION set_payment_status()
    RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.Pending_Amount = 0 THEN
        NEW.Payment_Status := 'Paid';
    ELSE
        NEW.Payment_Status := 'Pending';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER payment_status_trigger
    BEFORE INSERT OR UPDATE
    ON Payment
    FOR EACH ROW
EXECUTE FUNCTION set_payment_status();

-- Function: check_and_insert_defaulter()
CREATE OR REPLACE FUNCTION check_and_insert_defaulter()
    RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.Payment_Status = 'Pending' THEN
        INSERT INTO Defaulter (Payment_ID, Due_Date)
        VALUES (NEW.Payment_ID, NEW.Date + INTERVAL '30 days');
    ELSE
        UPDATE Defaulter SET is_paid = true WHERE Payment_ID = NEW.Payment_ID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER trigger_check_defaulter
    AFTER INSERT OR UPDATE
    ON Payment
    FOR EACH ROW
EXECUTE FUNCTION check_and_insert_defaulter();

--Function: calculate_monthly_profit()
CREATE OR REPLACE FUNCTION calculate_monthly_profit()
    RETURNS TABLE
            (
                year            NUMERIC,
                month           NUMERIC,
                total_sales     NUMERIC,
                total_purchases BIGINT,
                profit          NUMERIC
            )
AS
$$
BEGIN
    RETURN QUERY
        WITH MonthlySales AS (SELECT EXTRACT(YEAR FROM p.Date)  AS year,
                                     EXTRACT(MONTH FROM p.Date) AS month,
                                     SUM(p.Paid_Amount)         AS total_sales
                              FROM Payment AS p
                              GROUP BY year, month),
             MonthlyPurchases AS (SELECT EXTRACT(YEAR FROM i.In_Date)  AS year,
                                         EXTRACT(MONTH FROM i.In_Date) AS month,
                                         SUM(i.Quantity * si.Price)    AS total_purchases
                                  FROM Inbound_Items AS i
                                           JOIN Suppliers_Item AS si
                                                ON i.Supp_Item_ID = si.Supp_Item_ID
                                  GROUP BY year, month)
        SELECT s.year,
               s.month,
               COALESCE(s.total_sales, 0)                                    AS total_sales,
               COALESCE(p.total_purchases, 0)                                AS total_purchases,
               (COALESCE(s.total_sales, 0) - COALESCE(p.total_purchases, 0)) AS profit
        FROM MonthlySales AS s
                 FULL JOIN MonthlyPurchases AS p
                           ON s.year = p.year AND s.month = p.month
        ORDER BY s.year, s.month;
END;
$$ LANGUAGE plpgsql;

--Function: show_customers_whose_debts_are_past_due()
CREATE OR REPLACE FUNCTION show_customers_whose_debts_are_past_due()
    RETURNS TABLE
            (
                customer_id  INTEGER,
                order_id     INTEGER,
                first_name   VARCHAR(100),
                second_name  VARCHAR(100),
                address      VARCHAR(200),
                phone_number VARCHAR(50),
                email        VARCHAR(50),
                Image        BYTEA
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT c.customer_id,
               o.order_id,
               c.first_name,
               c.second_name,
               c.address,
               c.phone_number,
               c.email,
               c.Image
        FROM Customer AS c,
             Defaulter AS d,
             Payment AS p,
             Orders AS o
        WHERE d.due_date < CURRENT_DATE
          AND d.is_paid = false
          AND d.payment_id = p.payment_id
          AND p.orders_id = o.order_id
          AND o.customer_id = c.customer_id;
END;
$$ LANGUAGE plpgsql;

--Function: add_stock
CREATE OR REPLACE FUNCTION add_stock()
    RETURNS TRIGGER AS
$$
BEGIN
    UPDATE item
    SET quantity = quantity + NEW.quantity
    WHERE item_id = (SELECT item_id FROM suppliers_item WHERE supp_item_id = NEW.supp_item_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER add_stock
    BEFORE INSERT
    ON inbound_items
    FOR EACH ROW
EXECUTE FUNCTION add_stock();

--Function: calculate_most_profitable_item
CREATE OR REPLACE FUNCTION calculate_most_profitable_item()
    RETURNS TABLE
            (
                "item id"      INTEGER,
                "item name"    VARCHAR(100),
                income         NUMERIC,
                outcome        NUMERIC,
                net            NUMERIC,
                "net per item" NUMERIC
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT o.item_id                                                                AS "item id",
               i.name                                                                   AS "item name",
               SUM(p.paid_amount + p.pending_amount)                                    AS Income,
               SUM(o.quantity * a.average_price)                                        AS Outcome,
               SUM((p.paid_amount + p.pending_amount) - (o.quantity * a.average_price)) AS Net,
               ROUND(SUM((p.paid_amount + p.pending_amount) - (o.quantity * a.average_price)) /
                     SUM(o.quantity))                                                   AS Net_Per_Item
        FROM payment AS p,
             orders AS o,
             item AS i,
             (SELECT item_id, ROUND(AVG(price), 2) AS average_price FROM suppliers_item GROUP BY item_id) AS a
        WHERE p.orders_id = o.order_id
          AND a.item_id = o.item_id
          AND i.item_id = a.Item_ID
        GROUP BY o.item_id, i.name
        ORDER BY net_per_item DESC;
END;
$$ LANGUAGE plpgsql;


--Function: get_customer_have_unpaid_amount
CREATE OR REPLACE FUNCTION get_customer_have_unpaid_amount()
    RETURNS TABLE
            (
                customer_id    INTEGER,
                order_id       INTEGER,
                payment_id     INTEGER,
                pending_amount FLOAT,
                paid_amount    FLOAT,
                total_amount   FLOAT,
                date           DATE
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT O.Customer_ID,
               O.Order_ID,
               P.Payment_ID,
               P.Pending_Amount,
               P.Paid_Amount,
               (P.Paid_Amount + P.Pending_Amount) as total_amount,
               P.Date
        FROM Payment AS P,
             Orders AS O
        WHERE P.Orders_ID = O.Order_ID
          AND P.Payment_Status = 'Pending';
END;
$$ LANGUAGE plpgsql;
