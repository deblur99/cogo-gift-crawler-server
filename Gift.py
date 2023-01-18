class Gift:
  brand: str
  product: str
  price: str
  url: str
  
  def __init__(self, brand: str, product: str, price: str, url: str):
    self.brand = brand
    self.product = product
    self.price = price
    self.url = url
    
  def get_price(self):
    return int(self.price.replace(',', '').replace('P', ''))
    
  def to_string(self):
    return f'{self.brand}, {self.price}, {self.product}, {self.url}'
  
  def to_list(self):
    return [self.brand, self.price, self.product, self.url]
  

# test
# cake = Gift('투썸플레이스', '파티팩 아이스박스', '42,900P', 'https://cogo.co.kr/store_detail/2')
# print(cake.to_string())