{
    'name': 'Bulk Image Import for E-Commerce',
    'version': '1.0',
    'summary': 'Matches even with different capital letters and dashes! Easily bulk import product images by matching filenames to product references, names, or barcodes.',
    'category': 'Inventory',
    'author': 'Dow Group',
    'website': 'https://www.dowgroup.com',
    'support': 'info@dowgroup.com',
    'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/image_import_wizard_views.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'description': """
The Bulk Image Importer for Odoo makes product image management fast, accurate, and stress-free. 
No more renaming files or uploading one by one — just drop your images in a folder and let the app do the work.

What Makes It Smart
-------------------
- **Case-Insensitive Matching**: Works no matter how your file names look.
  - Blue Chair.jpg, blue-chair.jpg, or Blue_Chair.JPG → all match the product Blue Chair.
  - CHAIR123.jpg → matches product chair123.
- Bulk Upload: Import hundreds or thousands of images in one go.
- Smart Matching: Finds the right product by Internal Reference (SKU), Barcode, or Product Name.
- Duplicate-Safe: Skips images that are already uploaded.
- Error-Proof: Files that don’t match any product are skipped automatically.
- Handles Big Catalogs: Optimized for large imports without slowing down Odoo.
- Easy Wizard UI: Anyone can use it — no technical skills needed.

Why Choose This Importer?
-------------------------
It’s built to save you time, prevent mistakes, and handle real-world file names — making it the most reliable way to keep your Odoo catalog updated with images.

Faster. Smarter. Easier.
    """,
    'images': [
        'static/description/odoo_app_thumbnail.png',  
        'static/description/odoo image preview.svg',
        'static/description/odoo image preview(2).svg',
        'static/description/odoo image preview(3).svg',
        'static/description/odoo image preview(4).svg',
        'static/description/odoo image preview(5).svg',
        'static/description/odoo image preview(6).svg',
    ],
    'icon': 'static/description/icon.png',
    'currency': 'USD',
}
