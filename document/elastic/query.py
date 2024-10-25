from datetime import datetime


def get_documents_query(
    query: str,
    pacient_id: int | None = None,
    history_date: datetime | None = None,
    hospital_id: int | None = None,
    doctor_id: int | None = None
) -> dict:
    query_dict = {
        "function_score": {
            "min_score": 0.1,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "date": {"query": history_date}
                            }
                        },
                        {
                            "match": {
                                "data": {
                                    "query": query,
                                    "fuzziness": "AUTO:3,5",
                                    "operator": "and",
                                    "boost": 3.0
                                }
                            }
                        },
                    ],
                    "must": [
                        {
                            "term": {"pacientId": pacient_id}
                        },
                        {
                            "term": {"hospitalId": hospital_id}
                        },
                        {
                            "term": {"doctorId": doctor_id}
                        },
                    ]
                }
            },
            "functions": []
        },
    }
    
    add_date_filter(query_dict, history_date)
    filter_query_dict(query_dict, pacient_id, hospital_id, doctor_id)
        
    return query_dict


def add_date_filter(query_dict: dict, history_date: datetime | None = None) -> dict:
    if history_date is None:
        query_dict["function_score"]["query"]["bool"]["should"].pop(0)
    else:
        query_dict["function_score"]["functions"].append(
            {
                "gauss": {
                    "date": {
                        "origin": history_date,
                        "scale": "1d",
                        "decay": 0.5
                    }
                }
            }
        )
    return query_dict


def filter_query_dict(
    query_dict: dict,
    pacient_id: int | None = None,
    hospital_id: int | None = None,
    doctor_id: int | None = None
) -> dict:
    filters_to_remove = []
    if pacient_id is None:
        filters_to_remove.append(0)
    if hospital_id is None:
        filters_to_remove.append(1)
    if doctor_id is None:
        filters_to_remove.append(2)

    for i in sorted(filters_to_remove, reverse=True):
        query_dict["function_score"]["query"]["bool"]["must"].pop(i)

    return query_dict
