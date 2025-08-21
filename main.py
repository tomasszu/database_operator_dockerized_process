from ReceiveFeatures import ReceiveFeatures
from database import Database

def main():

    db = Database()

    save_features_receiver = ReceiveFeatures(topic="tomass/save_features")
    comp_features_receiver = ReceiveFeatures(topic="tomass/compare_features")


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



if __name__ == "__main__":
    main()