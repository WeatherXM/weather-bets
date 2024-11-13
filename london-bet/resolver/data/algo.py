import base64
from cryptography.hazmat.primitives import serialization, asymmetric, hashes
from cryptography import exceptions
from operator import itemgetter


def m5(pub_key, packet_b64, packet_sig):
    verifying_key = serialization.load_pem_public_key(bytes(pub_key, "utf-8"))
    sig_bytes = base64.urlsafe_b64decode(packet_sig)
    sig_der = asymmetric.utils.encode_dss_signature(
        int.from_bytes(sig_bytes[0:32], "big"),
        int.from_bytes(sig_bytes[32:64], "big"),
    )
    try:
        verifying_key.verify(
            sig_der,
            bytes(packet_b64, "utf-8"),
            asymmetric.ec.ECDSA(hashes.SHA256()),
        )
        return True
    except exceptions.InvalidSignature:
        return False


def helium(pub_key, packet_b64, packet_sig):
    verifying_key = serialization.load_pem_public_key(bytes(pub_key, "utf-8"))
    sig_bytes = base64.urlsafe_b64decode(packet_sig)
    sig_der = asymmetric.utils.encode_dss_signature(
        int.from_bytes(sig_bytes[0:32], "big"),
        int.from_bytes(sig_bytes[32:64], "big"),
    )
    try:
        verifying_key.verify(
            sig_der,
            base64.urlsafe_b64decode(packet_b64),
            asymmetric.ec.ECDSA(hashes.SHA256()),
        )
        return True
    except exceptions.InvalidSignature:
        return False


def d1(pub_key, packet_b64, packet_sig):
    verifying_key = serialization.load_pem_public_key(bytes(pub_key, "utf-8"))
    sig_bytes = base64.urlsafe_b64decode(packet_sig)
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(chosen_hash)
    hasher.update(str(packet_b64).encode("ascii"))
    digest = hasher.finalize()
    try:
        verifying_key.verify(
            sig_bytes,
            digest,
            asymmetric.padding.PKCS1v15(),
            asymmetric.utils.Prehashed(chosen_hash),
        )
        return True
    except exceptions.InvalidSignature:
        return False

type_to_fn = {
    "WS1000": m5,
    "WS2001": helium,
    "WS2000": helium,
    "WG1200": d1
}

def verify(df):
    verified_mask = []
    devices = []
    for index, record in df.iterrows():
        name, pub_key, packet_b64, packet_sig, model = df.loc[index, ['name', 'public_key_PEM', 'ws_packet_b64', 'ws_packet_sig', 'model']]
        fn = type_to_fn.get(model)
        if name not in devices:
            devices.append(name)
        if model == 'WS1001':
            verified_mask.append(False)
            continue
        if fn is None:
            print(f"{name}: verification failed - not supported hardware bundle '{record}'")
            verified_mask.append(False)
            continue

        try:
            verified = fn(pub_key, packet_b64, packet_sig)
            verified_mask.append(verified)
        except Exception as e:
            verified_mask.append(False)
    filtered_df = df.loc[verified_mask].copy()
    print('VERIFIED DEVICES {}'.format(filtered_df['name'].unique()))
    return filtered_df