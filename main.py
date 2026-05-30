from typing import List, Dict, Any, Generator

class Field:
    def validate(self, value: Any) -> Any:
        return value

class Int(Field):
    def validate(self, value: Any) -> int:
        return int(value)

class Str(Field):
    def __init__(self, lowercase: bool = False):
        self.lowercase = lowercase

    def validate(self, value: Any) -> str:
        string_val = str(value)
        return string_val.lower() if self.lowercase else string_val

class Pipe:
    def __init__(self, schema: Dict[str, Field]):
        self.schema = schema
        self._current_data: List[Dict[str, Any]] = []

    def drain(self, data: List[Dict[str, Any]]) -> 'Pipe':
        """Ingest raw data into the pipe."""
        self._current_data = data
        return self

    def stream(self) -> Generator[Dict[str, Any], None, None]:
        """Lazily validate and yield records one by one."""
        for record in self._current_data:
            processed_record = {}
            for key, field in self.schema.items():
                # Case-insensitive lookup helper for messy source data
                source_key = next((k for k in record if k.lower() == key.lower()), key)
                if source_key in record:
                    processed_record[key] = field.validate(record[source_key])
                else:
                    processed_record[key] = None
            yield processed_record

    def to_list(self) -> List[Dict[str, Any]]:
        return list(self.stream())

    def to_polars(self):
        import polars as pl
        return pl.DataFrame(self.to_list())