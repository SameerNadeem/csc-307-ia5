import matplotlib.pyplot as plt

aes_key_sizes = [128, 192, 256]
aes_throughput = [323230.52, 277175.00, 240674.21]

rsa_key_sizes = [512, 1024, 2048, 4096]
rsa_sign_throughput = [7143.9, 2174.3, 540.9, 101.1]
rsa_verify_throughput = [235224.4, 111199.9, 38364.1, 10074.7]

plt.figure(figsize=(8, 5))
plt.plot(aes_key_sizes, aes_throughput, marker='o', label='AES Throughput')
plt.title('AES Throughput vs. Key Size')
plt.xlabel('AES Key Size (bits)')
plt.ylabel('Throughput (KB per second)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(rsa_key_sizes, rsa_sign_throughput, marker='o', label='RSA Signing Throughput')
plt.title('RSA Signing Throughput vs. Key Size')
plt.xlabel('RSA Key Size (bits)')
plt.ylabel('Throughput (operations per second)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(rsa_key_sizes, rsa_verify_throughput, marker='o', label='RSA Verification Throughput')
plt.title('RSA Verification Throughput vs. Key Size')
plt.xlabel('RSA Key Size (bits)')
plt.ylabel('Throughput (operations per second)')
plt.legend()
plt.grid(True)
plt.show()