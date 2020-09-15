import re
import hashlib

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(raw_html) )
    return cleantext

class Detection:
    def __init__(self, url, 
                risk, 
                threats, 
                vulnerability, 
                weakness, 
                instance, 
                assets, 
                countermeasure, 
                attacks, 
                likelihood_of_exploit, 
                scan_tool
    ):

        if (url is None) or (url.strip() == ''):
            raise ValueError('url cannot be None or empty')

        self.url = url

        if not risk is None:
            self.risk = cleanhtml(risk)
        else:
            self.risk = None

        if not threats is None:
            self.threats = cleanhtml(threats)
        else:
            self.threats = None

        if not vulnerability is None:
            self.vulnerability = cleanhtml(vulnerability)
        else:
            self.vulnerability = None

        if not weakness is None:
            self.weakness = cleanhtml(weakness)
        else:
            self.weakness = None

        if not instance is None:
            self.instance = cleanhtml(instance)
        else:
            self.instance = None

        if not assets is None:
            self.assets = cleanhtml(assets)
        else:
            self.assets = None

        if not countermeasure is None:
            self.countermeasure = cleanhtml(countermeasure)
        else:
            self.countermeasure = None

        if not attacks is None:
            self.attacks = cleanhtml(attacks)
        else:
            self.attacks = None

        if not likelihood_of_exploit is None:
            self.likelihood_of_exploit = cleanhtml(likelihood_of_exploit)
        else:
            self.likelihood_of_exploit = None
        
        self.scan_tool = cleanhtml(scan_tool)

        self.nist = ''

    def getId(self):
        items_to_hash = [self.vulnerability, self.weakness, self.instance, self.countermeasure, self.attacks]
        return str(hashlib.md5(''.join(items_to_hash).encode('utf-8')).hexdigest())