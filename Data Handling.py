# DATA HANDLING SYSTEM (SINGLE FILE)

import json
import csv
import time
from typing import List, Dict, Any, Optional


# -----------------------------
# DATA MODEL
# -----------------------------

class DataRecord:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.cleaned = False
        self.timestamp = time.time()


# -----------------------------
# DATA ENGINE
# -----------------------------

class DataHandler:
    def __init__(self):
        self.dataset: List[DataRecord] = []

    # -------------------------
    # INGEST DATA
    # -------------------------
    def ingest(self, records: List[Dict[str, Any]]):
        for r in records:
            self.dataset.append(DataRecord(r))
        return {"status": "ingested", "count": len(records)}

    # -------------------------
    # CLEAN DATA
    # -------------------------
    def clean(self):
        for record in self.dataset:
            cleaned_data = {}

            for k, v in record.data.items():
                if v is None or v == "":
                    continue

                if isinstance(v, str):
                    v = v.strip()

                cleaned_data[k] = v

            record.data = cleaned_data
            record.cleaned = True

        return {"status": "cleaned", "total": len(self.dataset)}

    # -------------------------
    # VALIDATION
    # -------------------------
    def validate(self, required_fields: List[str]):
        errors = []

        for i, record in enumerate(self.dataset):
            for field in required_fields:
                if field not in record.data:
                    errors.append({
                        "index": i,
                        "missing_field": field
                    })

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    # -------------------------
    # TRANSFORMATION
    # -------------------------
    def transform(self, numeric_fields: List[str]):
        for record in self.dataset:
            for field in numeric_fields:
                if field in record.data:
                    try:
                        record.data[field] = float(record.data[field])
                    except:
                        record.data[field] = 0.0

        return {"status": "transformed"}

    # -------------------------
    # FILTER DATA
    # -------------------------
    def filter(self, key: str, value: Any):
        return [
            r.data for r in self.dataset
            if r.data.get(key) == value
        ]

    # -------------------------
    # AGGREGATION
    # -------------------------
    def aggregate_sum(self, field: str):
        total = 0

        for record in self.dataset:
            try:
                total += float(record.data.get(field, 0))
            except:
                continue

        return {"field": field, "sum": total}

    # -------------------------
    # EXPORT TO JSON
    # -------------------------
    def export_json(self, filename: str):
        data = [r.data for r in self.dataset]

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        return {"status": "exported", "file": filename}

    # -------------------------
    # EXPORT TO CSV
    # -------------------------
    def export_csv(self, filename: str):
        if not self.dataset:
            return {"error": "No data"}

        keys = self.dataset[0].data.keys()

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()

            for record in self.dataset:
                writer.writerow(record.data)

        return {"status": "exported", "file": filename}

    # -------------------------
    # QUERY DATA
    # -------------------------
    def query(self, **conditions):
        results = []

        for record in self.dataset:
            match = True

            for k, v in conditions.items():
                if record.data.get(k) != v:
                    match = False
                    break

            if match:
                results.append(record.data)

        return results

    # -------------------------
    # SUMMARY REPORT
    # -------------------------
    def summary(self):
        return {
            "total_records": len(self.dataset),
            "cleaned_records": sum(1 for r in self.dataset if r.cleaned)
        }


# -----------------------------
# EXAMPLE USAGE
# -----------------------------

if __name__ == "__main__":
    engine = DataHandler()

    sample_data = [
        {"name": "Alice", "age": "25", "salary": "50000"},
        {"name": "Bob", "age": "30", "salary": "60000"},
        {"name": "Charlie", "age": None, "salary": "70000"},
    ]

    print(engine.ingest(sample_data))
    print(engine.clean())
    print(engine.validate(["name", "age"]))
    print(engine.transform(["age", "salary"]))

    print(engine.aggregate_sum("salary"))
    print(engine.query(name="Alice"))

    print(engine.export_json("data.json"))
    print(engine.summary())