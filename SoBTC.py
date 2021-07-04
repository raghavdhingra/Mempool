from os import path

mempool_transactions_array = []

visited_transactions = {}
non_visited_transactions = {}

max_block_weight = 4000000

class MempoolTransaction(): # Mempool transaction class, acting as a data store for a transaction
  def __init__(self, txid, fee, weight, parent): 
    self.txid = txid 
    self.fee = int(fee)
    self.weight = int(weight)
    self.parent = parent

  def __eq__(self, other):
        return self.fee == other.fee

  def __lt__(self, other):
      return self.fee < other.fee
    
  def __repr__(self):
      return self.txid


def check_for_file(): # File Checker, whether the txt file is present or not
  file_name = "block.txt"
  if not path.exists(file_name):
    open(file_name, "x")
  else:
    open(file_name, 'w').close()

def parse_mempool_csv():
  with open('mempool.csv') as f: # Reading mempool csv
    for line in f.readlines(): # Reading lines
      transaction_block = line.strip().split(',') # Spliting lines by commas (,) symbol
      if transaction_block[0] == "tx_id": # Checking for the existence of header
        continue
      if transaction_block[3] != "": # Checking for the parents
        transaction_block[3] = transaction_block[3].split(";") # if parent is present, converting it to arrays of parents, else empty array
      else:
        transaction_block[3] = []
      mempool_transactions_array.append(MempoolTransaction(*transaction_block)) # Appending a list of transaction classes
  sorted(mempool_transactions_array, reverse=True) # Sorting based on fees in descending order

def transaction_iterator():
  for txn in mempool_transactions_array:
    if len(txn.parent) == 0:
      # Has no parent
      print("no parent")
    else:
      # Has parent
      print("Has parent")
    break


def initialise():
  check_for_file()
  parse_mempool_csv()
  transaction_iterator()

initialise()
# print(mempool_transactions_array)