import requests
import numpy as np
import datetime
import copy

Today = datetime.date.today()
Acct_number = '867701887'
Roth_number = '488917295'
UID = 'BCGR0SUAECLXK2GMFJOTFCWW80PERFF5'
redirect = 'https://localhost/test'
refresh_token = "jkojfuKo9whyJ9HQVsxQUtqDuAu+9iEKfvx/pR6si/7QQP+pDkSPWQgXqzXNEq/W0K499q2lKIr56MbDoVb1jGzmARXRuFW9DlwBZlzhO7KV3nEtSiPBfgnRUShOUqK991ACTLIYMEqqyVGWhebul5/cSVu5iZyE0fM3bGaOzcFbRqix0ewsnIrHNsmb8PHOL8zRqrmjvdS7tE7EvEPxV5IbEBer4w3VpnHxN9LpJquZKCkQfGs9jl5ugwhbTRZSlbtMeM2c1y0lxf+2MJ0GGn0iwrsL2BWqOU/kwihSUanKraD0jFxqsv1zC/l3B1gGBULtqh1uF2JYB8Em7qb24x9L+yp2hmH9PiIUDOemp8NsBcNZveSnegbv45as5F6cJ+7nx8IPOYirPIHCwUIatS1CBJHHyKLaMHm3J3SKtv16jpUD66VAy1Yf0Vi100MQuG4LYrgoVi/JHHvllhhsfJkes4QOLfUv2mHdWR96Y1E6ZctKA+rXZmXlqIsib4DfPoNtaZEr5lbxuh3+hhb5ub+c7ZDaS7laJp8A12atK0eEBWr8AUZhwVTBhIohj/o/qhl0MLiEs56qSrwP8/Z7XNWE5M+5d3JYEnP1y7J3ZUjDqF849DqWKkaQIlLrfPxO7+MCKYG4V0zmUC79N1krSwPtUQ05ouLK6xqp3sCn3L2goeii6h/vO7Ov0lRFEGIEUWQaqKVwK7ZdmVlEgk90jClozPgA787UJ6/FoiEcC2qKgHG0E39/mM/gRylWOiJCl+YnnWtv68E9hywPmqNOKURbmaDOdDFVb2+RYAX6rA5QSz1d/5zGBunKjlRqONAB7tuY4aI67GorS8d1Ue3qdWicmjl+aBD4fnfxXswl3NJMQ2UYPbRWnFI6Cm+OAlM7yBgKnUH5ToM=212FD3x19z9sWBHDJACbC00B75E"
token_type = "Bearer "
Post_Access_Token = {'type':    'post',
                     'URL':     'https://api.tdameritrade.com/v1/oauth2/token',
                     'params':  {
                                'grant_type': 'refresh_token',
                                'refresh_token': refresh_token,
                                'access_type': '',
                                'code': '',
                                'client_id': UID,
                                'redirect_uri': redirect 
                                }                      
                    }
def refreshtoken():
    content = requests.post(Post_Access_Token['URL'],Post_Access_Token['params'])
    data = content.json()
    access_token = token_type+data['access_token']
    return access_token

access_token = refreshtoken()
print(access_token)
Today = datetime.date.today()
StartDate = Today + datetime.timedelta(days = 20)
EndDate = Today + datetime.timedelta(days = 90)

APIs = {'Post Access Token': Post_Access_Token,
        'Get Price History':
            {'type':   'get',
             'URL': r'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format('MMM'),
             'params':
                 {'apikey': '',
                  'periodType': 'day',
                  'period': '2',
                  'frequencyType': 'minute',
                  'frequency': '5',
                  'endDate': '',
                  'startDate': '',
                  'needExtendedHoursData':''
                 },
             'headers':
                 {'Authorization': ''
                      },
                },
        'Get Accounts':
            {'type':   'get',
              'URL': 'https://api.tdameritrade.com/v1/accounts',
              'params':
                  {'fields': r'{}'
                      },
              'headers':
                  {'Authorization': ''
                      }
             },
        'Get Account':
            {'type':   'get',
             'URL': r'https://api.tdameritrade.com/v1/accounts/{}',
             'params':
                 {'fields': r'{}'.format('positions')
                  },
             'headers':
                 {'Authorization': access_token
                  }
            },
        'Get Option Chain':
            {'type':   'get',
              'URL':    'https://api.tdameritrade.com/v1/marketdata/chains',
              'params':
                  {'apikey': '',
                   'symbol': r'{}',
                   'contractType': 'PUT',
                   'strikeCount': '',
                   'includeQuotes': '',
                   'strategy': '',
                   'interval': '',
                   'strike': '',
                   'range': 'OTM',
                   'fromDate': str(StartDate),
                   'toDate': str(EndDate),
                   'volatility': '',
                   'underlyingPrice': '',
                   'interestRate': '',
                   'daysToExpiration': '',
                   'expMonth': '',
                   'optionType': '',
                      },
                'headers':
                    {'Authorization': access_token,
                     'Content-Type': 'application/json'
                        }
                 }
        }

desired = ["symbol",'mark','delta','daysToExpiration']

def optional(dic):
    new_dic = {}
    for key in dic:
        if dic[key] != '':
            new_dic[key] = dic[key]
    return new_dic

def Request(req, form):
    request = requests.get(url = APIs[req]['URL'].format(form), params = optional(APIs[req]['params']), headers = APIs[req]['headers'])
    return request

def getPuts(symbol):
    APIs['Get Option Chain']['params']['symbol'].format(symbol)
    puts = Request('Get Option Chain', '').json
    return puts
def placeOrder(account, symbol):
    pass
def wheel_strategy(symbol,delta,minYield):
    option_chain = getPuts(symbol) 
    enter_wheel(option_chain,delta)

def find_desired_delta(option_chain, delta):
    R = {}
    choices = []
    desired = ["symbol",'mark','delta','daysToExpiration']
    for date in option_chain['putExpDateMap']:
        for price in option_chain['putExpDateMap'][date]:
            if option_chain['putExpDateMap'][date][price][0]['delta'] =='NaN'\
            or abs(option_chain['putExpDateMap'][date][price][0]['delta']) < delta-.075\
            or abs(option_chain['putExpDateMap'][date][price][0]['delta']) > delta+.075:
                continue
            R['price'] = price
            for info in desired:
                R[info] = option_chain['putExpDateMap'][date][price][0][info]
            C = copy.deepcopy(R)
            choices.append(C)
            
    for put in choices:
        Yield = 100*float(put['mark'])/(float(put['price']))
        put['Yield'] = round(Yield,2)
        AdjYield = Yield*30/put['daysToExpiration']
        # AnnYield = (1+Yield)**(365/put['daysToExpiration'])-1
        put['AdjYield'] = round(AdjYield,2)
    return choices

def enter_wheel(option_chain, delta):
    find_desired_delta(option_chain, delta)

def monitor_puts(symbol, minYield):
    positions = Request('Get Account', Acct_number).json()
    market_puts = find_desired_delta(getPuts(symbol), 0.3)
    active_puts = []
    for position in positions['securitiesAccount']['positions']:
        if  position['instrument']['assetType'] == 'OPTION'\
        and position['instrument']['putCall'] == 'PUT'\
        and position['instrument']['underlyingSymbol'] == symbol:
            active_puts.append(position)
    for position in active_puts:
        option_symbol = position['instrument']['symbol']
        profit = 100*position['averagePrice']
        print(profit)

print(getPuts('F'))
            
# print(APIs['Get Account']['URL'].format(Acct_number))
# print(find_starting_puts('F',.3)[0])
print('Done')