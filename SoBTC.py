
def parse_mempool_csv():
  no_parent = 0
  parent = 0
  with open('mempool.csv') as f:
    for line in f.readlines():
      transaction_block = line.strip().split(',')
      if transaction_block[0] == "tx_id":
        continue
      if transaction_block[3] != "":
        parent+=1
      else:
        no_parent+=1
  print(parent)
  print(no_parent)


parse_mempool_csv()