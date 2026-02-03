================================================================================
                    GENERAL STORE STOCK MANAGEMENT APP
================================================================================

A complete offline stock management system for general stores. No internet required!
Perfect for small shops and personal inventory management.

================================================================================
                            FEATURES
================================================================================

✅ STOCK MANAGEMENT
   • Add new products with complete details
   • Edit existing product information
   • Delete products from inventory
   • View all stock in sortable table format

✅ EXPIRY ALERT SYSTEM
   • Automatic detection of expired items
   • Near expiry alerts (within 7 days)
   • Color-coded expiry status
   • Separate expiry dashboard

✅ SUPPLIER PAYMENT TRACKING
   • Track pending supplier payments
   • Mark payments as paid
   • Supplier-wise pending totals
   • Payment status indicators

✅ DASHBOARD WITH STATISTICS
   • Total products count
   • Total stock quantity
   • Near expiry items count
   • Expired items count
   • Total pending supplier payments

✅ SEARCH & FILTER
   • Search by product name or supplier
   • Filter expiry items
   • Filter pending payments
   • Sortable table columns

✅ CSV EXPORT
   • Export complete stock report
   • Export pending payments report
   • Supplier-wise reports

✅ MOBILE FRIENDLY
   • Works on Android phones
   • Works on iPhone browsers
   • Responsive design
   • Touch-friendly interface

================================================================================
                            TECH STACK
================================================================================

• Backend: Python (Flask)
• Frontend: HTML5, CSS3 (Flexbox + Grid)
• Database: SQLite (local file)
• No internet connection required
• No cloud services
• No external APIs

================================================================================
                            INSTALLATION
================================================================================

1. REQUIREMENTS
   • Python 3.7 or higher
   • No additional packages needed (uses only Python standard library)

2. SETUP STEPS
   • Extract/Download the app folder
   • Open Command Prompt/Terminal
   • Navigate to the app folder
   • Run: python app.py

3. ACCESS THE APP
   • Open browser and go to: http://localhost:5000
   • Default login password: admin123

================================================================================
                            USAGE GUIDE
================================================================================

LOGIN
-----
• Password: admin123
• Click "Login" to access dashboard

ADDING PRODUCTS
---------------
1. Click "Add Product" from sidebar
2. Fill in all required fields:
   • Product Name, Category, Quantity, Unit
   • Purchase Price (per unit)
   • Total Amount (auto-calculated)
   • Supplier Name, Purchase Date
   • Expiry information (if applicable)
   • Payment details
3. Click "Add Product" to save

VIEWING STOCK
-------------
1. Click "View Stock" from sidebar
2. See all products in sortable table
3. Use search bar to find products
4. Use filter buttons for expiry/pending items
5. Click column headers to sort
6. Edit or delete products using action buttons

EXPIRY ALERTS
-------------
1. Click "Expiry Alerts" from sidebar
2. View expired items (red)
3. View near expiry items (orange)
4. Take action to reduce waste

SUPPLIER PAYMENTS
-----------------
1. Click "Pending Payments" from sidebar
2. View all pending supplier payments
3. See supplier-wise totals
4. Click "Mark Paid" to settle payments
5. Export pending payments report

EXPORTING DATA
--------------
1. From sidebar or dashboard
2. Click "Export Stock CSV" for full inventory
3. Click "Export Pending CSV" for payment report
4. Files download automatically

================================================================================
                            DATA FIELDS
================================================================================

Each product stores:
• Product Name
• Category (Groceries, Beverages, Dairy, etc.)
• Quantity and Unit
• Purchase Price (per unit)
• Total Amount
• Supplier Name
• Purchase Date
• Expiry Date (optional)
• Payment Status (PAID/PENDING)
• Paid Amount
• Pending Amount
• Notes

================================================================================
                            COLOR CODING
================================================================================

🔴 RED    = Expired items
🟠 ORANGE  = Near expiry (≤7 days)
🟡 YELLOW  = Pending supplier payments
🟢 GREEN   = Paid items / Fresh items

================================================================================
                            MOBILE USAGE
================================================================================

• App works perfectly on mobile browsers
• Use hamburger menu (☰) for navigation
• Tables are scrollable horizontally
• Forms stack vertically on small screens
• Touch-friendly buttons and controls

================================================================================
                            TROUBLESHOOTING
================================================================================

DATABASE ISSUES
---------------
• If database gets corrupted, delete 'stock.db' file
• Restart app - new database will be created automatically

PORT ALREADY IN USE
------------------
• Close other applications using port 5000
• Or modify app.py line 335: change port=5000 to another port

APP NOT STARTING
----------------
• Check Python version (3.7+ required)
• Ensure you're in correct directory
• Check for syntax errors in app.py

MOBILE DISPLAY ISSUES
---------------------
• Refresh browser page
• Clear browser cache
• Ensure latest browser version

================================================================================
                            SECURITY NOTES
================================================================================

• Default password: admin123 (change in app.py if needed)
• App runs locally only (no internet access)
• Database file stored locally (stock.db)
• No data sent to external servers
• Perfect for offline use

================================================================================
                            BACKUP YOUR DATA
================================================================================

IMPORTANT: Regular backup recommended!

1. BACKUP METHOD
   • Copy entire app folder to backup location
   • Or copy just 'stock.db' file

2. BACKUP FREQUENCY
   • Daily for active users
   • Weekly for moderate usage
   • Monthly for light usage

3. RESTORATION
   • Replace 'stock.db' with backup file
   • Restart app

================================================================================
                            SUPPORT
================================================================================

This is a self-contained offline application.
No internet connection or external support required.

For issues:
• Check troubleshooting section above
• Restart the application
• Verify Python installation
• Ensure all files are present in folder

================================================================================
                            FILE STRUCTURE
================================================================================

general_store_app/
│
├── app.py                 # Main Flask application
├── stock.db              # SQLite database (created automatically)
│
├── templates/            # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   ├── add_product.html
│   ├── edit_product.html
│   ├── view_stock.html
│   ├── expiry_alert.html
│   └── pending_suppliers.html
│
├── static/
│   └── css/
│       └── style.css     # Modern responsive CSS
│
└── README.txt            # This file

================================================================================
Enjoy using your General Store Stock Management App! 🏪

Created with ❤️ for small business owners
Version 1.0 - 2024
================================================================================
