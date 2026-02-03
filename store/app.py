from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
from datetime import datetime, timedelta
import csv
import io
from flask import Response
import os

app = Flask(__name__)
app.secret_key = 'general_store_secret_key_2024'

# Custom Jinja2 filters
@app.template_filter('days_since')
def days_since(date_str):
    if not date_str:
        return 0
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        diff = (today - date_obj).days
        return max(0, diff)
    except:
        return 0

@app.template_filter('days_until')
def days_until(date_str):
    if not date_str:
        return 0
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        diff = (date_obj - today).days
        return max(0, diff)
    except:
        return 0

# Database initialization
def init_db():
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit TEXT NOT NULL,
            purchase_price REAL NOT NULL,
            total_amount REAL NOT NULL,
            supplier_name TEXT NOT NULL,
            purchase_date TEXT NOT NULL,
            has_expiry TEXT NOT NULL,
            expiry_date TEXT,
            payment_status TEXT NOT NULL,
            paid_amount REAL NOT NULL,
            pending_amount REAL NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Helper functions
def get_db_connection():
    conn = sqlite3.connect('stock.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_expiry_status(expiry_date):
    if not expiry_date:
        return None
    
    try:
        expiry = datetime.strptime(expiry_date, '%Y-%m-%d').date()
        today = datetime.now().date()
        days_until = (expiry - today).days
        
        if days_until < 0:
            return 'expired'
        elif days_until <= 7:
            return 'near_expiry'
        else:
            return 'fresh'
    except:
        return None

# Routes
@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'admin123':  # Simple password for offline app
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get dashboard statistics
    total_products = conn.execute('SELECT COUNT(*) as count FROM stock').fetchone()['count']
    total_quantity = conn.execute('SELECT SUM(quantity) as total FROM stock').fetchone()['total'] or 0
    
    # Calculate expiry counts
    all_stock = conn.execute('SELECT * FROM stock').fetchall()
    expired_count = 0
    near_expiry_count = 0
    
    for item in all_stock:
        if item['has_expiry'] == 'YES' and item['expiry_date']:
            status = calculate_expiry_status(item['expiry_date'])
            if status == 'expired':
                expired_count += 1
            elif status == 'near_expiry':
                near_expiry_count += 1
    
    # Calculate total pending supplier payments
    pending_total = conn.execute('SELECT SUM(pending_amount) as total FROM stock WHERE payment_status = "PENDING"').fetchone()['total'] or 0
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_products=total_products,
                         total_quantity=total_quantity,
                         expired_count=expired_count,
                         near_expiry_count=near_expiry_count,
                         pending_total=pending_total)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get form data
        product_name = request.form.get('product_name')
        category = request.form.get('category')
        quantity = int(request.form.get('quantity'))
        unit = request.form.get('unit')
        purchase_price = float(request.form.get('purchase_price'))
        total_amount = float(request.form.get('total_amount'))
        supplier_name = request.form.get('supplier_name')
        purchase_date = request.form.get('purchase_date')
        has_expiry = request.form.get('has_expiry')
        expiry_date = request.form.get('expiry_date') if has_expiry == 'YES' else None
        payment_status = request.form.get('payment_status')
        paid_amount = float(request.form.get('paid_amount'))
        pending_amount = float(request.form.get('pending_amount'))
        notes = request.form.get('notes')
        
        # Timestamps
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = created_at
        
        # Insert into database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO stock (
                product_name, category, quantity, unit, purchase_price, total_amount,
                supplier_name, purchase_date, has_expiry, expiry_date, payment_status,
                paid_amount, pending_amount, notes, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (product_name, category, quantity, unit, purchase_price, total_amount,
              supplier_name, purchase_date, has_expiry, expiry_date, payment_status,
              paid_amount, pending_amount, notes, created_at, updated_at))
        
        conn.commit()
        conn.close()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('view_stock'))
    
    return render_template('add_product.html')

@app.route('/view_stock')
def view_stock():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    stock_items = conn.execute('SELECT * FROM stock ORDER BY created_at DESC').fetchall()
    
    # Add expiry status to each item
    stock_with_status = []
    for item in stock_items:
        item_dict = dict(item)
        if item['has_expiry'] == 'YES' and item['expiry_date']:
            item_dict['expiry_status'] = calculate_expiry_status(item['expiry_date'])
        else:
            item_dict['expiry_status'] = None
        stock_with_status.append(item_dict)
    
    conn.close()
    
    return render_template('view_stock.html', stock_items=stock_with_status)

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        # Get form data
        product_name = request.form.get('product_name')
        category = request.form.get('category')
        quantity = int(request.form.get('quantity'))
        unit = request.form.get('unit')
        purchase_price = float(request.form.get('purchase_price'))
        total_amount = float(request.form.get('total_amount'))
        supplier_name = request.form.get('supplier_name')
        purchase_date = request.form.get('purchase_date')
        has_expiry = request.form.get('has_expiry')
        expiry_date = request.form.get('expiry_date') if has_expiry == 'YES' else None
        payment_status = request.form.get('payment_status')
        paid_amount = float(request.form.get('paid_amount'))
        pending_amount = float(request.form.get('pending_amount'))
        notes = request.form.get('notes')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Update database
        conn.execute('''
            UPDATE stock SET
                product_name = ?, category = ?, quantity = ?, unit = ?, purchase_price = ?,
                total_amount = ?, supplier_name = ?, purchase_date = ?, has_expiry = ?,
                expiry_date = ?, payment_status = ?, paid_amount = ?, pending_amount = ?,
                notes = ?, updated_at = ?
            WHERE id = ?
        ''', (product_name, category, quantity, unit, purchase_price, total_amount,
              supplier_name, purchase_date, has_expiry, expiry_date, payment_status,
              paid_amount, pending_amount, notes, updated_at, id))
        
        conn.commit()
        conn.close()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('view_stock'))
    
    # GET request - fetch product data
    product = conn.execute('SELECT * FROM stock WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if product is None:
        flash('Product not found!', 'error')
        return redirect(url_for('view_stock'))
    
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:id>')
def delete_product(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM stock WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('view_stock'))

@app.route('/expiry_alert')
def expiry_alert():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    all_stock = conn.execute('SELECT * FROM stock WHERE has_expiry = "YES" AND expiry_date IS NOT NULL').fetchall()
    conn.close()
    
    expired_items = []
    near_expiry_items = []
    
    for item in all_stock:
        status = calculate_expiry_status(item['expiry_date'])
        if status == 'expired':
            expired_items.append(dict(item))
        elif status == 'near_expiry':
            near_expiry_items.append(dict(item))
    
    return render_template('expiry_alert.html', 
                         expired_items=expired_items,
                         near_expiry_items=near_expiry_items)

@app.route('/pending_suppliers')
def pending_suppliers():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    pending_items = conn.execute('SELECT * FROM stock WHERE payment_status = "PENDING" ORDER BY supplier_name').fetchall()
    
    # Calculate supplier-wise totals
    supplier_totals = {}
    for item in pending_items:
        supplier = item['supplier_name']
        if supplier not in supplier_totals:
            supplier_totals[supplier] = 0
        supplier_totals[supplier] += item['pending_amount']
    
    conn.close()
    
    return render_template('pending_suppliers.html', 
                         pending_items=pending_items,
                         supplier_totals=supplier_totals)

@app.route('/process_payment/<int:id>', methods=['POST'])
def process_payment(id):
    if 'logged_in' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    try:
        data = request.get_json()
        payment_amount = float(data.get('paymentAmount'))
        new_paid_amount = float(data.get('newPaidAmount'))
        new_pending_amount = float(data.get('newPendingAmount'))
        is_fully_paid = data.get('isFullyPaid', False)
        
        conn = get_db_connection()
        
        # Update payment information
        payment_status = 'PAID' if is_fully_paid else 'PENDING'
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn.execute('''
            UPDATE stock SET
                payment_status = ?,
                paid_amount = ?,
                pending_amount = ?,
                updated_at = ?
            WHERE id = ?
        ''', (payment_status, new_paid_amount, new_pending_amount, updated_at, id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Payment processed successfully',
            'newStatus': payment_status
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/mark_paid/<int:id>')
def mark_paid(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get current item
    item = conn.execute('SELECT * FROM stock WHERE id = ?', (id,)).fetchone()
    
    if item:
        # Update payment status
        new_paid_amount = item['paid_amount'] + item['pending_amount']
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn.execute('''
            UPDATE stock SET
                payment_status = "PAID",
                paid_amount = ?,
                pending_amount = 0,
                updated_at = ?
            WHERE id = ?
        ''', (new_paid_amount, updated_at, id))
        
        conn.commit()
        flash('Payment marked as paid!', 'success')
    
    conn.close()
    return redirect(url_for('pending_suppliers'))

@app.route('/export_stock_csv')
def export_stock_csv():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    stock_items = conn.execute('SELECT * FROM stock ORDER BY created_at DESC').fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Product Name', 'Category', 'Quantity', 'Unit', 'Purchase Price', 
                    'Total Amount', 'Supplier', 'Purchase Date', 'Has Expiry', 
                    'Expiry Date', 'Payment Status', 'Paid Amount', 'Pending Amount', 
                    'Notes', 'Created At'])
    
    # Write data
    for item in stock_items:
        writer.writerow([
            item['product_name'], item['category'], item['quantity'], item['unit'],
            item['purchase_price'], item['total_amount'], item['supplier_name'],
            item['purchase_date'], item['has_expiry'], item['expiry_date'],
            item['payment_status'], item['paid_amount'], item['pending_amount'],
            item['notes'], item['created_at']
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=stock_report.csv'}
    )

@app.route('/export_pending_csv')
def export_pending_csv():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    pending_items = conn.execute('SELECT * FROM stock WHERE payment_status = "PENDING" ORDER BY supplier_name').fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Product Name', 'Supplier', 'Pending Amount', 'Purchase Date', 'Notes'])
    
    # Write data
    for item in pending_items:
        writer.writerow([
            item['product_name'], item['supplier_name'], item['pending_amount'],
            item['purchase_date'], item['notes']
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=pending_suppliers_report.csv'}
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
