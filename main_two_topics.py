from ReceiveFeatures import ReceiveFeatures
from database import Database
import time

def main():

    db = Database()

    save_features_receiver = ReceiveFeatures(topic="tomass/save_features")
    comp_features_receiver = ReceiveFeatures(topic="tomass/compare_features")

    cleanup_interval = 60          # run cleanup every 60 seconds
    last_cleanup = time.time()     # record last cleanup time

    while True:

        save_vectors = save_features_receiver.get_pending_vectors()

        for entry in save_vectors:

            id = entry["track_id"]
            vector = entry["features"]

            db.insert(id, vector)

        
        comp_vectors = comp_features_receiver.get_pending_vectors()

        for entry in comp_vectors:

            id = entry["track_id"]
            vector = entry["features"]

            results = db.query(vector)

            if results:
                print(f"{id} found as: {results[0]}")
            else:
                print(f"{id} not found in database")

        # periodic cleanup based on wall clock time
        now = time.time()
        if now - last_cleanup >= cleanup_interval:
            db.delete_old(max_age_seconds=cleanup_interval)  # delete docs older than cleanup_interval (for example 60 sec)
            last_cleanup = now

if __name__ == "__main__":
    main()