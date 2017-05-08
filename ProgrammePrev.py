#	coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import lxml.html
import mysql.connector
from mysql.connector import errorcode
import datetime
from datetime import timedelta


chrome_path="./chromedriver"
driver = webdriver.Chrome(chrome_path)


#connexion  à la base de données


# try:
# 	cnn=mysql.connector.connect(
# 		user='xxxxxx',
# 		password='xxxx',
# 		host='xxxx',
# 		database='xxxxx')
# 	print ("BD connectee!!")
# except mysql.connector.Error as e:
# 	if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
# 		print "Something is wrong with username or password"
# 	elif e.errno == errorcode.ER_BAD_BD_ERROR:
# 		print "DATABASE Does not exist"
# 	else:
# 		print e
# cursor= cnn.cursor(buffered=True)

driver.get("https://www.marchespublics.gov.ma/index.php5?page=entreprise.ListePPs")
#
year="2017"
driver.find_element_by_xpath("//select[@name='ctl0$CONTENU_PAGE$anneePP']/option[text()='"+year+"']").click()

time.sleep(1)


driver.find_element_by_xpath('//*[@id="ctl0_CONTENU_PAGE_panelSearchInPP"]/input[2]').click()
time.sleep(3)

page = lxml.html.fromstring(driver.page_source)
rows = page.xpath('//*[@id="ctl0_CONTENU_PAGE_tableauPP_panelListePPs"]/div[2]/div[1]/table/tbody/tr')
compteur=1
t=0
for row in rows:
	telechargement=page.xpath('//*[@id="ctl0_CONTENU_PAGE_tableauPP_panelListePPs"]/div[2]/div[1]/table/tbody/tr['+str(compteur)+']/td[1]/a/@href')
	if len(telechargement) > 0:
		t=1
		telechargement=telechargement[0].split('javascript:popUp(\'')[1].split('\')')[0]
		tele="https://www.marchespublics.gov.ma/"+telechargement;
		#print tele
		org=page.xpath('//*[@id="ctl0_CONTENU_PAGE_tableauPP_panelListePPs"]/div[2]/div[1]/table/tbody/tr['+str(compteur)+']/td[2]/span/text()')
		idOrg=0
		if len (org) >= 1:
			org=org[0].replace('\n', '').replace('\t', '').replace('\'', '').strip() 

		print org

		annee=page.xpath('//*[@id="ctl0_CONTENU_PAGE_tableauPP_panelListePPs"]/div[2]/div[1]/table/tbody/tr['+str(compteur)+']/td[3]/span/text()')[0].replace('\n', '').replace('\t', '').replace('\'', '').strip()
		print annee

		datep=page.xpath('//*[@id="ctl0_CONTENU_PAGE_tableauPP_panelListePPs"]/div[2]/div[1]/table/tbody/tr['+str(compteur)+']/td[4]/span/text()')[0].replace('\n', '').replace('\t', '').replace('\'', '').strip()
		print datep

		print org.encode('utf-8')+" "+annee.encode('utf-8')+" "+datep.encode('utf-8')+" "+tele.encode('utf-8')
		compteur+=1
	if t == 0:
		print "la liste est vide"