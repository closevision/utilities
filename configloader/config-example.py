import config

# Retrieved values can be assigned to dictionary 
apiCredentials = config.read_config(section='network-api')

print(apiCredentials['user'])
print(apiCredentials['password'])



