from opensearch_logic import Opensearch_db


class Database:
    def __init__(self):

        self.db = Opensearch_db("localhost", 9200, ("admin", "admin"))

        self.list_of_existing_ids = set()

    def insert(self, id, vector, cam_id):

        self.db.insert(id, vector, cam_id)

    def query(self, id, vector, cam_id):

        composite_id = int(str(cam_id) + str(id))
        corrected_id = None

        if composite_id in self.list_of_existing_ids:
            print(f"{composite_id} found in local cache\n")
            self.insert(composite_id, vector, cam_id)
        else:
            print(f"{composite_id} not found in local cache, querying database\n")
            
            filtered_result = self.db.query_vector(vector, cam_id)

            if filtered_result:
                print(f"{composite_id} from {cam_id} found in database as: {filtered_result[0]}\n")
                corrected_id = filtered_result[0][0]
                self.insert(corrected_id, vector, cam_id)
            else:
                print(f"{id} from {cam_id} not found in database\n")
                print(f"Inserting as new id: {composite_id}\n")
                self.insert(composite_id, vector, cam_id)

                self.list_of_existing_ids.add(composite_id)

        return (composite_id, cam_id) if corrected_id is None else (corrected_id, cam_id)
    
    def delete_old(self, max_age_seconds=60):
        self.db.delete_old(max_age_seconds=max_age_seconds)