## DRF Project to allocate service areas for providers

### Tools used:
* [Django](https://www.djangoproject.com/)
* [GeoDjango](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/)
* [DRF](https://www.django-rest-framework.org/)
* [DRF-GIS](https://github.com/djangonauts/django-rest-framework-gis)
* [DRF](https://www.django-rest-framework.org/)
* [Docker](https://www.docker.com/)
* [Dokku](https://github.com/dokku/dokku)
* [PyTest](https://pytest-django.readthedocs.io/en/latest/)

### Premise:
we have a growing problem that many transportation suppliers we'd like to 
integrate cannot give us concrete zipcodes, cities, etc that they serve. 
To combat this, we'd like to be able to define custom polygons as their "service area" 
and we'd like for the owners of these shuttle companies to be able to define and alter 
their polygons whenever they want, eliminating the need for employees to do this boring grunt work.

Project should have API endpoints to create, update, delete, and retreive information about providers. Batch operations are not necessary except for get. A provider should contain the following information:

    - Name

    - Email

    - Phone Number

    - Language

    - Currency

Once a provider is created they should be able to start defining service areas. 
These service areas will be geojson polygons and should be stored in the database 
in a way that they can be retreived and queried upon easily. 
There should be endpoints to create, update, delete, and get a polygon. 
Batch operations are not necessary except for get. 
A polygon should contain a name and price as well as the geojson information.

You should create an API endpoint to query this data. 
It should take a lat/lng pair as arguments and return a list of all polygons 
that include the given lat/lng. The name of the polygon, provider's name, and price 
should be returned for each polygon. This operation should be FAST. 
There are thousand of providers and hundreds of thousands of service areas.

Admin panel: <base_url>/admin/
Api Docs: <base_url>/docs/