link_extractor
==============

# Installation

1. clone this repository.
2. `cd link_extractor` and then

```bash
python setup.py install --user
 ```
 
 # Usage

```Python
from link_extractor import extractor
data = extractor('nescafe')

#sample output looks like this:  

{'DOMAIN': 'http://www.nescafe.com/',
'ADDRESS': '',
 'COMPANY_NAME': 'Nescafé',
 'facebook': ['https://www.facebook.com/Nescafe/'],
 'linkedin': [],
 'twitter': ['https://twitter.com/nescafe'],
 'youtube': ['https://www.youtube.com/user/nescafe',
  'https://www.youtube.com/user/nescafe',
  'https://www.youtube.com/user/UKNescafe',
  'https://www.youtube.com/watch'],
 'github': [],
 'google plus': [],
 'pinterest': [],
 'instagram': ['https://www.instagram.com/nescafe/'],
 'snapchat': [],
 'flipboard': [],
 'flickr': [],
 'weibo': [],
 'periscope': [],
 'telegram': [],
 'soundcloud': [],
 'feedburner': [],
 'vimeo': [],
 'slideshare': [],
 'vkontakte': [],
 'xing': []} 
```
