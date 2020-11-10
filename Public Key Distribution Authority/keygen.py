import rsa
import pickle

keysize = 512

(public_PKDA, private_PKDA) = rsa.newkeys(keysize, accurate=True)
(public_A, private_A) = rsa.newkeys(keysize,accurate=True)
(public_B, private_B) = rsa.newkeys(keysize,accurate=True)

with open('ClientA.pkl', 'wb') as f:
    pickle.dump({"public":public_A,"private":private_A}, f)

with open('ClientB.pkl', 'wb') as f:
    pickle.dump({"public":public_B,"private":private_B}, f)

with open('pkda.pkl', 'wb') as f:
    pickle.dump({"public":public_PKDA,"private":private_PKDA}, f)
