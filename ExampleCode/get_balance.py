import pyupbit

access_key = "access key"
secret_key = "secret key"

upbit = pyupbit.Upbit(access_key, secret_key)
print(upbit.get_balances())