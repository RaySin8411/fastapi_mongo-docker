import pymongo

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = client['db_name']
    buildings = db_name['Building']

    result = buildings.aggregate([
        # Group the documents and "count" via $sum on the values
        {"$group": {
            "_id": {
                "city_area": "$city_area",
            },
            "count": {"$sum": 1}
        }}
    ])
    for x in sorted(list(result), key=lambda d: d['count']):
        print(f'{x["_id"]["city_area"]}: {x["count"]}')

    result = buildings.aggregate([
        {
            "$group": {
                "_id": {
                    "city_area": "$city_area",
                    "area_id": "$area_id",
                    "use_license": "$use_license",
                    "construction_license": "$construction_license",

                },
                "applicant": {"$last": "$applicant"},
                "designer": {"$last": "$designer"},
                "date": {"$last": '$date'},
            }
        },
        {
            "$project": {
                "city_area": "$city_area",
                "area_id": "$area_id",
                "use_license": "$use_license",
                "construction_license": "$construction_license",
                "applicant": "$applicant",
                "designer": "$designer",
                "date": "$date"
            }
        },
        {
            "$match": {
                "date": {"$ne": ''}
            }
        },
        {
            "$sort": {
                'date': 1
            }
        },
        {
            "$limit": 1
        }

    ])
    print(list(result))
