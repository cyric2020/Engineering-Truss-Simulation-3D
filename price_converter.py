# usdpt = 219.34 # Average for 304
usdpt = 227.84 # Average for 316

# Convert the USD price per tonne to AUD per kg
usdpkg = usdpt / 1000

# Get the current usd/aud exchange rate
usdaud = 1.48

audpkg = usdpkg * usdaud

# Print the result
print(audpkg)
