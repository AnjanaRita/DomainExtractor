from .domain_extractor import DomainExtractor
from .social_media_extractor import SocialMedia


class LinkExtractionError(Exception):
    pass

def link_extractor(company_name , extract_social_media_links = True, invalid_link= None, 
                   social_media = None, enable_tor=True, password= None):
    try:
        DE = DomainExtractor(company_name, invalid_link,enable_tor, password)
        return_object = DE.domain
        link = return_object.get('DOMAIN')
        if link and extract_social_media_links:
            social_links = SocialMedia(link, social_media).social_links
            return_object.update(social_links)
        return return_object
    except LinkExtractionError:
        return None