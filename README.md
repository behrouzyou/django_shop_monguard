# Django Shop

A Django e-commerce project with separate apps for products, categories, accounts, orders, and the shop homepage. The URL configuration also includes a product sitemap endpoint.

## Features visible in the code
- Product detail views based on product slugs
- Product and category apps
- Account and order areas
- Shopping-cart form integration in product detail
- Django admin
- XML sitemap for products
- Media-file serving in development

## Tech stack
- Python and Django
- Django templates
- SQLite database currently present in the repository
- CKEditor
- Django sitemap framework

## Run locally
Requires Python and pip.

```bash
git clone https://github.com/behrouzyou/django_shop_monguard.git
cd django_shop_monguard
python -m venv .venv
```

Activate the virtual environment and install the project's dependencies. Configure a development secret key and allowed hosts, then run:

```bash
python manage.py migrate
python manage.py runserver
```

## Security and maintenance
Use environment variables for secrets, exclude local databases/logs/IDE caches from version control, and do not deploy with development settings.
