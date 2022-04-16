import yfinance as yf
import csv



filename = "test.csv"
fields = []
rows = []
prices = []
lowest_times = []
lowest_times_count = {}
highest_times = []
highest_times_count = {}



class HourlyPrice:
    def __init__(self, date, time):
        self.date = date
        self.time = time
        self.day_open = {}
        self.day_close = {}
        self.day_high = {}
        self.day_low = {}
    
    def min_price(self):
        min_open = min(self.day_open, key=self.day_open.get)
        min_close = min(self.day_close, key=self.day_close.get)
        temp = min(self.day_open[min_open], self.day_close[min_close])
        if temp == self.day_open[min_open]:
            return(min_open, min(self.day_open[min_open], self.day_close[min_close]))
        else:
            return(min_close, min(self.day_open[min_open], self.day_close[min_close]))
    
    def max_price(self):
        min_open = max(self.day_open, key=self.day_open.get)
        min_close = max(self.day_close, key=self.day_close.get)
        temp = max(self.day_open[min_open], self.day_close[min_close])
        if temp == self.day_open[min_open]:
            return(min_open, max(self.day_open[min_open], self.day_close[min_close]))
        else:
            return(min_close, max(self.day_open[min_open], self.day_close[min_close]))
    
    def add_open(self, time, open):
        self.day_open[time] = open
    
    def add_close(self, time, close):
        self.day_close[time] = close
    
    def add_high(self, time, high):
        self.day_high[time] = high
    
    def add_low(self, time, low):
        self.day_low[time] = low

def get_info():
    intraday_data = yf.download(tickers="ARTL",
                                period="60d",
                                interval="15m",
                                auto_adjust=True)
    #intraday_data.drop(columns=['Volume', 'High', 'Low'], inplace=True)
    print(intraday_data.tail())
    intraday_data.to_csv(filename, header=True)




def parse_csv(filename, fields, rows):
    
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        fields.append(next(csvreader))
        
        
    
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
            


def print_parsed(fields, rows):
    # printing the field names
    
    for field in fields:
        field[0] = "Date"
       # print('Field names are:' + ', '.join(field))
        #print(field[0])
    
    #  printing first 5 rows
    #print('\nFirst 5 rows are:\n')
    #for row in rows[:5]:
        # parsing each column of a row
        #for col in row:
            #print("%10s"%col,end=" "),
        #print('\n')

def convert_to_class(prices, rows):
    last_date = ''
    count = 0
    for row in rows:
        temp = row[0]
        date = temp[:10]
        #print(date)
        time = temp[11:]
        #print(time)
        if date == last_date:
            prices[count-1].day_open[time] = 0
            prices[count-1].day_close[time] = 0
            prices[count-1].day_high[time] = 0
            prices[count-1].day_low[time] = 0
            prices[count-1].add_open(time, row[1])
            prices[count-1].add_close(time, row[4])
            prices[count-1].add_high(time, row[2])
            prices[count-1].add_low(time, row[3])
        else:
            prices.append(HourlyPrice(date, time))
            prices[count].day_open[time] = 0
            prices[count].day_close[time] = 0
            prices[count].day_high[time] = 0
            prices[count].day_low[time] = 0
            prices[count].add_open(time, row[1])
            prices[count].add_close(time, row[4])
            prices[count].add_high(time, row[2])
            prices[count].add_low(time, row[3])
            count += 1
        
        last_date = date
    
    

def lowest(prices, lowest_times):
    
    for obj in prices:
        lowest_time, lowest_value = obj.min_price()
        lowest_times.append(lowest_time)
        #print(f"Date:{obj.date} | Open {obj.day_open} | Close {obj.day_close}")
        #print(obj.min_price())

def lowest_count(lowest_times, lowest_times_count):
    for time in lowest_times_count:
        for i in lowest_times:
            #print(time, i)
            if time == i:
                lowest_times_count[time] += 1

def highest(prices, highest_times):
    
    for obj in prices:
        highest_time, highest_value = obj.max_price()
        highest_times.append(highest_time)

        #print(f"Date:{obj.date} | Open {obj.day_open} | Close {obj.day_close}")
        #print(obj.min_price())

def highest_count(highest_times, highest_times_count):
    for time in highest_times_count:
        for i in highest_times:
            #print(time, i)
            if time == i:
                highest_times_count[time] += 1

def test_buy_sell(prices):
    start = 100
    profit = 0
    buy_date = '09:30:00-05:00'
    sell_date = '15:45:00-05:00'
    for i in range(len(prices)):
        
        if i > 0 and i < 59:
            buy_price = min(prices[i].day_open[buy_date], prices[i].day_close[buy_date])
            sell_price = max(prices[i].day_open[sell_date], prices[i].day_close[sell_date])
            amount = start/float(buy_price)
            profit += (int(amount) * float(sell_price))-100
            
    return profit

def fill_dict(rows, lowest_times_count, highest_times_count):
    for row in rows:
        temp = row[0]
        lowest_times_count[temp[11:]] = 0
        highest_times_count[temp[11:]] = 0
    
        



get_info()
parse_csv(filename, fields, rows)
print_parsed(fields, rows)
convert_to_class(prices, rows)
fill_dict(rows, lowest_times_count, highest_times_count)
lowest(prices, lowest_times)
lowest_count(lowest_times, lowest_times_count)
highest(prices, highest_times)
highest_count(highest_times, highest_times_count)
for price in prices:
    for i in price.day_high:

        print(f"High is {price.day_high[i]}")
#print("Lowest:")
#for key, value in lowest_times_count.items():
#    if value > 0:
#        print(key, value)
#print(lowest_times_count)
#print("Highest:")
#for key, value in highest_times_count.items():
#    if value > 0:
#        print(key, value)
#print(highest_times_count)
#print(f"Profit: {test_buy_sell(prices)}")

