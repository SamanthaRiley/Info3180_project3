from bs4 import BeautifulSoup
import requests


def matching_words(string_1, string_2):
    count = 0
    string_1 = string_1.split()
    
    for word in string_1:
        if word in string_2:
            count += 1
    return count
    
def good_match(string, num_matching_words):
    string = string.split()
    str_len = len(string)
    if str_len > 0:
        percent =(float(num_matching_words)*100/float(str_len))
        if percent >= 50:
            return True
    return False

def get_data(url):
    try:
        result      = requests.get(url)
        soup        = BeautifulSoup(result.text, "html.parser")
        thumbnails  = []
        title       = ""
        
        if "amazon.com" in url:
            soup_title  = soup.find("span",id="productTitle")
            soup_img    = soup.find_all("img", id="landingImage")
            
            if not soup_img:
                return {"error":1,"data":{},"message":"Unable to extract images."}
            else:
                for img in soup_img:
                    if img["src"] not in thumbnails:
                        thumbnails.append(img["src"])
                
                if soup_title:
                    title = soup_title.string

            return {"error":None,"data":{"title":title, "thumbnails":thumbnails},"message":"Success"}
        
        elif "ebay.com" in url:
            soup_title = soup.find("h1", id="itemTitle")
            soup_img = soup.find_all("img", id="icImg")
            
            if not soup_img:
                return {"error":1,"data":{},"message":"Unable to extract images."}
            else:
                for img in soup_img:
                    if img["src"] not in thumbnails:
                        thumbnails.append(img["src"])
                
                if soup_title:
                    children = []
                    for child in soup_title.children:
                        children.append(child)
                    title = children[1]

            return {"error":None,"data":{"title":title, "thumbnails":thumbnails},"message":"Success"}
        
        else:
            title = soup.title.string
            for img in soup.find_all("img", alt=True):
                alt = img['alt']
                src = img['src']
                numMatchingWords = matching_words(title,alt)
                if good_match(alt, numMatchingWords):
                    if src not in thumbnails and src[-4:]==".jpg" and "sprite" not in src:
                        thumbnails.append(src)
            
            if not thumbnails:
                for img in soup.findAll("img", src=True):
                    if "sprite" not in img["src"] and src[-4:]==".jpg":
                        thumbnails.append(img["src"])
            
            if not thumbnails:
                return {"error":1,"data":{},"message":"Unable to extract images."}
    
            return {"error":None,"data":{"title":title, "thumbnails":thumbnails},"message":"Success"}
    
    except requests.exceptions.RequestException:
        return {"error":2,"data":{},"message":"URL entered is invalid."}
    
    

url1 = "https://www.amazon.com/gp/product/B00G5OAT88/ref=ox_sc_act_title_2?ie=UTF8&psc=1&smid=A3HIHADV23VGU1"
url2 = "http://www.amazon.com/dp/B00X4WHP5E/ref=fs_ods_fs_ha_dr"
url3 = "https://www.amazon.com/s/ref=s9_dnav_bw_ir02_s?node=172282,!493964,1266092011,172659,6459737011&search-alias=electronics&field-feature_five_browse-bin=2443316011&bbn=6459737011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=GST661ZR83YHCE6C68EF&pf_rd_t=101&pf_rd_p=1633959322&pf_rd_i=5969290011"
url4 = "https://www.amazon.com/Jawbone-Heart-Activity-Sleep-Tracker/dp/B00N9E6DUK/ref=lp_12633156011_1_6?srs=12633156011&ie=UTF8&qid=1462674647&sr=8-6"
url5 = "http://www.ebay.com/itm/dji-phantom-3-standard-with-2-7k-camera-and-3-axis-gimbal-cp-pt-000168/282004999561?hash=item41a8cecd89"
