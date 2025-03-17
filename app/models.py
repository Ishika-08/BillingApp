from app.database import execute_query

class Customer:
    # """Handles customer operations."""
    @staticmethod
    def add_customer(name, email):
        """Adds a new customer if not exists and returns the customer ID."""
        query = "SELECT id FROM customers WHERE email = %s"
        customer = execute_query(query, (email,), fetch=True)

        if customer:
            return customer[0][0]
        
        insert_query = "INSERT INTO customers (name, email) VALUES (%s, %s)"
        execute_query(insert_query, (name, email))

        return execute_query(query, (email,), fetch=True)[0][0]

class Bill:
    # """Handles bill operations."""
    @staticmethod
    def add_bill(customer_id, amount):
        """Inserts a new bill for a customer."""
        query = "INSERT INTO bills (customer_id, amount) VALUES (%s, %s)"
        execute_query(query, (customer_id, amount))

    @staticmethod
    def get_bills():
        # """Retrieves all bills along with customer details."""
        query = """
        SELECT customers.name, customers.email, bills.amount 
        FROM bills 
        JOIN customers ON bills.customer_id = customers.id
        """
        return execute_query(query, fetch=True)
