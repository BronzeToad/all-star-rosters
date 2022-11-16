import google.cloud.bigquery as gcpBigQuery
import os.path as osPath

from string import capwords as strCapwords

import helpers.data_utils as DataHelper
import helpers.env_utils as EnvHelper

# ============================================================================ #

class BigQueryLoader:

    ROOT_DIR = EnvHelper.get_root_dir()
    SCHEMA_DIR = osPath.join(ROOT_DIR, 'configs', 'bigquery_schemas')
    GCP_PROJECT = EnvHelper.get_gcp_project()
    GCP_BUCKET = EnvHelper.get_gcp_bucket()
    
    def __init__(self,
                 data_source: str,
                 table_id: str,
                 **kwargs):
        
        self.data_source = data_source
        self.table_id = table_id
        
        default_params = DataHelper.get_json(folder=osPath.join(self.ROOT_DIR, 'configs'),
                                             filename='bigquery_defaults')
        
        default_params.update(kwargs)
        
        self.allow_jagged_rows = default_params['allow_jagged_rows']
        self.allow_quoted_newlines = default_params['allow_quoted_newlines']
        self.autodetect = default_params['autodetect']
        self.create_disposition = default_params['create_disposition']
        self.field_delimiter = default_params['field_delimiter']
        self.ignore_unknown_values = default_params['ignore_unknown_values']
        self.labels = default_params['labels']
        self.max_bad_records = default_params['max_bad_records']
        self.null_marker = default_params['null_marker']
        self.quote_character = default_params['quote_character']
        self.schema_file = default_params['schema_file']
        self.skip_leading_rows = default_params['skip_leading_rows']
        self.source_format = default_params['source_format']
        self.write_disposition = default_params['write_disposition']

# ============================================================================ #

    @property
    def data_source(self) -> str:
        return self._data_source
    
    @data_source.setter
    def data_source(self, val) -> None:
        if val not in self.valid_data_sources:
            raise ValueError(f'Invalid data source: {val}')
        self._data_source = val
        
    
    @property
    def table_id(self) -> str:
        return self._table_id
    
    @table_id.setter
    def table_id(self, val: str) -> None:
        self._table_id = val

# ============================================================================ #

    @property
    def allow_jagged_rows(self) -> str:
        return self._allow_jagged_rows
    
    @allow_jagged_rows.setter
    def allow_jagged_rows(self, val: str) -> None:
        self._allow_jagged_rows = val
        
    
    @property
    def allow_quoted_newlines(self) -> str:
        return self._allow_quoted_newlines
    
    @allow_quoted_newlines.setter
    def allow_quoted_newlines(self, val: str) -> None:
        self._allow_quoted_newlines = val
        
    
    @property
    def autodetect(self) -> str:
        return self._autodetect
    
    @autodetect.setter
    def autodetect(self, val: str) -> None:
        self._autodetect = val
        
    
    @property
    def create_disposition(self) -> str:
        return self._create_disposition
    
    @create_disposition.setter
    def create_disposition(self, val: str) -> None:
        self._create_disposition = val
    
    
    @property
    def field_delimiter(self) -> str:
        return self._field_delimiter
    
    @field_delimiter.setter
    def field_delimiter(self, val: str) -> None:
        self._field_delimiter = val
    
    
    @property
    def ignore_unknown_values(self) -> str:
        return self._ignore_unknown_values
    
    @ignore_unknown_values.setter
    def ignore_unknown_values(self, val: str) -> None:
        self._ignore_unknown_values = val
        
        
    @property
    def labels(self) -> str:
        return self._labels
    
    @labels.setter
    def labels(self, val: str) -> None:
        self._labels = val
        
    
    @property
    def max_bad_records(self) -> str:
        return self._max_bad_records
    
    @max_bad_records.setter
    def max_bad_records(self, val: str) -> None:
        self._max_bad_records = val
        
        
    @property
    def null_marker(self) -> str:
        return self._null_marker
    
    @null_marker.setter
    def null_marker(self, val: str) -> None:
        self._null_marker = val
        
    
    @property
    def quote_character(self) -> str:
        return self._quote_character
    
    @quote_character.setter
    def quote_character(self, val: str) -> None:
        self._quote_character = val
        
        
    @property
    def schema_file(self) -> str:
        return self._schema_file
    
    @schema_file.setter
    def schema_file(self, val: str) -> None:
        self._schema_file = val
        
    
    @property
    def skip_leading_rows(self) -> str:
        return self._skip_leading_rows
    
    @skip_leading_rows.setter
    def skip_leading_rows(self, val: str) -> None:
        self._skip_leading_rows = val
        
        
    @property
    def source_format(self) -> str:
        return self._source_format
    
    @source_format.setter
    def source_format(self, val: str) -> None:
        self._source_format = val
    
    
    @property
    def write_disposition(self) -> str:
        return self._write_disposition
    
    @write_disposition.setter
    def write_disposition(self, val: str) -> None:
        self._write_disposition = val

# ============================================================================ #

    @property
    def filename(self) -> str:
        return DataHelper.force_extension(self.table_id, 'csv')

    @property
    def gcp_dir(self) -> str:
        return osPath.join(self.GCP_BUCKET, self.data_source)
    
    @property
    def gcp_filepath(self) -> str:
        return osPath.join(self.gcp_dir, self.filename)
    
    @property
    def job_id_prefix(self) -> str:
        _source = DataHelper.snek_to_camel(self.data_source)
        _table = DataHelper.snek_to_camel(self.table_id)
        _timestamp = DataHelper.get_epoch_timestamp()        
        return f'{_source}_{_table}_{_timestamp()}_'

    @property
    def destination(self) -> str:
        return f'{self.GCP_PROJECT}.{self.data_source}.{self.table_id}'
    
    @property
    def schema(self) -> dict:
        return DataHelper.get_json(folder=osPath.join(self.SCHEMA_DIR, self.data_source),
                                   filename=self.filename)
    
    @property
    def job_config(self):
        return gcpBigQuery.job.LoadJobConfig(allow_jagged_rows=self.allow_jagged_rows,
                                             allow_quoted_newlines=self.allow_quoted_newlines,
                                             autodetect=self.autodetect,
                                             create_disposition=self.create_disposition,
                                             field_delimiter=self.field_delimiter,
                                             ignore_unknown_values=self.ignore_unknown_values,
                                             max_bad_records=self.max_bad_records,
                                             quote_character=self.quote_character,
                                             skip_leading_rows=self.skip_leading_rows,
                                             write_disposition=self.write_disposition,
                                             schema=self.schema)
    
    @property
    def job_result(self):
        _job = gcpBigQuery.Client().load_table_from_uri(source_uris=self.gcp_filepath,
                                                        destination=self.destination,
                                                        job_id_prefix=self.job_id_prefix,
                                                        job_config=self.job_config,
                                                        timeout=300.0)
        return _job.result()
    
    @property
    def job_details(self):
        return self.job_result.to_api_repr()
    
    @property
    def job_id(self):
        return self.job_result.job_id

# ============================================================================ #

    # @classmethod



# ============================================================================ #

if __name__ == '__main__':
    print('\n\n------------------------------------------------')
    