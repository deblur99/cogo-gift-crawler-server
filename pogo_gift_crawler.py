# parameters
# txt, csv
# 상한가
# 하한가
# 최대 페이지 수

# return -> object 꼴의 string type (txt로 저장한 형태)

from Gift import Gift
import requests
from bs4 import BeautifulSoup
import os
import csv

def search_gift(max_price: int = -1, min_price: int = -1, limit_page: int = 999999999):    
  base_url = 'https://cogo.co.kr'
  pagination = 1
  result = dict()
  gift_list = list()

  # while 문 탈출 조건 : ul 아래에 태그가 아무것도 없을 때
  res = requests.get(f'{base_url}/store?page={pagination}')
  soup = BeautifulSoup(res.text, 'html.parser')
  items = soup.select('ul.store_ul > li')  
  
  while len(items) != 0 and pagination < limit_page:        
    brand_list = soup.find_all('p', 'fw_700')
    brand_list = list(map(lambda n: n.text, brand_list))
    result['brand'] = brand_list
    
    product_list = soup.find_all('p', 'fw_500')
    product_list = list(map(lambda n: n.text, product_list))
    result['description'] = product_list
    
    price_list = soup.find_all('p', 'ff_tit')
    price_list = list(map(lambda n: n.text, price_list))
    result['price'] = price_list
    
    url_list = soup.select('ul.store_ul > li > a')
    url_list = list(map(lambda n: '%s/%s'%(base_url, n.get('href')), url_list))
    result['url'] = url_list
    
    # Encapsulate    
    for i in range(len(result['brand'])):
      item = Gift(result['brand'][i], result['description'][i], result['price'][i], result['url'][i])
      gift_list.append(item)
      
    pagination += 1
    res = requests.get(f'{base_url}/store?page={pagination}')
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('ul.store_ul > li')
  
  if max_price > 0 and min_price > 0:
    gift_list = list(filter(lambda n: n.get_price() >= min_price and n.get_price() <= max_price, gift_list))
    
  elif max_price > 0:
    gift_list = list(filter(lambda n: n.get_price() <= max_price, gift_list))
    
  elif min_price > 0:
    gift_list = list(filter(lambda n: n.get_price() >= min_price, gift_list))
  
  return gift_list, pagination


def export_to_file(gift_list: list, filetype: str):
    file_list = os.listdir('./')
        
    saved_index = 0
    for i in range(len(file_list)):
      if file_list[i].find('search_result') > -1:
        saved_index = i
        
    if filetype == 'txt':      
      gift_list = list(map(lambda n: n.to_string(), gift_list))
      with open('search_result.txt', 'w') as f:
        for gift in gift_list:
          f.write(f'{gift}\n')
    
    elif filetype == 'csv':
      with open('search_result.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['브랜드', '상품명', '가격', '상품 URL'])
        for gift in gift_list:
           writer.writerow(gift.to_list())


def main():  
  while True:
    price_list = list(map(lambda n: int(n), input('상한 가격과 하한 가격을 공백 구분하여 입력하세요\n>>> ').split()))
    if len(price_list) > 2:
      print('상한 가격과 하한 가격만 입력할 수 있습니다. 다시 시도하세요.\n')
    else:
      if price_list[0] < price_list[1]:
        print('잘못된 입력입니다. 상한 가격은 하한 가격보다 크거나 같은 값이어야 합니다.\n')
        continue
      break
  
  limit_page = input('\n검색할 최대 페이지 수를 입력하세요.\n아무 값도 입력하지 않거나 0 이하의 값을 입력하면, 모든 페이지를 검색합니다.\n>>> ')
  if limit_page == '':
    limit_page = 999999999
  else:
    limit_page = int(limit_page)
  
  if len(price_list) == 2:
    gift_list, pagination = search_gift(max_price=price_list[0], min_price=price_list[1], limit_page=limit_page)
  elif len(price_list) == 1:
    gift_list, pagination = search_gift(max_price=price_list[0], limit_page=limit_page)
  elif len(price_list) == 0:
    gift_list, pagination = search_gift(limit_page=limit_page)
    
  gift_list = sorted(gift_list, key=lambda gift: gift.price, reverse=True)      
    
  print(f'\n{pagination}개의 페이지를 탐색했습니다.')  
  do_saving = input('검색 결과를 .txt 또는 .csv 파일로 저장하겠습니까?\n.txt 파일로 저장하려면 "txt"를, .csv 파일로 저장하려면 "csv"를 입력하세요.\n아무 것도 저장하지 않으려면 두 문자열을 제외한 아무 문자열이나 입력하세요.\n>>> ').lower()
  if do_saving == 'txt' or do_saving == 'csv':
    export_to_file(gift_list, filetype=do_saving)
    
  input('\n저장이 완료되었습니다.\n계속하려면 엔터 키를 누르십시오...')
            
  
main()