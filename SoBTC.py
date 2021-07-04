from os import path

mempool_transactions_array = []
has_parent_dict = {}
no_parent_dict = {}

visited_transactions = {}
non_visited_transactions = {}

max_block_weight = 4000000

class MempoolTransaction(): 
  def __init__(self, txid, fee, weight, parents): 
    self.txid = txid 
    self.fee = int(fee)
    self.weight = int(weight)
    self.parents = parents

  def __eq__(self, other):
        return self.fee == other.fee

  def __lt__(self, other):
      return self.fee < other.fee
    
  def __repr__(self):
      return self.txid


def check_for_file():
  file_name = "block.txt"
  if not path.exists(file_name):
    open(file_name, "x")
  else:
    open(file_name, 'w').close()

def parse_mempool_csv():
  with open('mempool.csv') as f:
    for line in f.readlines():
      transaction_block = line.strip().split(',')
      if transaction_block[0] == "tx_id":
        continue
      if transaction_block[3] != "":
        transaction_block[3] = transaction_block[3].split(";")
        has_parent_dict[transaction_block[0]] = transaction_block
      else:
        no_parent_dict[transaction_block[0]] = transaction_block
      mempool_transactions_array.append(MempoolTransaction(*transaction_block))
  sorted(mempool_transactions_array, reverse=True)

def transaction_iterator():
  for txn in mempool_transactions_array:
    print(txn.txid)
    break


def initialise():
  check_for_file()
  # parse_mempool_csv()
  # transaction_iterator()

initialise()
# print(mempool_transactions_array)