mempool_transactions_array = []

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


def parse_mempool_csv():
  with open('mempool.csv') as f:
    for line in f.readlines():
      transaction_block = line.strip().split(',')
      if transaction_block[0] == "tx_id":
        continue
      mempool_transactions_array.append(MempoolTransaction(*transaction_block))

parse_mempool_csv()
print(mempool_transactions_array)
print(sorted(mempool_transactions_array, reverse=True))