import hashlib


class CoreModule:
    def __init__(self, config_dict, raw_queue, verified_queue):
        """
        Initializes the Core Module. It now acts as the cryptographic verification layer.
        """
        self.raw_queue = raw_queue
        # Note: We push to the verified_queue now, NOT the processed_queue
        self.verified_queue = verified_queue

        # Grab the secret key from the config dictionary
        self.secret_key = config_dict.secret_key
        self.iterations = 100000

    def generate_signature(self, raw_value_str: str, key: str, iterations: int) -> str:
        """
        Generates a PBKDF2 HMAC SHA-256 signature.
        Provided by the professor in readme.txt.
        """
        password_bytes = key.encode("utf-8")
        salt_bytes = raw_value_str.encode("utf-8")

        hash_bytes = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password_bytes,
            salt=salt_bytes,
            iterations=iterations,
        )
        return hash_bytes.hex()

    def run_worker(self):
        """
        Pulls from Raw Data Stream, verifies authenticity, and pushes valid data to the Aggregator.
        """
        print("[CoreWorker] Started cryptographic verification...")

        while True:
            # 1. Pull from Raw Data Stream
            packet = self.raw_queue.get()

            # Poison pill handling
            if packet is None:
                self.verified_queue.put(None)
                break

            metric = packet.get("metric_value")
            provided_signature = packet.get("auth_signature")

            if metric is not None and provided_signature is not None:
                # 2. The professor's rules state the raw_value must be rounded to 2 decimal places
                raw_value_str = f"{metric:.2f}"

                # 3. Compute the heavy hash
                computed_hash = self.generate_signature(
                    raw_value_str, self.secret_key, self.iterations
                )

                # 4. Authenticate!
                if computed_hash == provided_signature:
                    # It's authentic! Push to the Aggregator's queue
                    self.verified_queue.put(packet)
                else:
                    # FAKE DATA! We just let the loop continue, effectively dropping the packet.
                    pass
