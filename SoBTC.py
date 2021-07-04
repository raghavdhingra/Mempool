from os import path

mempool_transactions_array = []

visited_transactions = {}
non_visited_parent_transactions = {}

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
  global mempool_transactions_array
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
  mempool_transactions_array = sorted(mempool_transactions_array, reverse=True) # Sorting based on fees in descending order

def file_writer_txn_id(txn): # For block weight calculations, and writing the transaction id in block txt file
  global max_block_weight
  block_file = open("block.txt", "a")
  max_block_weight = max_block_weight - txn.fee
  block_file.write(txn.txid + "\n")
  visited_transactions[txn.txid] = txn
  block_file.close()

def has_parent_iterator(txn): # Iteration over the transactions with parent id
  is_parent_visited = True
  for p_txn in txn.parent:
    if p_txn in visited_transactions:
      continue
    else:
      is_parent_visited = False
      non_visited_parent_transactions[p_txn] = txn
      break
  if is_parent_visited:
    if max_block_weight - txn.fee < 0:
      return 1
    file_writer_txn_id(txn)

def transaction_iterator(): # Iteration over the transaction for finding the parent and non parent transactions
  for txn in mempool_transactions_array:
    if len(txn.parent) == 0:
      # Has no parent
      if max_block_weight - txn.fee < 0:
        break
      file_writer_txn_id(txn)
      if txn.txid in non_visited_parent_transactions:
        v_p_txn = non_visited_parent_transactions[txn.txid]
        is_parent_visited = True
        for p_txn in v_p_txn.parent:
          if p_txn in visited_transactions:
            continue
          else:
            is_parent_visited = False
            non_visited_parent_transactions[p_txn] = txn
            break
        if is_parent_visited:
          file_writer_txn_id(v_p_txn)
          
    else:
      # Has parent
      p_res = has_parent_iterator(txn)
      if p_res == 1:
        break

def initialise(): # initialising all the events and the functions
  check_for_file()
  parse_mempool_csv()
  transaction_iterator()

initialise() # Calling the initialise function
