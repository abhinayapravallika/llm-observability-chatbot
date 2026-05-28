from database import SessionLocal
from models import InferenceLog


def save_log(data):

    db = SessionLocal()

    try:

        log = InferenceLog(

            session_id=data.get("session_id"),

            model=data.get("model"),

            provider=data.get("provider"),

            latency=data.get("latency"),

            input_tokens=data.get("input_tokens"),

            output_tokens=data.get("output_tokens"),

            status=data.get("status"),

            input_preview=data.get("input_preview"),

            output_preview=data.get("output_preview")

        )

        db.add(log)

        db.commit()

    except Exception as e:

        print("Logging Error:", e)

        db.rollback()

    finally:

        db.close()