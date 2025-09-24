# Deploy to PythonAnywhere

## Quick Steps:

1. **Zip your project folder**
2. **Upload to PythonAnywhere Files**
3. **Extract in console**: `unzip ecommm.zip`
4. **Install requirements**: `pip3.10 install --user -r requirements.txt`
5. **Create web app** in PythonAnywhere dashboard
6. **Set WSGI file** to point to your project
7. **Configure static files** path to `/static/`

## WSGI Configuration:
```python
import os
import sys
path = '/home/yourusername/ecommm'
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecom.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```