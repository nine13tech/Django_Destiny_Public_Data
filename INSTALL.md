WHO:  
    Made by NinerOneThree  
    
WHAT:  
    Public Data Presentation for Destiny 1 and 2.
    This app works with Python Social Auth (as you will see below)
      
REQUIRES:  
    https://github.com/7SAIF/Destiny2API class (place in root of Django project like an app)   
    Django  
    Python 3.5+  
    
HOW:  
Add to settings.py:  
`'Destiny_Public_Data',`  
and  
`SOCIAL_AUTH_BUNGIE_API_KEY = '<your api key>'  
SOCIAL_AUTH_BUNGIE_ORIGIN = '<your origin key>'`  

Add to the project's urls.py:  
`url('', include('Destiny_Public_Data.urls', namespace='Destiny_Public_Data')),`
