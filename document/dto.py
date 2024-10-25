from sqlalchemy import ScalarResult


class HistoryDTO:
    @classmethod
    def to_dict(cls, history_obj: ScalarResult) -> dict:
        return {
            "data": history_obj.data,
            "pacientId": history_obj.pacientId,
            "hospitalId": history_obj.hospitalId,
            "doctorId": history_obj.doctorId,
            "date": history_obj.date
        }