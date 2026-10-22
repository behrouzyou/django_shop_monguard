# Django Shop

A Django e-commerce project with separate apps for products, categories, accounts, orders, and the shop homepage. The URL configuration also includes a product sitemap endpoint.

## Features visible in the code
- Product detail views based on slugs
- Product and category apps
- Account and order areas
- Shopping-cart form integration in product detail
- Django admin
- XML sitemap for products
- Media-file serving in development

## Stack
- Python and Django
- Django templates
- CKEditor
- Django sitemap framework

## Run locally
Create and activate a Python virtual environment, install project dependencies, configure a private development secret key, and run:

```bash
python manage.py migrate
python manage.py runserver
```

## Security and maintenance
Use environment variables for secrets, exclude local databases/logs/IDE caches from version control, and do not deploy with development settings.
