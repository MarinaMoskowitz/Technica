from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import nltk
from newspaper import Article

def index(request):
    template = loader.get_template('articles/index.html')
    context = {'articles' : gen_str()}
    return HttpResponse(template.render(context, request))

def gen_str():
    urls = ['https://www.csoonline.com/article/3227046/malware/what-is-a-fileless-attack-how-hackers-invade-systems-without-installing-software.html',
            'https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/shift-in-atm-malware-landscape-to-network-based-attacks',
            'https://www.infosecurity-magazine.com/news/virlock-ransomware-spreads/',
            'https://www.infosecurity-magazine.com/news/more-payloads-appear-for/',
            'https://www.infosecurity-magazine.com/news/wannacry-exploit-used-to-spread/',
            'https://www.engadget.com/2017/11/04/crunchyroll-hack-tried-to-infect-visitors-with-malware/',
            'https://www.infosecurity-magazine.com/news/new-waves-of-ransomware-spread/',
            'https://www.infosecurity-magazine.com/news/magnitude-ek-targets-south-korea/',
            'https://www.infosecurity-magazine.com/news/doublelocker-ransomware-changes/',
            'http://baltimore.cbslocal.com/2017/10/26/new-ransomware-attack/',
            'http://searchsecurity.techtarget.com/news/450429169/Bad-Rabbit-ransomware-data-recovery-may-be-possible']
        
            i = 0
            articles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for url in urls:
                if url is None or url == '':
                    raise ArticleException('input url bad format')
                        else:
                            a = Article(url, language='en')
                                a.download()
                                    a.parse()
                                        a.nlp()
                                            ar = Analyzed_Art(a.title, url, a.keywords, a.top_img)
                                                articles[i] = ar
                                                    i += 1

out_str = ''
    out_dict = {}
    index = 0
    for article in articles:
        artc = {'title' : article.title,
            'url' : article.url,
                'risk' : article.risk_level,
                'tags' : article.tags,
                'img' : article.img}
        out_dict[index] = artc
        index += 1
    # out_str += "{'title':%s, 'url':%s, 'risk_level':%d, 'tags',%s" % (article.title, article.url, article.risk_level, article.tags)
    
    # return out_str
    return out_dict


class Analyzed_Art:
    """
        Documentation lol
        """
    risk_level = 0
    url = ''
    title = ''
    tags = []
    img = ''
    
    def __init__(self, name, link, keywords, image):
        self.title = name
        self.url = link
        self.img = image
        self.set_tags(keywords)
        self.calc_risk(keywords)
    
    def set_tags(self, keywords):
        words_of_interest = ['injection', 'trojan', 'rabbit', 'botnet', 'worm',
                             'virus', 'spam', 'spyware', 'root',
                             'ransomware', 'rootkit', 'bios', 'honeypot',
                             'zombie', 'man in the middle', 'zero', 'nday',
                             'exploit', 'phishing', 'spearphishing', 'network',
                             'adjacent', 'local', 'physical', 'ecrypt', 'root',
                             'rootkit', 'unprivileged', 'waterhole', 'keylogger',
                             'spoofing', 'bluejacking', 'implant', 'bluesnarfing',
                             'eavesdropping', 'eavesdropped', 'eavesdrop',
                             'evil twin', 'nsa', 'russia', 'russian', 'china',
                             'chinese', 'spy', 'equifax', 'opm', 'hack',
                             'hackers', 'hacked', 'android', 'apple', 'ios',
                             'mobile', 'windows', 'microsoft', 'network',
                             'adjacent', 'local', 'physical', 'undefined',
                             'workaround', 'temporary', 'fix', 'fileless',
                             'admin', 'iso', 'tcp', 'boot', 'ssl', 'https',
                             'permission', 'remote', 'direct', 'application',
                             'layer', 'transport', 'equifax', 'plain', 'public',
                             'upd', 'http', 'undefined', 'patched', 'patch',
                             'fix', 'bot', 'encrypts', 'injection', 'inject',
                             'quantum', 'escalation', 'encryption', 'encrypted',
                             'anonymous', 'isis', 'privileged']
                             i = 0
                             for word in keywords:
                                 keywords[i] = word.lower()
                                     i += 1
                                 
    self.tags = set(keywords) & set(words_of_interest)

def calc_risk(self, keywords):
    self.risk_level = 0
        
        attack_vector = {'network': 4, 'adjacent': 3, 'local': 2, 'physical': 1}
        redemption_level = {'undefined': 4, 'workaround': 3, 'temporary': 1, 'fix': -1, 'fixed': -1, 'patch': -1, 'patched': -1}
        
        for word in keywords:
            for key, value in attack_vector.items():
                if word.lower() == key:
                    self.risk_level = self.risk_level + value
            for key, value in redemption_level.items():
                if word.lower() == key:
                    self.risk_level = self.risk_level + value
    
    
    high_complexity_words = ['ransomware', 'aes', 'fileless', 'ecrypts', 'encrypt', 'encrypted', 'encryption', 'admin', 'root', 'unprivileged', 'ISO', 'TCP', 'boot', 'SSL', 'HTTPS', 'permission', 'remote', 'direct', 'application layer', 'transport layer', 'equifax']
        self.risk_level = self.risk_level + (len(set(keywords) & set(high_complexity_words)) * 4)
        
        low_complexity_words = ['plain', 'public', 'upd', 'http']
        self.risk_level = self.risk_level + len(set(keywords) & set(low_complexity_words))

# attack_complexity = {word: 4 for word in high_complexity_words}
# attack_complexity.update({word: 1 for word in low_complexity_words})

