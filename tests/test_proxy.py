import sys
sys.path.insert(0, '../')
from app.models import Container
c = Container.query.all()[0]
import os
os.environ['PROXY_BASE'] = 'http://127.0.0.1:8001/api/routes'
os.environ['PROXY_TOKEN'] = '0b20cdf3c951d25936d27fc4405eb23e2e29790b00'
print c.notebook_proxy_url
