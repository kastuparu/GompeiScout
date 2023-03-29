from pymongo import MongoClient


def get_database():
    mongodb_url = "mongodb+srv://kastuparu:S5qbLeQ1dby8DxpJ@cluster0.juawsdp.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongodb_url)
    return client["23_wpi_district"]


if __name__ == "__main__":
    dbname = get_database()
